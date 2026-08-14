"""Native Windows Job Object ownership for suspended Tool Hub children."""

from __future__ import annotations

import os


class WindowsOwnershipError(RuntimeError):
    """Raised when Windows cannot establish exact child process-tree ownership."""


CREATE_SUSPENDED = 0x00000004
CREATE_NO_WINDOW = 0x08000000


if os.name == "nt":
    import ctypes
    from ctypes import wintypes

    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    JobObjectExtendedLimitInformation = 9
    PROCESS_TERMINATE = 0x0001
    PROCESS_SET_QUOTA = 0x0100
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    THREAD_SUSPEND_RESUME = 0x0002
    TH32CS_SNAPTHREAD = 0x00000004
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    ULONG_PTR = ctypes.c_size_t
    SIZE_T = ctypes.c_size_t

    class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", SIZE_T),
            ("MaximumWorkingSetSize", SIZE_T),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ULONG_PTR),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class IO_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_ulonglong),
            ("WriteOperationCount", ctypes.c_ulonglong),
            ("OtherOperationCount", ctypes.c_ulonglong),
            ("ReadTransferCount", ctypes.c_ulonglong),
            ("WriteTransferCount", ctypes.c_ulonglong),
            ("OtherTransferCount", ctypes.c_ulonglong),
        ]

    class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
            ("IoInfo", IO_COUNTERS),
            ("ProcessMemoryLimit", SIZE_T),
            ("JobMemoryLimit", SIZE_T),
            ("PeakProcessMemoryUsed", SIZE_T),
            ("PeakJobMemoryUsed", SIZE_T),
        ]

    class THREADENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ThreadID", wintypes.DWORD),
            ("th32OwnerProcessID", wintypes.DWORD),
            ("tpBasePri", wintypes.LONG),
            ("tpDeltaPri", wintypes.LONG),
            ("dwFlags", wintypes.DWORD),
        ]

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
    _kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    _kernel32.SetInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    )
    _kernel32.SetInformationJobObject.restype = wintypes.BOOL
    _kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    _kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    _kernel32.CreateToolhelp32Snapshot.argtypes = (wintypes.DWORD, wintypes.DWORD)
    _kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    _kernel32.Thread32First.argtypes = (wintypes.HANDLE, ctypes.POINTER(THREADENTRY32))
    _kernel32.Thread32First.restype = wintypes.BOOL
    _kernel32.Thread32Next.argtypes = (wintypes.HANDLE, ctypes.POINTER(THREADENTRY32))
    _kernel32.Thread32Next.restype = wintypes.BOOL
    _kernel32.OpenThread.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    _kernel32.OpenThread.restype = wintypes.HANDLE
    _kernel32.ResumeThread.argtypes = (wintypes.HANDLE,)
    _kernel32.ResumeThread.restype = wintypes.DWORD
    _kernel32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
    _kernel32.TerminateJobObject.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    _kernel32.CloseHandle.restype = wintypes.BOOL


def _windows_error(message: str) -> WindowsOwnershipError:
    if os.name != "nt":
        return WindowsOwnershipError(message)
    code = ctypes.get_last_error()
    return WindowsOwnershipError(f"{message} (winerror={code})")


class WindowsJobOwner:
    """Own one Windows Job Object and attach exactly one suspended root process."""

    def __init__(self) -> None:
        if os.name != "nt":
            raise WindowsOwnershipError("Windows Job Objects are unavailable on this platform")
        self._handle = _kernel32.CreateJobObjectW(None, None)
        if not self._handle:
            raise _windows_error("could not create Windows Job Object")
        self._closed = False
        self._assigned = False
        limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not _kernel32.SetInformationJobObject(
            self._handle,
            JobObjectExtendedLimitInformation,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            self.close()
            raise _windows_error("could not configure Windows Job Object")

    def attach_and_resume(self, process_id: int) -> None:
        if self._closed or self._assigned:
            raise WindowsOwnershipError("Windows Job Object is not attachable")
        access = PROCESS_TERMINATE | PROCESS_SET_QUOTA | PROCESS_QUERY_LIMITED_INFORMATION
        process = _kernel32.OpenProcess(access, False, process_id)
        if not process:
            raise _windows_error("could not open suspended child process")
        try:
            if not _kernel32.AssignProcessToJobObject(self._handle, process):
                raise _windows_error("could not assign suspended child to Windows Job Object")
            self._assigned = True
        finally:
            _kernel32.CloseHandle(process)

        thread_ids = self._thread_ids(process_id)
        if len(thread_ids) != 1:
            raise WindowsOwnershipError("suspended child did not expose exactly one primary thread")
        thread = _kernel32.OpenThread(THREAD_SUSPEND_RESUME, False, thread_ids[0])
        if not thread:
            raise _windows_error("could not open suspended child primary thread")
        try:
            previous = _kernel32.ResumeThread(thread)
            if previous == 0xFFFFFFFF:
                raise _windows_error("could not resume suspended child primary thread")
            if previous < 1:
                raise WindowsOwnershipError("child primary thread was not suspended")
        finally:
            _kernel32.CloseHandle(thread)

    @staticmethod
    def _thread_ids(process_id: int) -> list[int]:
        snapshot = _kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
        if snapshot == INVALID_HANDLE_VALUE:
            raise _windows_error("could not enumerate suspended child threads")
        try:
            entry = THREADENTRY32()
            entry.dwSize = ctypes.sizeof(entry)
            result: list[int] = []
            if _kernel32.Thread32First(snapshot, ctypes.byref(entry)):
                while True:
                    if entry.th32OwnerProcessID == process_id:
                        result.append(int(entry.th32ThreadID))
                    entry.dwSize = ctypes.sizeof(entry)
                    if not _kernel32.Thread32Next(snapshot, ctypes.byref(entry)):
                        break
            return result
        finally:
            _kernel32.CloseHandle(snapshot)

    def terminate(self, exit_code: int = 1) -> None:
        if self._closed:
            return
        if self._assigned and not _kernel32.TerminateJobObject(self._handle, exit_code):
            raise _windows_error("could not terminate Windows Job Object")

    def close(self) -> None:
        if self._closed:
            return
        handle = self._handle
        self._handle = None
        self._closed = True
        if handle:
            _kernel32.CloseHandle(handle)

    def __enter__(self) -> "WindowsJobOwner":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
