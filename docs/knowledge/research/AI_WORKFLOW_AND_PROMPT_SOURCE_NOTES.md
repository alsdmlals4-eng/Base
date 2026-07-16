# AI 작업 구조·프롬프트 공식 자료 메모

- 상태: 공식 자료 기반 참고
- 최종 확인일: 2026-07-16
- 목적: 외부 AI worktree, 토큰·컨텍스트 효율, 구조화 출력, 프롬프트 모듈화 규칙의 근거와 재확인 위치를 기록한다.

## 1. Git worktree

공식 문서:

- Git `git-worktree`: https://git-scm.com/docs/git-worktree

확인한 원리:

- 하나의 저장소에 여러 working tree를 연결할 수 있다.
- 서로 다른 브랜치를 동시에 체크아웃해 병렬 작업공간으로 사용할 수 있다.
- linked worktree는 기준 저장소와 메타데이터를 공유하므로 작업 종료 시 상태를 확인하고 제거한다.

Base 적용:

- DeepSeek·외부 AI의 대량 초안은 main과 분리된 브랜치·worktree에서 수행한다.
- 같은 브랜치를 둘 이상의 worktree에서 임의로 공유하지 않는다.
- dirty·미통합 worktree는 자동 삭제하지 않는다.

## 2. DeepSeek context caching

공식 문서:

- Context Caching: https://api-docs.deepseek.com/guides/kv_cache

확인한 원리:

- API 요청의 이전 입력과 겹치는 접두부를 캐시 대상으로 사용할 수 있다.
- cache hit와 miss 사용량을 응답 usage에서 확인할 수 있다.
- 캐시는 best-effort이므로 항상 적중한다고 가정하지 않는다.

Base 적용:

- 공통 규칙, 예시, 출력 스키마를 안정적인 앞부분에 둔다.
- 작업마다 바뀌는 파일·질문·대상은 뒤쪽 가변 구역에 둔다.
- 캐시 적중은 비용 최적화 지표이며 정확성·보안 검증을 대체하지 않는다.

## 3. DeepSeek JSON output

공식 문서:

- JSON Output: https://api-docs.deepseek.com/guides/json_mode

확인한 원리:

- 구조화 결과가 필요할 때 JSON object 출력 모드를 사용할 수 있다.
- 프롬프트에 JSON 출력 의도와 원하는 구조의 예시를 명확히 포함해야 한다.
- 출력 토큰 한도와 후속 파싱 실패를 고려해야 한다.

Base 적용:

- 대량 데이터 카드·분류 결과는 고정 Markdown 또는 JSON 스키마로 회수한다.
- 결과가 비거나 잘린 경우를 대비해 스키마 검증과 재시도 조건을 둔다.
- 외부 AI가 만든 JSON도 실제 데이터 계약과 별도로 검수한다.

## 4. OpenAI prompt caching·프롬프트 구성

공식 문서:

- Prompt caching: https://platform.openai.com/docs/guides/prompt-caching
- Prompt engineering: https://platform.openai.com/docs/guides/prompt-engineering

확인한 원리:

- 반복되는 정적 내용은 프롬프트 앞부분에, 가변 내용은 뒤에 배치하는 구조가 캐시 재사용에 유리하다.
- 지시, 예시, 맥락을 Markdown 제목이나 XML 태그처럼 명확한 경계로 분리할 수 있다.
- 소수의 품질 높은 예시는 출력 형식을 안정시키는 데 사용할 수 있다.

Base 적용:

```text
Identity·Role
→ Stable Rules
→ Output Schema
→ Good Example
→ Project Context
→ Variable Task
```

- 긴 프롬프트는 같은 말을 반복하지 않고 책임 섹션으로 분리한다.
- 예시는 하나의 정확한 사례를 우선하고 잘못된 패턴은 실패 기준으로 분리한다.
- 캐시 효율보다 최신 사용자 지시와 정확한 작업 컨텍스트가 우선한다.

## 5. 재검증 조건

다음이 바뀌면 공식 문서를 다시 확인한다.

- API 모델·버전·요금·캐시 정책.
- JSON·구조화 출력 방식.
- worktree 명령과 플랫폼별 제한.
- 프로젝트의 보안·데이터 외부 전송 정책.

현재 프로젝트에서 사용할 실제 모델명, 비용, 토큰 한도와 계정 설정은 프로젝트 전용 AI 협업 프로필에서 관리한다.
