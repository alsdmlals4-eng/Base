# DeepSeek 대용량 작업 패키지

## 1. 작업 식별

- 작업명:
- 프로젝트:
- 기준 브랜치:
- 시작 커밋:
- worktree 경로:
- 작업 브랜치:
- 책임 검수자:

### 1.1 기계 검증 Sidecar

이 문서와 함께 `templates/ai/EXTERNAL_AI_WORKTREE_CONTRACT.json`을 복사해 실제 값으로 채운다.

```text
drafts/external-ai/<topic>/worktree-contract.json
```

외부 AI 작업 전과 결과 회수 후 아래 검사를 실행한다.

```bash
python tools/check_external_ai_worktree_contract.py \
  --root . \
  --contract drafts/external-ai/<topic>/worktree-contract.json
```

검사는 `.worktrees/` 무시 상태, 전용 `ai/deepseek-*` 브랜치, 시작 커밋 계보, 변경 경로 allowlist, 보호 경로, `REVIEW_PENDING` 상태, 정리 조건을 실제 Git 상태와 대조한다.

## 2. 목적과 사용자 가치

- 해결할 문제:
- 왜 대용량 외부 AI 작업이 필요한가:
- 사용자·플레이어에게 주는 가치:

## 3. 기준 입력

### 반드시 읽을 문서

1.
2.
3.

### 제공할 파일 allowlist

- 

### 보호 경로·금지 입력

- 비밀값·개인정보·권한 없는 원문:
- 읽지 말아야 할 archive·hold:
- 수정 금지 파일:

## 4. 작업 범위

- 수행할 초안·분류·변환:
- 작업 단위:
- 생성 가능한 경로:
- 수정 가능한 경로:

## 5. 제외 범위

- 기준 문서 최종 확정 금지.
- main·활성 작업 브랜치 직접 수정 금지.
- 구현 완료 판단 금지.
- 범위 밖 기능·리팩터링 금지.
- 출처 없는 최신 사실 확정 금지.

## 6. 고정 컨텍스트 접두부

아래 내용은 반복 요청에서 순서와 문구를 가능한 한 유지한다.

```text
역할:
프로젝트 규칙:
용어:
출력 스키마:
품질 기준:
금지 사항:
```

## 7. 가변 요청

```text
이번 작업 대상:
이번 산출물:
이번 예외:
```

## 8. 출력 계약

### Markdown 출력

```md
# 결과
## 확인한 입력
## 생성·수정 후보
## 초안
## 근거
## 가정
## 미확인
## Codex 검수 포인트
```

### 구조화 출력이 필요한 경우

```json
{
  "task": "",
  "source_files": [],
  "draft_items": [],
  "assumptions": [],
  "unverified": [],
  "review_points": []
}
```

모든 외부 AI 결과는 Sidecar의 `result_state: REVIEW_PENDING`을 유지한다. 실제 diff·근거·테스트를 책임 검수자가 확인하기 전에는 `APPROVED`, `VERIFIED`, `IMPLEMENTED`로 승격하지 않는다.

## 9. 자체 검수

- [ ] `.worktrees/`가 Git에서 무시된다.
- [ ] worktree와 `ai/deepseek-*` 전용 브랜치가 기준 브랜치와 분리됐다.
- [ ] allowlist 밖 파일을 사용하지 않았다.
- [ ] 보호 경로를 수정하지 않았다.
- [ ] 사실·가정·제안을 구분했다.
- [ ] 기존 원본을 새 파일로 중복하지 않았다.
- [ ] 가짜 경로·ID·명령을 만들지 않았다.
- [ ] 결과가 출력 계약을 따른다.
- [ ] 완료를 주장하지 않고 검수 포인트를 남겼다.
- [ ] `check_external_ai_worktree_contract.py`가 `PASS`하고 `RESULT_STATE: REVIEW_PENDING`을 출력했다.

## 10. Codex 인계

- 변경 후보 파일:
- 가장 위험한 가정:
- 표본 검사가 필요한 항목:
- 전체 검사가 필요한 항목:
- 폐기해도 되는 초안:
- worktree 정리 조건:

worktree 정리는 Sidecar의 `integration_state`가 `APPROVED_INTEGRATED`이고 작업 트리가 clean인 경우에만 요청한다. dirty 상태나 미통합 결과가 있으면 `cleanup_requested: false`로 보존한다.
