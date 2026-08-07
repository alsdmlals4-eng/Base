# Handoff

공용 실행·동기화 기준: `docs/ONE_CLICK_PLAY_HANDOFF_POLICY.md`

## 인수 시점 상태

## 완료한 작업과 증거

## 미완료 작업·차단 요소

## GitHub 전달·로컬 갱신

```yaml
repository:
branch:
commit SHA:
working_tree_expectation: CLEAN | USER_CHANGES_PRESERVED
update_steps:
  - GitHub Desktop에서 올바른 repository·branch 선택
  - Fetch origin
  - Pull origin
  - 로컬 HEAD와 전달 commit SHA 일치 확인
```

`Fetch origin → Pull origin` 순서를 구분한다. Fetch만 수행한 상태는 로컬 파일 적용 완료가 아니다.

## 기본 실행 인계

- 프로젝트 파일:
- 기본 실행: `Project Play`
- 기대 첫 화면:
- 대표 플레이 흐름: 시작 → 실제 gameplay → 성공·실패·복귀
- 핵심 조작:
- 별도 Scene 선택·편집기 수동 설정 필요 여부: `없음`이어야 함
- 자동 검증:
- 수동 검수: `NOT_RUN / PASS / FAIL · RETEST_REQUIRED / BLOCKED`
- 알려진 문제:

## 다음 작업자의 첫 행동

## 변경하면 안 되는 결정·경로

## 읽기 순서

## 실행·미실행 검증

장문 기획과 수치는 책임 원본에 남기고 이 문서에는 상태·위험·다음 행동만 기록한다. 패키징·export PASS는 실제 Project Play의 화면·입력·완주 PASS를 대체하지 않는다.
