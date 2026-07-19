# GitHub Actions Node 20 deprecation 증거

## PR #13

- PR: `https://github.com/alsdmlals4-eng/Base/pull/13`
- Run: `https://github.com/alsdmlals4-eng/Base/actions/runs/29688361894`
- Head: `6e8057007a8cf96e7673bc411f645f12217bc689`
- 결과: `validate-operating-system`, `validate-publications-windows`, `validate-whitespace` 모두 성공

Run annotation은 다음 Action들이 Node.js 20을 대상으로 하지만 Node.js 24에서 강제 실행된다고 보고했다.

- `actions/checkout@v4`
- `actions/setup-node@v4`
- `actions/setup-python@v5`
- `actions/upload-artifact@v4`

경고가 가리킨 공식 공지:

`https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/`

이 증거는 성공한 Workflow를 즉시 변경하라는 승인 근거가 아니다. 호환 major와 migration note를 확인할 후속 검토 근거다.
