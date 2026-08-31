from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
RUNNER_PATH = ROOT / ".github/workflows-support/temp_ai_solution_layer_runner.py"

spec = importlib.util.spec_from_file_location("temp_ai_solution_layer_runner", RUNNER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("unable to load bounded candidate runner")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

runner.PUBLIC_VIDEO_CONTRACT = r'''`PUBLIC_VIDEO_SOURCE_RECOVERY_BEFORE_BLOCKER` / `VIDEO_LINK_IS_NOT_UNREADABLE_UNTIL_DECLARED_READER_LADDER_EXHAUSTED`: 사용자가 YouTube 같은 공개 영상의 내용 확인·요약·역공학·흡수를 요청하면 일반 웹 페이지 렌더 실패만으로 링크를 읽을 수 없다고 판정하지 않는다. 먼저 `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`의 현행 `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER`와 `tools/public_video_research_ingest.py`를 읽고, 해당 owner가 선언한 `source_ladder`와 evidence ceiling을 실제로 실행한다.

```text
exact video/source identity readback
→ current owner-declared source_ladder
→ normalize any already-available local transcript through the existing adapter
→ preserve ASR_FALLBACK_REQUIRED and source-binding ceiling
→ only after the declared reader ladder is exhausted: BLOCKED_UNVERIFIED
```

- 이 route는 root `AGENTS.md`의 unreadable external-link blocker를 약화하거나 별도 자막 정본을 만들지 않는다. 전용 owner가 이미 선언한 reader와 허용 fallback을 소진하기 전에는 “현재 도구로 읽지 못함”이 확정되지 않았다는 source-specific dispatch다.
- 영상·오디오 자체를 자동 다운로드하거나 `yt-dlp`·ASR·새 패키지를 자동 설치하지 않는다. hosted transcript SaaS·paid proxy·별도 유료 API/계정/credit를 기본 fallback으로 추가하지 않는다.
- 자막 전문은 local research evidence로만 다루고 repository에는 결정에 필요한 파생 요약·짧은 인용·timestamp·source identity만 남긴다.
- local transcript는 원 영상 binding과 생성 출처가 별도 검증되기 전 `UNVERIFIED`다. `TRANSCRIPT_READY_IS_NOT_FACT_OR_PROJECT_FIT_PASS`: caption ingest 성공도 발언의 사실성·프로젝트 적합성·Base 흡수 승인이 아니다.
- 내용 증거를 확보한 뒤 `PROJECT_REUSE_OPPORTUNITY_SCAN`과 현재 owner 비교로 `ADOPT / ADAPT / REJECT`를 판정한다. 제목·검색 스니펫·주변 자료를 본문 대신 사용하지 않는다.

'''


def write_final_artifacts() -> None:
    tracked = subprocess.run(
        [
            "git",
            "diff",
            "--",
            str(runner.INTAKE_PATH.relative_to(ROOT)),
            str(runner.CAPABILITY_PATH.relative_to(ROOT)),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if tracked.returncode != 0:
        raise RuntimeError(tracked.stdout)

    new_test = subprocess.run(
        [
            "git",
            "diff",
            "--no-index",
            "--",
            "/dev/null",
            str(runner.TEST_PATH.relative_to(ROOT)),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if new_test.returncode not in {0, 1}:
        raise RuntimeError(new_test.stdout)

    task_diff = tracked.stdout + new_test.stdout
    (runner.CANDIDATE / "task.diff").write_text(task_diff, encoding="utf-8")

    digest_lines: list[str] = []
    for path in (
        runner.CANDIDATE / "skills/managing-project-intake-and-work-contract/SKILL.md",
        runner.CANDIDATE / "docs/CAPABILITY_COMPOSITION_MAP.md",
        runner.CANDIDATE / "tests/test_ai_solution_layer_selection_contract.py",
        runner.CANDIDATE / "task.diff",
    ):
        digest_lines.append(
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT)}"
        )
    (runner.CANDIDATE / "sha256.txt").write_text(
        "\n".join(digest_lines) + "\n", encoding="utf-8"
    )

    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    (runner.CANDIDATE / "status.txt").write_text(status.stdout, encoding="utf-8")


runner.write_final_artifacts = write_final_artifacts
raise SystemExit(runner.main())
