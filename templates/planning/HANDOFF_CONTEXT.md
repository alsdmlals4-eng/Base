# 기획 인수인계 컨텍스트 템플릿

> 작성 방법: `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`

이 문서는 전체 기획서를 복제하지 않는다. 새 채팅, 새 AI, 새 작업자가 프로젝트의 현재 상태와 책임 원본을 빠르게 찾도록 연결하는 라우터다.

## 1. 프로젝트 한 줄 정의

> 

- 핵심 플레이어 경험:
- 현재 가장 중요한 세일즈포인트:

## 2. 현재 상태

```yaml
status:
implemented_baseline:
verified_baseline:
base_version:
version:
branch_or_workspace:
completed:
in_progress:
approved_but_not_implemented:
blocked:
unverified:
```

## 3. 핵심 불변 조건

-
-
-

## 4. 기본 읽기 순서

```text
프로젝트 AGENTS.md
→ BASE_RULES_VERSION.md와 Base 로컬 사본
→ Documentation Map
→ 이 Active Context·Handoff
→ 프로젝트 방향·전체 기획서
→ 분야별 책임 기획서
→ Roadmap
→ 현재 Issue·Goal·Plan
→ 프로젝트 skill extension
→ 실제 대상 파일과 테스트
```

## 5. 책임 원본

| 질문 | 문서·파일 | 상태 | 최종 갱신 |
|---|---|---|---|
| 현재 무엇이 작동하는가? |  |  |  |
| 왜 이 방향인가? |  |  |  |
| 핵심 플레이어 경험은? |  |  |  |
| 분야별 표현·시스템 기준은? |  |  |  |
| 현재 단계와 다음 순서는? |  |  |  |
| 반복 작업에 사용할 스킬은? |  |  |  |
| 완료 판단은? |  |  |  |
| 과거 근거와 사례는? |  |  |  |

## 6. Roadmap 연결

- 현재 단계:
- 현재 우선순위:
- 선행 조건:
- 다음 마일스톤:
- 단계 종료 기준:
- 검증 방법:
- Roadmap 경로:

## 7. 다음 작업

- 작업명:
- 목표:
- 사용자 가치:
- 진입 기준:
- 작은 수직 단위:
- 제외 범위:
- 종료 기준:
- 관련 Issue·Goal·Plan:

## 8. 적용 스킬

| 작업 | Base skill | Project extension | 입력 원본 | 검증 |
|---|---|---|---|---|
|  |  |  |  |  |

## 9. 보호 경로·고위험 영역

- 저장·진행:
- 데이터 ID:
- 경제·결제:
- 외부 API·보안:
- UI·입력:
- 사용자 변경:

## 10. 실제 파일 위치

| 역할 | 경로 |
|---|---|
| 상태·도메인 로직 |  |
| 데이터 |  |
| UI·씬 |  |
| 아트·에셋 |  |
| 테스트 |  |
| 문서 |  |

## 11. 차이와 확인 필요

| 항목 | 기획 | 실제 구현 | 영향 | 처리 |
|---|---|---|---|---|
|  |  |  |  |  |  |

## 12. 검증

- 자동:
- 수동:
- 최소 해상도·입력:
- 저장·복귀:
- 사용자 확인:
- 실행하지 못한 검증:

## 13. Base 학습 환류

### 프로젝트 전용으로 남길 내용

-

### Base method·research·skill·template 반영

-

### 작성·갱신한 사례

| 사례 | 상태 | 검증 근거 | 후속 검증 |
|---|---|---|---|
|  | 관찰/가설/채택/패턴/검증 |  |  |

공용화할 내용이 없으면:

> 공용 학습 데이터 없음 — 프로젝트 전용 또는 단발성 작업

## 14. 과거 자료

- 백업 인덱스:
- 정확한 과거 원문 찾기:
- 기본 읽기에서 제외할 문서:

## 15. 콜드 스타트 검수

새 작업자가 10분 안에 다음을 찾을 수 있는가?

- [ ] 핵심 플레이어 경험과 현재 방향
- [ ] 현재 단계와 최우선 작업
- [ ] 다음 작업의 선행 조건과 종료 기준
- [ ] 변경하면 안 되는 범위
- [ ] 질문별 책임 기획서
- [ ] 적용할 Base skill과 프로젝트 extension
- [ ] 실제 데이터·파일·테스트 경로
- [ ] 승인·구현·검증·미확정 상태
- [ ] 작업 종료 시 Base 환류 대상

## 16. 완료 뒤 갱신

- [ ] 프로젝트 방향·전체 기획서
- [ ] 분야별 책임 기획서
- [ ] Roadmap
- [ ] 프로젝트 skill extension
- [ ] 현재 상태와 Active Context·Handoff
- [ ] Documentation Map·README
- [ ] Issue·Goal·Plan
- [ ] 테스트·QA 기록
- [ ] Base method·skill·template
- [ ] 공용 사례와 지식 상태
- [ ] BASE_RULES_VERSION과 로컬 사본 동기화
