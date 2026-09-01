# Base 활성 작업면 정리·프로젝트 시작 게이트 설계

> 상태: CURRENT_TASK_APPROVED
> 기준 Base main: 781dfe8faf0da26c04abb437ae68f94db2cb106b
> 범위: 활성 Skill·작업 라우팅 연결 검증, 프로젝트 L1+ receipt 경유, 실제로 대체된 역사 감사의 Archive 격리, 활성 엔진 정책의 V4 workspace authority 정합성

## 작업 전 문제

Base에는 L1+ benchmark/역공학 receipt와 legacy context hygiene가 이미 Skill, 시작 체크리스트, validator에 존재한다. 그러나 프로젝트의 가장 이른 사람용 시작점과 AI workflow, route resolver가 같은 기계 검증 진입점을 모두 명시하지 않아, 프로젝트가 Base를 채택했어도 시작 순서를 놓칠 가능성이 있었다.

또한 docs/audits의 2026-07-19 schema-v3 전환 감사 두 건은 현재 운영 owner가 아니라 당시 PR #8~#10의 검증 증거다. 일반 docs 경로에 남아 있어 현재 자료로 오인할 여지가 있지만, 원문과 rollback commit은 보존 가치가 있다.

적대적 검토 중 활성 `ENGINE_BASELINE_AND_ADAPTER_POLICY.md`가 Godot engine 선택에는 유효한 최신 기준을 유지하면서도, 작업면 설명에서 V3 `NOTION_HUMAN_FACING_CANON`과 `DOMAIN_SPLIT_CANON`을 현행으로 선언하는 충돌이 발견됐다.

## 조사·비교 결과

| 방식 | 판정 | 이유 |
|---|---|---|
| 날짜·버전명만 보고 삭제 | REJECT | 활성 consumer, 호환성, 고유 검증 근거를 잃을 수 있다. |
| 모든 구형 자료를 active docs에 유지 | REJECT | 기본 fresh-read와 token budget에 불필요한 과거 문맥이 섞인다. |
| 현재 owner·consumer를 확인한 뒤 history/evidence를 Manifest Archive로 이동 | ADOPT | 기본 작업면에서 분리하면서 원문 hash, rollback, 재감사 근거를 보존한다. |
| 프로젝트마다 공용 Skill 본문·validator를 복사 | REJECT | Base와 프로젝트 사이에 두 번째 공용 정본을 만든다. |
| project adapter pin으로 확인한 Base tool을 실행하고, receipt는 프로젝트 저장소에 소유 | ADOPT | 공용 검증 로직은 하나로 유지하고 프로젝트 사실·증거는 프로젝트가 소유한다. |

직접 비교한 현행 Base pattern은 다음이다.

- skills/SKILL_REGISTRY.json은 활성 Skill 30개를 단일 route owner로 둔다.
- skills/BASE_SHARED_SKILL_ROUTES.json은 필요한 두 extension route만 project adapter로 연결한다.
- WORK_PROJECT_START_CANON_CHECKLIST와 validate_work_contract_receipt.py는 L1+ preflight의 실제 필드·실패 조건을 이미 fail-closed로 정의한다.
- docs/archive/ARCHIVE_MANIFEST.json과 2026-07-30 무결성 감사는 archive 원문 hash·rollback·active_authority=false 방식의 검증된 선례다.

## 채택 구조와 이유

모든 프로젝트 L1+ 작업은 다음의 좁은 순서로 연결한다. 이 순서는 Project Start Here, AI workflow, current router, base project router뿐 아니라 기본 Work→Codex starter에도 동일하게 적용된다.

```text
Project AGENTS와 exact project state fresh-read
→ PROJECT_BASE_ADAPTER pin/route validation
→ WORK_PROJECT_START_CANON_CHECKLIST
→ project-repository-owned benchmark_preflight_receipt + hygiene inventory
→ exact pinned Base root의 validate_work_contract_receipt.py 실행
→ PASS 또는 material drift 없는 REUSED_EVIDENCE
→ 기획·시안·구현
```

Base tool 경로를 프로젝트의 임의 relative tools 경로로 가정하지 않는다. adapter가 확인한 exact Base pin과 일치하는 Base checkout을 해석하지 못하면 BLOCKED_UNVERIFIED로 멈춘다. receipt 자체는 프로젝트 정본의 evidence로 남기며 Base가 프로젝트의 장르, 메뉴, 버튼, 세계관이나 soft-coded 값을 고정하지 않는다.

역사 감사는 삭제 대신 다음 lifecycle으로 처리한다.

```text
docs/audits의 historical evidence
→ docs/archive/audits의 EVIDENCE_RETENTION 원문
→ Archive Manifest의 SHA-256·rollback ref·대체 current owner
→ 기본 fresh-read 제외
```

## 범위와 제외

포함:

- 프로젝트 시작점, AI workflow, 현재 실행 router, base project router, 기본 Work→Codex starter, shared adapter contract의 receipt gate 연결.
- Intake request metadata와 validator가 실행하는 root receipt JSON의 구조 분리 및 실제 예시 회귀 검증.
- schema-v3 read-only/final audit 원문 두 건의 Archive 이동과 internal reference 교정.
- Godot baseline·adapter 선택은 보존하면서, active engine policy의 workspace authority 설명을 V4 repository-first로 교정.
- archive와 project routing의 회귀 검증.

제외:

- 구형 v7/v8 prompt, v1 schema, compatibility appendix처럼 현재 테스트나 consumer가 있는 자료의 삭제.
- 프로젝트별 Base pin을 일괄 갱신하거나 프로젝트 코드·세계관·UI를 변경하는 작업.
- open PR takeover, direct main push, force push, 규칙 우회.

## 완료 증거

- 새 archive entry가 source path 부재, destination body SHA, active_authority=false, implementation_authority=NONE을 함께 검증한다.
- 모든 프로젝트 시작 entrypoint가 L1+ receipt의 source, checklist, exact pinned Base validator를 경유한다.
- receipt validator, targeted regression, reference freshness, generated artifact checks, full regression, GitHub required checks와 merge readback을 순서대로 확인한다.
