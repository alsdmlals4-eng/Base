# 공용 학습형 기획 지식 베이스

여러 프로젝트에서 재사용할 수 있는 **기획·서사·아트·연출·조사·검수 방법과 일반화된 사례**를 학습 데이터로 관리한다.

Base 작업 규칙이 “어떻게 협업할 것인가”를 정의한다면, 이 폴더는 “무엇을 관찰하고 어떤 순서로 판단하며 무엇으로 검증하고, 프로젝트 결과를 어떻게 다음 작업의 공용 지식으로 환류할 것인가”를 정의한다.

## 1. 학습형의 의미

Base의 지식은 고정된 정답 모음이 아니다. 프로젝트 작업과 벤치마킹에서 얻은 관찰, 성공, 실패, 수정 과정과 검증 결과를 누적해 기존 method·skill·template을 개선하는 **공용 학습 데이터**다.

```text
공용 방법·스킬
→ 프로젝트별 전용 규칙으로 분화
→ 실제 작업·테스트·플레이 검증
→ 성공·실패·미검증 사례 기록
→ 공용 원리와 프로젝트 고유 값 분리
→ Base 지식 상태·method·skill·template 갱신
```

- 사례는 학습의 입력이다.
- method는 반복 가능한 판단 순서다.
- skill은 직접 실행 가능한 작업 계약이다.
- template은 재사용 가능한 출력 구조다.
- 프로젝트는 공용 지식을 실제 조건에서 시험하고 전용으로 발전시키는 검증 공간이다.

## 2. 구조

```text
docs/knowledge/
├─ methods/   반복 가능한 판단·설계 방법
├─ research/  정보 수집·벤치마킹·표준·근거 평가
├─ skills/    분야별 입력·산출물·검수 능력 계약
└─ cases/     프로젝트·벤치마킹에서 추출한 성공·실패·미검증 사례
```

직접 실행 가능한 단계형 스킬은 루트 `skills/`에 둔다. `docs/knowledge/skills/`에는 여러 관련 작업을 한눈에 보는 역량 지도와 검수 기준을 둔다.

## 3. Base와 프로젝트 책임 경계

### Base — [학습형] [공용]

- 여러 프로젝트에서 재사용 가능한 방법과 체크리스트
- 출처와 권리를 확인한 조사·표준 참고
- 프로젝트 사례에서 일반화한 성공·실패·검증 교훈
- 새 프로젝트가 분화해 사용할 템플릿과 실행 스킬
- 지식 상태, 적용 조건, 실패 조건과 후속 검증

### 프로젝트 — [전용] [분화·적용·검증]

- 세계관, 캐릭터, 밸런스, 실제 수치와 파일 경로
- 현재 로드맵, 구현 상태, Issue·Goal·Plan
- 프로젝트 전용 아트·사운드·데이터·테스트
- 실제 모델·계정·비용·원본 자산·승인 프롬프트
- Base 스킬을 구체화한 프로젝트 전용 확장
- 공용화 전의 관찰·가설·실험과 실제 결과

사례에는 프로젝트 이름과 공개 가능한 맥락을 표시할 수 있지만 활성 기획서 전체를 복제하지 않는다. 프로젝트의 구체 해답은 프로젝트에 남기고, 반복 가능한 판단과 검증 교훈만 일반화한다.

## 4. 지식 상태

| 상태 | 의미 | Base 반영 범위 |
|---|---|---|
| `관찰` | 사례에서 발견했으나 채택 전 | case 중심 |
| `가설` | PoC·테스트 필요 | case·research 중심 |
| `채택` | 한 프로젝트에서 사용 결정 | 프로젝트 전용, 필요 시 case |
| `패턴` | 같은 조건에서 반복 재현 | method·template 보완 가능 |
| `검증` | 실제 작업·플레이테스트로 효과 확인 | 공용 rule·method·skill 승격 가능 |
| `제외` | 현재 조건에 맞지 않음 | 제외 이유를 case에 보존 |
| `폐기` | 더 나은 기준으로 대체 | 대체 경로와 Git 이력 보존 |

문서와 스킬이 존재한다는 사실만으로 `검증` 상태가 되지 않는다. 모델·서비스·버전에 의존하는 기술은 확인 조건과 날짜를 함께 기록한다.

한 번 성공한 방법은 먼저 case로 남긴다. 확정 rule·method·skill로 승격하려면 사용 조건, 비사용 조건, 실패 기준, 재현 절차와 실제 검증 근거가 필요하다.

## 5. 작업 시작 시 지식 확인

프로젝트 작업을 시작할 때는 현재 작업에 적용되는 다음 공용 정보를 확인한다.

- 관련 Base 작업 규칙
- 해당 분야 method·research
- 실행 skill과 검수 matrix
- 사용할 template
- 유사 case와 실패 사례

그 후 프로젝트의 `AGENTS.md`, Base 버전, Documentation Map, Active Context·Handoff, 기획서, Issue·Goal·Plan과 실제 영향 파일을 확인한다.

`공용 정보와 프로젝트 정보를 전부 확인한다`는 것은 저장소 전체를 무차별적으로 읽는다는 뜻이 아니다. Documentation Map과 참조 관계로 현재 작업에 적용되는 공용·전용 책임 원본의 범위를 정하고, 그 범위 안의 문서와 영향 파일을 빠짐없이 확인한다.

## 6. 라우팅

| 작업 | 먼저 읽을 문서 |
|---|---|
| 전체 기획 체계 | `methods/PLANNING_SYSTEM_METHOD.md` |
| 인수인계 | `methods/PROJECT_HANDOFF_CONTEXT_METHOD.md` |
| 서사·관계 | `methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md` |
| 아트 | `methods/ART_DIRECTION_METHOD.md` |
| 캐릭터·서사 아트 | `methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md` |
| AI 이미지 프롬프트·디자인 기술 | `methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md` |
| 애니메이션·전투 연출 | `methods/ANIMATION_AND_PRESENTATION_METHOD.md` |
| 대화·이벤트 연출 | `methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md` |
| 조사·벤치마킹 | `research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md` |
| 외부 AI·프롬프트 공식 자료 | `research/AI_WORKFLOW_AND_PROMPT_SOURCE_NOTES.md` |
| 딥인터뷰 외부 소스 감사 | `research/OUROBOROS_DEEP_INTERVIEW_SOURCE_AUDIT.md` |
| FACS 표정 제어 참고 | `research/FACS_ACTION_UNIT_PROMPT_REFERENCE.md` |
| 기획·조사·인수 능력 | `skills/PLANNING_RESEARCH_HANDOFF_SKILL_MATRIX.md` |
| 아트·프롬프트 능력 | `skills/ART_DIRECTION_SKILL_MATRIX.md` |
| 사례 | `cases/README.md` |

실행 스킬:

- 요청 변환: `../../skills/transforming-requests-into-prompts/SKILL.md`
- 요구 딥인터뷰: `../../skills/conducting-deep-requirement-interviews/SKILL.md`
- Vertical Slice: `../../skills/designing-vertical-slices/SKILL.md`
- 기획서 작성: `../../skills/writing-game-design-documents/SKILL.md`
- DeepSeek·외부 AI worktree: `../../skills/orchestrating-deepseek-worktrees/SKILL.md`
- 외부 AI 초안 검수: `../../skills/reviewing-external-ai-drafts/SKILL.md`
- 아트 프롬프트·기술 카드: `../../skills/designing-art-prompts-and-technique-cards/SKILL.md`
- 지식 승격: `../../skills/promoting-project-knowledge/SKILL.md`

십보강호에서 승격한 적용 사례:

- 규칙·UI·연출·QA 추적성: `cases/TEN_PACES_RULE_PRESENTATION_TRACEABILITY_CASE.md`
- 선택적 하이라이트와 정상 완주 경로: `cases/TEN_PACES_OPTIONAL_HIGHLIGHT_VERTICAL_SLICE_CASE.md`
- 내부 데이터의 세계관 문구 변환: `cases/DIEGETIC_OPPONENT_INFORMATION_CASE.md`

세 사례는 문서 구조와 기획 채택을 근거로 하며 실제 구현·플레이 검증 전이다. 따라서 검증 완료된 공용 규칙이 아니라 적용 조건과 후속 검증을 가진 학습 사례로 사용한다.

## 7. 아트 프롬프트 지식 운영

```text
프로젝트 사용 목적
→ 기술 카드와 프롬프트 가설
→ 원본·모델·조건을 기록한 시험
→ 성공·실패·수정 사례
→ 실제 화면·현지화 QA
→ 프로젝트 패턴
→ 반복 검증 뒤 Base method·skill 보완
```

- AU 번호, 모델 태그, 스타일 키워드는 자연어 목적과 보호 조건을 대체하지 않는다.
- 생성 이미지의 글자·로고는 최종 의미 텍스트와 분리한다.
- 캐릭터 포스터는 메인 일러스트와 정보 슬롯을 독립적으로 수정 가능하게 만든다.
- 한 번 성공한 프롬프트는 먼저 사례 또는 가설로 기록한다.

관련 사례:

- `cases/FACS_EXPRESSION_EDITING_PROMPT_CASE.md`
- `cases/CHARACTER_PROMO_POSTER_LAYOUT_CASE.md`

## 8. 작업 종료·인수인계 시 학습 환류

작업 종료와 인수인계에서는 다음 순서로 정리한다.

```text
프로젝트 결과 확인
→ 프로젝트 전용 기준 문서와 Active Context 갱신
→ 공용으로 재사용할 데이터 추출
→ 기존 Base 책임 원본과 중복·충돌 확인
→ method·research·skill·template 갱신
→ 성공·실패·미검증 case 작성
→ 지식 상태 갱신
→ Base 버전과 프로젝트 로컬 사본 동기화
```

반드시 구분해 기록한다.

- 프로젝트 전용으로 남긴 세계관·수치·경로·자산·구현 상태
- Base 기획서·method·skill·template에 반영한 공용 데이터
- 새로 작성하거나 상태를 갱신한 사례
- 아직 검증되지 않아 `관찰`·`가설`로 남긴 내용
- 다음 프로젝트에서 재검증할 조건

공용화 가능한 내용이 없으면 Base를 억지로 수정하지 않는다. 이 경우 `공용 학습 데이터 없음 — 프로젝트 전용 또는 단발성 작업`으로 인수인계에 기록한다.

## 9. 프로젝트에서 Base로 승격

```text
프로젝트 문제
→ 프로젝트 전용 해결
→ 실제 검증
→ 고유 정보와 공용 원칙 분리
→ 기존 책임 문서와 중복·충돌 확인
→ 적절한 지식 유형으로 반영
→ 사례와 지식 상태 갱신
→ 프로젝트 로컬 사본·버전 동기화 확인
```

분류:

- 반복되는 작업 규칙: `AGENTS.md` 또는 작업 규칙
- 판단 순서와 설계법: `methods/`
- 조사와 근거 평가: `research/`
- 직접 실행할 절차: 루트 `skills/`
- 분야별 역량 지도: `docs/knowledge/skills/`
- 복사 가능한 산출물: `templates/`
- 구체 문제와 결과: `cases/`

상세 절차는 `skills/promoting-project-knowledge/SKILL.md`를 따른다.

## 10. 사례 필수 항목

- 출처와 확인 날짜
- 해결할 문제와 제약
- 관찰한 근거
- 검토한 대안
- 결정과 이유
- 결과와 미검증 항목
- 실패·수정 과정
- 재사용 가능한 원칙
- 그대로 복사하면 안 되는 프로젝트 특화 요소
- 현재 지식 상태
- 후속 검증 조건

`templates/KNOWLEDGE_CASE_STUDY.md`를 사용한다.

## 11. 프로젝트 전용 스킬·AI 프로필

프로젝트가 Base 스킬을 확장할 때 전체 스킬을 복제하지 않는다.

다음만 기록한다.

- 적용 Base 스킬과 기준 버전
- 프로젝트 추가·대체 규칙
- 실제 문서·데이터·파일 경로
- 프로젝트 전용 완료 기준과 테스트
- 프로젝트 검증 결과와 Base 환류 여부

템플릿:

- 스킬 확장: `templates/skills/PROJECT_SKILL_EXTENSION.md`
- GPT·DeepSeek·Codex 역할: `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md`
- DeepSeek 대량 작업: `templates/ai/DEEPSEEK_WORK_PACKAGE.md`
- 외부 AI 결과 검수: `templates/ai/EXTERNAL_AI_DRAFT_REVIEW.md`

## 12. 품질 원칙

- 추상 조언보다 입력, 산출물, 실패 기준, 검증을 남긴다.
- “멋있게”, “자연스럽게”, “최고로”를 관찰 가능한 기준으로 변환한다.
- 사례의 표면이 아니라 문제 해결 원리를 기록한다.
- 저작권이 있는 코드·아트·문구·UI를 복제하지 않는다.
- 바뀔 수 있는 외부 사실과 모델 기능은 출처·버전·확인일을 남긴다.
- 외부 AI 산출물은 실제 diff·근거·테스트 확인 전까지 검수 대기 입력이다.
- 같은 규칙은 하나의 책임 문서에서 관리한다.
- 오래된 내용은 Git 이력으로 보존한다.
