# 사례 — Work↔Codex Starter Prompt, Local Execution, Git Sync, Build Delivery

- 확인 날짜: 2026-08-27
- 상태: Base process-contract correction; project runtime evidence 없음
- 적용 owner: Work v4.9 minimum-transition profile과 현행 Git/local/Godot/Vertical Slice owner

## 문제

기능적으로 완전한 공용 실행 프로필이 있어도 사용자가 채팅에 수백 줄을 매번 복사하면 Base 변경 뒤 문구가 stale해지고 두 번째 정본이 생긴다. 반대로 프로젝트명 한 줄만 주면 사용자가 별도로 승인한 local computer control, 자동 Git 동기화, Notion 최초 감사, 다운로드 가능한 빌드 전달 같은 실행 권한이 복원되지 않을 수 있다.

## 대안 비교

1. 전체 계약을 매 채팅에 그대로 복제 — 즉시 읽히지만 길고 drift·중복·토큰 비용이 크므로 기각.
2. 프로젝트명만 전달 — 가장 짧지만 explicit delegation과 local/build 경계가 사라질 수 있어 불충분.
3. current Base profile을 fresh-read하도록 라우팅하는 짧은 starter + 사용자별 명시 위임·안전 경계 — 채택.

## 재사용 원칙

### `STARTER_PROMPT_SHOULD_ROUTE_CURRENT_OWNER`

사용자용 시작 프롬프트는 안정적인 의도·권한·예외만 담고, 상세 Work/Codex·Visual·Git·Godot·QA 절차는 current Base owner를 fresh-read한다. Base owner가 바뀌면 starter의 오래된 상세 복제보다 current owner가 우선한다.

### `SAFE_PULL_IS_NOT_BLIND_PULL`

`git pull`은 fetch 후 현재 branch에 통합하는 동작이므로 자동화 전에 dirty/divergence/upstream/worktree/owner 상태를 확인한다. 자동 경로는 `fetch --prune`과 clean·non-diverged 상태의 `pull --ff-only`다. divergence·dirty state를 force/reset/rebase로 덮지 않고 exact SHA와 intended delta를 보존해 reconcile한다.

### `LOCAL_CONTROL_IS_CAPABILITY_BOUNDED`

사용자 위임은 실제 callable tool이 있을 때 프로젝트 범위 Godot·terminal·game window 조작을 허용한다. 지시문만으로 computer tool이나 editor connection이 생기지는 않는다. exact project/session/process identity가 없으면 실행을 추측하지 않으며 unrelated application/file, credential, OS security, network exposure는 범위 밖이다.

### `DOWNLOADABLE_BUILD_IS_SEPARATE_FROM_PUBLIC_RELEASE`

내부 검증용 executable/ZIP과 GitHub Actions artifact는 사용자 플레이 전달 수단이다. Store, GitHub Release, 공개 배포는 별도 외부 publication이다. 내부 artifact는 exact build identity, SHA-256, clean-extract launch smoke와 durable locator를 가져야 하며 public release 권한을 자동 상속하지 않는다.

## 공식 자료에서 확인한 근거

- Git 공식 `git-pull` 문서는 pull이 먼저 fetch하고 현재 branch에 통합하며, `--ff-only`는 divergence에서 실패해 implicit history rewrite를 피하는 경로임을 설명한다.
- Godot 공식 command-line/export 문서는 project path·scene 실행, headless QA/export, export preset/template 기반 playable build 생성을 지원한다.
- GitHub 공식 workflow artifact 문서는 binary·log·screenshot 같은 workflow 산출물을 보존하고 다운로드하는 용도를 정의한다.
- GitHub auto-merge는 required review와 status check가 충족된 뒤에만 merge한다.

## Source locators

- Git pull: https://git-scm.com/docs/git-pull
- Godot command line: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Godot export: https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html
- GitHub workflow artifacts: https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
- GitHub auto-merge: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request

## 비사용 조건

- local/computer capability가 현재 host에 노출되지 않음
- 정확한 project path/editor session/process identity를 검증할 수 없음
- dirty/diverged worktree의 의미를 복원하지 못함
- export preset/template이 없거나 target platform이 미확정
- artifact upload route가 없는데 local path를 다운로드 링크로 가장하려는 경우
- public release, 계정 권한, 유료 비용, 법적 권리 판단이 필요한 경우

## Evidence ceiling

이 사례와 starter의 repository contract는 prompt discovery와 안전 경계를 검증한다. 실제 Git fetch/pull/push, Godot 실행, PC 조작, Notion audit, exported build, artifact 다운로드, Human/Player 경험은 프로젝트별 실행 evidence가 있어야 한다.
