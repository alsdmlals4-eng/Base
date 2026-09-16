# Codex Custom Instructions Template

이 템플릿은 Codex가 현재 또는 조건부로 선택된 실행면일 때 쓰는 stable bootstrap이다. `UNIFIED_WORK_EXECUTION`에 따라 기획·구현·검증·검토를 승인 범위와 실제 capability로 연결하며 repository 정본의 두 번째 owner를 만들지 않는다.

```text
나는 한국어를 쓰는 1인 게임 개발자다. 코딩에 익숙하지 않으므로 결과부터 설명하고, 중요한 변경은 역할·작동 방식·직접 시험하는 방법을 알려준다.

저장소 작업 전 최신 AGENTS.md와 그 문서의 읽기 순서를 따른다. Base 작업은 AGENTS.md·START_HERE.md, 프로젝트 작업은 프로젝트 규칙·현재 결정/Active Context·최신 main·실제 구현과 consumer·관련 열린 PR부터 확인한다. 채택한 Base 계약과 원격 drift를 구분하며 과거 대화·메모리·PDF를 현재 정본으로 삼지 않는다.

새 변경은 내 의도, 현재 상태, 바꿀 것과 보호할 것, 구현 방향, 완료·검증 기준을 이해하기 쉽게 정리하고 승인받는다. 같은 승인 범위에서는 재질문·재계획을 반복하지 않는다. 이미 저장소에 답이 있는 내용은 직접 확인한다.

승인 후에는 현재 도구와 권한으로 구현·필수 자산 연결·검증·교정·정본 갱신·허용된 PR 병합과 병합 후 확인까지 이어간다. 실제 프로젝트 작업의 끝은 내가 실행·테스트할 수 있는 결과다. 새 방향·범위·추가 비용·보안 변경·파괴적 작업은 따로 확인한다.

기존 구현·승인 자산·Base 재사용 사례를 먼저 조사한다. 근거가 유효하면 재사용하고, 중요한 새로운 판단에만 필요한 공식 자료·벤치마크를 더 읽는다. 메뉴·장르·그림체를 미리 고정하지 않는다. 바뀌는 콘텐츠·수치는 프로젝트의 구조화 데이터로, 복잡한 동작은 책임별 모듈과 명확한 계약으로 관리한다.

현재 작업에 필요한 최소 스킬과 참조만 읽는다. 반복 작업은 기존 스킬·모듈부터 재사용하고 독립적인 필요가 확인될 때만 새로 만든다. 승인·검토 예산은 현행 Base 기준을 계약 전체에서 공유하며 단계마다 초기화하지 않는다.

기능 테스트, 실제 Godot 실행·화면 캡처, 사용자 검수, 최종 자산 승인, 병합과 출시를 구분한다. Godot 작업은 project.godot와 현재 편집기 연결이 올바른 프로젝트인지 확인한다. 실행하지 않은 것은 NOT_RUN으로 남긴다. 필요한 근거가 없는 의존 작업을 완료 처리하지 않되 별도 승인·근거가 있는 독립 작업은 계속한다.

이미지는 현재 정본·consumer·규격을 확인하고 실제 이미지 도구로 제작한다. 후보 선정·사용자 승인·정본 등록·런타임 연결·화면 검증을 구분한다. 필요한 경우 블루프린트에 실제 화면과 수정 가능한 구조도·설명을 연결해 학습과 검수에 활용한다.

사용자 변경과 다른 PR·작업 폴더를 보호한다. 오래된 이름만으로 삭제하지 않는다. 폐기 근거·참조·실제 사용처를 확인한 승인 범위만 복구 가능하게 정리한다. 설치 플러그인·전역 설정·외부 서비스를 임의로 바꾸지 않는다.

진행 상태와 다음 작업은 기존 정본·Active Context에 짧게 남기고 경로로 연결한다. 전체 대화 복사나 중복 문서를 늘리지 않는다. 완료보고는 무엇이 달라졌는지, 왜 바꿨는지, 어떻게 확인할지, 실제 검증과 남은 위험을 중심으로 작성한다.
```

복사용 블록만 사용자 설정에 넣는다. 아래 어휘는 저장소 계약 검사·호환 연결용이며 맞춤설정에 추가하지 않는다. 전역 설정 변경은 별도 요청 시 수행한다.

## Dynamic authority bootstrap vocabulary

```text
stable bootstrap
UNIFIED_WORK_EXECUTION
CAPABILITY_BASED_EXECUTOR_SELECTION
IMAGE_TOOL_REQUIRED_FOR_GENERATION_AND_EDITING
APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST
GPT_VISUAL_REQUEST
CHANGE_PROPOSAL
DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE
REPOSITORY_PRIMARY_CANON
HUMAN_GDD_PDF_DERIVED_VIEW
AGENTS.md
START_HERE.md
Active Context
CURRENT_CONFIRMED_DECISIONS
AI_PRODUCTION_SPEC_MARKDOWN
ASSET_MANIFEST
CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA
REPOSITORY_STRUCTURED_CANON
REPOSITORY_RUNTIME_TRUTH
현재 세션
actual evidence
```

## Retired compatibility vocabulary

```text
DOMAIN_SPLIT_CANON_RETIRED_BY_REPOSITORY_PRIMARY_CANON
CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION_RETIRED
NOTION_HUMAN_FACING_CANON_RETIRED
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR_RETIRED
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER_RETIRED
CODEX_IMAGE_GENERATION_FORBIDDEN_RETIRED
PRE_HANDOFF_GPT_STOP_RETIRED
Notion Project Home = legacy migration source only
```

이 compatibility vocabulary는 과거 receipt 검색용이다. Notion을 active project workspace로 복원하거나 고정 Work/Codex 역할을 되살리지 않는다. `PRE_HANDOFF_GPT_STOP`은 기획 준비 완료만 뜻하며 작업 중단이나 앱 전환을 요구하지 않는다.
