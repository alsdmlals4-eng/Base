#!/usr/bin/env python3
"""Fail-closed public YouTube caption ingest for local research evidence.

The reference implementation intentionally does not download video/audio and does not
invoke a cloud transcript API. yt-dlp is used only to discover video metadata and
caption track URLs; WebVTT normalization is handled with the Python standard library.
A caller-supplied local transcript can be used when yt-dlp is unavailable.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import stat
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
TAG_RE = re.compile(r"<[^>]+>")
TIMING_RE = re.compile(r"^\s*(\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})\s+-->\s+(\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})")
ALLOWED_YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
    "www.youtu.be",
}
ALLOWED_CAPTION_HOST_SUFFIXES = ("youtube.com", "googlevideo.com")
DEFAULT_OUTPUT_ROOT = Path(".tmp/public-video-research")
DEFAULT_LANGUAGES = ("ko", "en", "en-US")
MAX_LOCAL_TRANSCRIPT_BYTES = 5 * 1024 * 1024
LOCAL_TRANSCRIPT_SUFFIXES = {".vtt", ".srt", ".txt"}


class VideoIngestError(RuntimeError):
    """Expected fail-closed error with a machine-readable code."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


class NoCaptionTrack(VideoIngestError):
    def __init__(self, detail: str = "no supported caption track was available") -> None:
        super().__init__("ASR_FALLBACK_REQUIRED", detail)


class EmptyTranscript(VideoIngestError):
    def __init__(self, detail: str = "caption payload contained no usable cues") -> None:
        super().__init__("EMPTY_TRANSCRIPT", detail)


def _validated_video_id(value: str) -> str:
    if not VIDEO_ID_RE.fullmatch(value):
        raise ValueError(f"invalid YouTube video id: {value!r}")
    return value


def extract_video_id(value: str) -> str:
    """Extract a strict 11-character YouTube video id from common URL forms."""
    candidate = value.strip()
    if VIDEO_ID_RE.fullmatch(candidate):
        return candidate

    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_YOUTUBE_HOSTS:
        raise ValueError("only YouTube video URLs or bare video IDs are supported")

    if host.endswith("youtu.be"):
        return _validated_video_id(parsed.path.strip("/").split("/", 1)[0])

    path_parts = [part for part in parsed.path.split("/") if part]
    if parsed.path == "/watch":
        values = parse_qs(parsed.query).get("v", [])
        if not values:
            raise ValueError("YouTube watch URL is missing the v parameter")
        return _validated_video_id(values[0])
    if len(path_parts) >= 2 and path_parts[0] in {"shorts", "embed", "live"}:
        return _validated_video_id(path_parts[1])
    raise ValueError("unsupported YouTube video URL form")


def _language_keys(available: Sequence[str], preferred: Sequence[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for requested in preferred:
        if requested in available and requested not in seen:
            ordered.append(requested)
            seen.add(requested)
        base = requested.split("-", 1)[0].lower()
        variants = sorted(
            key
            for key in available
            if key not in seen and key.split("-", 1)[0].lower() == base
        )
        ordered.extend(variants)
        seen.update(variants)
    return ordered


def _select_vtt_entry(entries: object) -> Mapping[str, object] | None:
    if not isinstance(entries, list):
        return None
    candidates = [item for item in entries if isinstance(item, Mapping) and isinstance(item.get("url"), str)]
    for item in candidates:
        if str(item.get("ext", "")).lower() == "vtt":
            return item
    return None


def choose_caption_track(metadata: Mapping[str, object], languages: Sequence[str]) -> dict[str, object]:
    """Choose a manual WebVTT track first, then an automatic WebVTT track."""
    source_sections = (
        ("subtitles", "youtube_manual_caption", False),
        ("automatic_captions", "youtube_auto_caption", True),
    )
    for section_name, source_kind, generated in source_sections:
        section = metadata.get(section_name)
        if not isinstance(section, Mapping):
            continue
        available = [key for key in section if isinstance(key, str)]
        for language in _language_keys(available, list(languages)):
            entry = _select_vtt_entry(section.get(language))
            if entry is None:
                continue
            url = str(entry["url"])
            return {
                "source_kind": source_kind,
                "language": language,
                "is_generated": generated,
                "track_label": str(entry.get("name") or language),
                "url": url,
                "ext": "vtt",
            }
    raise NoCaptionTrack()


def _timestamp_seconds(value: str) -> float:
    parts = value.replace(",", ".").split(":")
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    raise ValueError(f"invalid WebVTT timestamp: {value!r}")


def _clean_caption_text(lines: Sequence[str]) -> str:
    raw = " ".join(line.strip() for line in lines if line.strip())
    without_tags = TAG_RE.sub("", raw)
    decoded = html.unescape(without_tags)
    return re.sub(r"\s+", " ", decoded).strip()


def parse_vtt(text: str) -> list[dict[str, object]]:
    """Normalize timestamped WebVTT cues and drop only consecutive duplicates."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    blocks = re.split(r"\n\s*\n", normalized)
    segments: list[dict[str, object]] = []
    previous_text: str | None = None

    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        first = lines[0].strip()
        if first == "WEBVTT" or first.startswith(("NOTE", "STYLE", "REGION")):
            continue

        timing_index = -1
        timing_match = None
        for index, line in enumerate(lines):
            match = TIMING_RE.match(line)
            if match:
                timing_index = index
                timing_match = match
                break
        if timing_match is None:
            continue

        cue_text = _clean_caption_text(lines[timing_index + 1 :])
        if not cue_text or cue_text == previous_text:
            continue
        previous_text = cue_text
        segments.append(
            {
                "start_sec": _timestamp_seconds(timing_match.group(1)),
                "end_sec": _timestamp_seconds(timing_match.group(2)),
                "text": cue_text,
            }
        )

    if not segments:
        raise EmptyTranscript()
    return segments


def _parse_plain_text(text: str) -> list[dict[str, object]]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    segments: list[dict[str, object]] = []
    for block in re.split(r"\n\s*\n", normalized):
        cleaned = re.sub(r"\s+", " ", block).strip()
        if cleaned:
            segments.append({"start_sec": None, "end_sec": None, "text": cleaned})
    if not segments:
        raise EmptyTranscript("local transcript contained no usable text")
    return segments


def _read_local_transcript(path: Path) -> tuple[bytes, str]:
    suffix = path.suffix.lower()
    if suffix not in LOCAL_TRANSCRIPT_SUFFIXES:
        raise VideoIngestError(
            "UNSUPPORTED_LOCAL_TRANSCRIPT_FORMAT",
            "local transcript must use .vtt, .srt, or .txt",
        )
    try:
        with path.open("rb") as stream:
            opened = os.fstat(stream.fileno())
            if not stat.S_ISREG(opened.st_mode):
                raise VideoIngestError(
                    "LOCAL_TRANSCRIPT_NOT_REGULAR_FILE",
                    "local transcript must be a regular file",
                )
            if opened.st_size > MAX_LOCAL_TRANSCRIPT_BYTES:
                raise VideoIngestError(
                    "LOCAL_TRANSCRIPT_TOO_LARGE",
                    f"local transcript exceeds {MAX_LOCAL_TRANSCRIPT_BYTES} bytes",
                )
            payload = stream.read(MAX_LOCAL_TRANSCRIPT_BYTES + 1)
    except VideoIngestError:
        raise
    except OSError as error:
        raise VideoIngestError("LOCAL_TRANSCRIPT_READ_FAILED", "unable to read local transcript") from error
    if len(payload) > MAX_LOCAL_TRANSCRIPT_BYTES:
        raise VideoIngestError(
            "LOCAL_TRANSCRIPT_TOO_LARGE",
            f"local transcript exceeds {MAX_LOCAL_TRANSCRIPT_BYTES} bytes",
        )
    try:
        text = payload.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise VideoIngestError("LOCAL_TRANSCRIPT_ENCODING_FAILED", "local transcript must be UTF-8") from error
    return payload, text


def validate_caption_url(value: str) -> str:
    """Prevent metadata-driven fetches outside known HTTPS YouTube caption hosts."""
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    allowed_host = any(host == suffix or host.endswith(f".{suffix}") for suffix in ALLOWED_CAPTION_HOST_SUFFIXES)
    if parsed.scheme != "https" or not allowed_host:
        raise VideoIngestError("UNSAFE_CAPTION_URL", "caption URL must be HTTPS on a YouTube/GoogleVideo host")
    return value


def _iso_upload_date(value: object) -> str | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d{8}", value):
        return None
    return f"{value[:4]}-{value[4:6]}-{value[6:8]}"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_evidence_packet(
    metadata: Mapping[str, object],
    *,
    source_url: str,
    tool_version: str,
    track: Mapping[str, object] | None,
    segments: Sequence[Mapping[str, object]],
    status: str,
    checked_at: str | None = None,
) -> dict[str, object]:
    """Build a provenance-preserving local research packet."""
    video_id = str(metadata.get("id") or extract_video_id(source_url))
    _validated_video_id(video_id)
    segment_payload = [dict(item) for item in segments]
    source_kind = str(track.get("source_kind")) if track else "none"
    language = str(track.get("language")) if track else None
    is_generated = bool(track.get("is_generated")) if track else False
    track_label = str(track.get("track_label")) if track and track.get("track_label") else None

    return {
        "schema_version": 1,
        "source_url": source_url,
        "canonical_url": str(metadata.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}"),
        "video_id": video_id,
        "title": str(metadata.get("title") or ""),
        "uploader_or_channel": str(metadata.get("channel") or metadata.get("uploader") or ""),
        "duration_sec": metadata.get("duration"),
        "published_or_uploaded_at": _iso_upload_date(metadata.get("upload_date")),
        "retrieval": {
            "tool": "yt-dlp",
            "tool_version": tool_version,
            "checked_at": checked_at or _utc_now(),
        },
        "transcript": {
            "status": status,
            "source_kind": source_kind,
            "language": language,
            "is_generated": is_generated,
            "track_label": track_label,
            "segment_count": len(segment_payload),
            "segments": segment_payload,
        },
        "storage_policy": {
            "full_transcript": "LOCAL_RESEARCH_ONLY",
            "default_output_root": ".tmp/public-video-research",
            "repository_evidence": "DERIVED_NOTES_AND_TIMESTAMPS_ONLY",
        },
        "content_claim_ceiling": (
            "TRANSCRIPT_EVIDENCE_ONLY_NOT_FACT_VERIFICATION"
            if status == "READY"
            else "BLOCKED_UNVERIFIED"
        ),
    }


def ingest_local_transcript(
    source_url: str,
    transcript_file: Path,
    *,
    language: str | None = None,
) -> dict[str, object]:
    """Normalize a caller-supplied local transcript without invoking yt-dlp."""
    video_id = extract_video_id(source_url)
    source_url_value = (
        f"https://www.youtube.com/watch?v={video_id}"
        if VIDEO_ID_RE.fullmatch(source_url.strip())
        else source_url
    )
    path = Path(transcript_file)
    payload, text = _read_local_transcript(path)
    suffix = path.suffix.lower()
    timestamped = suffix in {".vtt", ".srt"}
    segments = parse_vtt(text) if timestamped else _parse_plain_text(text)
    source_kind = {
        ".vtt": "local_vtt",
        ".srt": "local_srt",
        ".txt": "local_plain_text",
    }[suffix]
    metadata: dict[str, object] = {
        "id": video_id,
        "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
    }
    track: dict[str, object] = {
        "source_kind": source_kind,
        "language": language,
        "is_generated": False,
    }
    packet = build_evidence_packet(
        metadata,
        source_url=source_url_value,
        tool_version="local-file",
        track=track,
        segments=segments,
        status="READY",
    )
    packet["retrieval"] = {
        "tool": "local-file",
        "tool_version": "filesystem",
        "checked_at": _utc_now(),
    }
    transcript = packet["transcript"]
    if isinstance(transcript, dict):
        transcript["timestamp_evidence"] = "AVAILABLE" if timestamped else "UNAVAILABLE"
        transcript["is_generated"] = None
    packet["local_transcript_input"] = {
        "format": suffix.removeprefix("."),
        "byte_length": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "video_binding": "UNVERIFIED",
        "creation_source": "UNKNOWN",
    }
    packet["content_claim_ceiling"] = (
        "LOCAL_TRANSCRIPT_TIMESTAMPS_ONLY_VIDEO_BINDING_UNVERIFIED_NOT_FACT_VERIFICATION"
        if timestamped
        else "LOCAL_TRANSCRIPT_TEXT_ONLY_VIDEO_BINDING_UNVERIFIED_NOT_FACT_VERIFICATION"
    )
    return packet


def _run_ytdlp(arguments: Sequence[str], *, yt_dlp: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [yt_dlp, *arguments],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )
    except FileNotFoundError as error:
        raise VideoIngestError("MISSING_YT_DLP", f"executable not found: {yt_dlp}") from error
    except subprocess.TimeoutExpired as error:
        raise VideoIngestError("YT_DLP_TIMEOUT", f"yt-dlp exceeded {timeout} seconds") from error


def fetch_ytdlp_version(yt_dlp: str = "yt-dlp") -> str:
    result = _run_ytdlp(["--version"], yt_dlp=yt_dlp, timeout=15)
    if result.returncode != 0 or not result.stdout.strip():
        raise VideoIngestError("YT_DLP_VERSION_FAILED", result.stderr.strip()[:500] or "yt-dlp --version failed")
    return result.stdout.strip().splitlines()[0]


def fetch_metadata(source_url: str, yt_dlp: str = "yt-dlp") -> dict[str, object]:
    expected_video_id = extract_video_id(source_url)
    result = _run_ytdlp(
        ["--ignore-config", "--skip-download", "--no-playlist", "--dump-single-json", source_url],
        yt_dlp=yt_dlp,
    )
    if result.returncode != 0:
        raise VideoIngestError("METADATA_FETCH_FAILED", result.stderr.strip()[:1000] or "yt-dlp metadata fetch failed")
    try:
        payload: Any = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise VideoIngestError("METADATA_FETCH_FAILED", "yt-dlp did not return valid JSON") from error
    if not isinstance(payload, dict):
        raise VideoIngestError("METADATA_FETCH_FAILED", "yt-dlp metadata root was not an object")
    actual_video_id = str(payload.get("id") or "")
    if actual_video_id != expected_video_id:
        raise VideoIngestError("VIDEO_ID_MISMATCH", f"requested {expected_video_id}, received {actual_video_id or 'missing id'}")
    return payload


def _safe_caption_headers(metadata: Mapping[str, object]) -> dict[str, str]:
    raw = metadata.get("http_headers")
    if not isinstance(raw, Mapping):
        return {"User-Agent": "Base-Public-Video-Research-Ingest/1"}
    allowed = {"user-agent", "referer", "accept-language"}
    headers = {
        str(key): str(value)
        for key, value in raw.items()
        if isinstance(key, str) and isinstance(value, str) and key.lower() in allowed
    }
    headers.setdefault("User-Agent", "Base-Public-Video-Research-Ingest/1")
    return headers


def fetch_caption_text(track_url: str, metadata: Mapping[str, object], *, timeout: int = 30) -> str:
    safe_url = validate_caption_url(track_url)
    request = urllib.request.Request(safe_url, headers=_safe_caption_headers(metadata))
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - validated HTTPS host
            validate_caption_url(response.geturl())
            data = response.read()
    except urllib.error.HTTPError as error:
        raise VideoIngestError("CAPTION_FETCH_FAILED", f"HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise VideoIngestError("CAPTION_FETCH_FAILED", str(error.reason)) from error
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise VideoIngestError("CAPTION_FETCH_FAILED", "caption payload was not UTF-8 WebVTT") from error


def ingest_public_video(
    source_url: str,
    *,
    languages: Sequence[str] = DEFAULT_LANGUAGES,
    yt_dlp: str = "yt-dlp",
) -> dict[str, object]:
    """Fetch metadata + one caption track; return fail-closed ASR state when absent."""
    extract_video_id(source_url)
    tool_version = fetch_ytdlp_version(yt_dlp)
    metadata = fetch_metadata(source_url, yt_dlp)
    try:
        track = choose_caption_track(metadata, languages)
    except NoCaptionTrack:
        return build_evidence_packet(
            metadata,
            source_url=source_url,
            tool_version=tool_version,
            track=None,
            segments=[],
            status="ASR_FALLBACK_REQUIRED",
        )
    caption_text = fetch_caption_text(str(track["url"]), metadata)
    segments = parse_vtt(caption_text)
    return build_evidence_packet(
        metadata,
        source_url=source_url,
        tool_version=tool_version,
        track=track,
        segments=segments,
        status="READY",
    )


def write_packet(
    packet: Mapping[str, object],
    *,
    output: Path | None,
    default_root: Path = DEFAULT_OUTPUT_ROOT,
) -> Path:
    video_id = _validated_video_id(str(packet.get("video_id") or ""))
    path = output if output is not None else default_root / f"{video_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dict(packet), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def _parse_languages(value: str) -> tuple[str, ...]:
    languages = tuple(item.strip() for item in value.split(",") if item.strip())
    if not languages:
        raise argparse.ArgumentTypeError("at least one language code is required")
    return languages


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_url", help="YouTube URL or 11-character video ID")
    parser.add_argument("--langs", type=_parse_languages, default=DEFAULT_LANGUAGES, help="comma-separated language priority")
    parser.add_argument("--yt-dlp", default="yt-dlp", dest="yt_dlp", help="yt-dlp executable path")
    parser.add_argument("--transcript-file", type=Path, help="caller-supplied local .vtt/.srt/.txt transcript")
    parser.add_argument("--language", help="language code for --transcript-file provenance")
    parser.add_argument("--output", type=Path, help="local JSON packet path; defaults under .tmp/")
    args = parser.parse_args(argv)

    source_url = args.source_url
    if VIDEO_ID_RE.fullmatch(source_url):
        source_url = f"https://www.youtube.com/watch?v={source_url}"
    try:
        if args.transcript_file is not None:
            packet = ingest_local_transcript(source_url, args.transcript_file, language=args.language)
        else:
            packet = ingest_public_video(source_url, languages=args.langs, yt_dlp=args.yt_dlp)
        path = write_packet(packet, output=args.output)
    except (VideoIngestError, ValueError) as error:
        code = error.code if isinstance(error, VideoIngestError) else "INVALID_SOURCE_URL"
        detail = error.detail if isinstance(error, VideoIngestError) else str(error)
        print(json.dumps({"status": "BLOCKED_UNVERIFIED", "code": code, "detail": detail}, ensure_ascii=False), file=sys.stderr)
        return 1

    status = str(packet["transcript"]["status"])  # type: ignore[index]
    print(json.dumps({"status": status, "packet": str(path)}, ensure_ascii=False))
    return 0 if status == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
