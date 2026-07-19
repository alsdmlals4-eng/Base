# BCP-2026-002 — GitHub Actions Node 24 호환 버전 전환

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `c85e40855400a7595bf8b1350cba53a0e3c7e94d`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`

## 관찰과 증거

PR #12와 PR #13의 GitHub Actions는 전부 성공했지만, `actions/checkout@v4`, `actions/setup-node@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4`가 Node.js 20을 대상으로 하며 runner에서 Node.js 24로 강제 실행된다는 deprecation annotation을 반복해서 출력했다.

- PR #13 Actions run: `29688361894`
- Linux·Windows·whitespace job: 모두 성공
- 공식 경고 링크: `https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/`
- 원문과 job별 위치: [ACTIONS_WARNINGS.md](evidence/ACTIONS_WARNINGS.md)

현재 기능 실패는 아니므로 P0·P1이 아니라 P2 유지보수 제안이다.

## 일반화 후보

GitHub 공식 Action을 Node.js 24 호환 major로 전환하고, Action major·runner 변경 경고를 Base Health Review의 유지보수 신호로 검사한다. 구현 시점의 공식 release와 migration note를 다시 확인하며 단순 문자열 일괄 교체는 하지 않는다.

## 적용 조건과 비사용 조건

- 적용: 사용 중인 각 공식 Action에 Node.js 24 호환 안정 major와 공식 migration 안내가 존재하고, Linux·Windows job을 모두 재검증할 수 있을 때
- 비사용: 공식 호환 release가 아직 없거나 새 major가 현재 runner·입력 계약과 호환되지 않을 때

## 반례와 위험

- 최신 major가 입력 기본값, 캐시, 권한 또는 아티팩트 동작을 바꿀 수 있다.
- 한 Action만 올리면 annotation 일부가 남고 환경 차이가 커질 수 있다.
- 경고 제거만 목표로 검증되지 않은 commit SHA나 비공식 fork를 채택해서는 안 된다.

## 영향 범위와 검증

- 예상 영향: `.github/workflows/validate-game-project-operating-system.yml`, Workflow 유지보수 검사, 관련 문서
- 검증: Linux 전체 회귀, Windows 실제 발행 smoke, whitespace, artifact 업로드, checkout history depth, Node·Python setup 결과
- 보안: 공식 저장소 release와 immutable commit SHA 사용 여부를 구현 시 별도 결정
- 롤백: Action 버전 변경 커밋을 revert해 현재 성공한 major 조합으로 복구

## 승인과 구현

- 사용자 승인 근거: `미승인`
- 구현 PR: `없음`
