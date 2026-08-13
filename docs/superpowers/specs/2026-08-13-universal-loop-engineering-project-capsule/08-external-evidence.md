# External Evidence

## OpenAI Agents SDK

Agent, Handoff, Session과 Trace는 전문 역할과 실행 관측에 채택한다. 프로젝트 정본과 Run 상태는 SDK Session이 아니라 GitHub Capsule과 Run Ledger가 소유한다. 함수 도구 Guardrail을 활용하되 내장 실행 도구에는 별도의 프로젝트 범위 Wrapper가 필요하다.

Primary sources:

- https://openai.github.io/openai-agents-python/
- https://openai.github.io/openai-agents-python/guardrails/
- https://openai.github.io/openai-agents-python/tracing/

## GitHub Actions

수동 초기 실행은 `workflow_dispatch`, 프로젝트별 중복 축소는 reusable workflow를 사용한다.

- https://docs.github.com/en/actions/how-tos/manage-workflow-runs
- https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations

## Figma

Version History, Dev Mode 비교, Component·Style 설명은 Visual Evidence 보조로 사용한다. Figma 자체는 모든 프로젝트 필수 provider가 아니며 Final·Ready for Dev 상태만으로 Runtime 일치나 제품 자산 승인을 주장하지 않는다.

- https://help.figma.com/hc/en-us/articles/360038006754-View-a-file-s-version-history
- https://help.figma.com/hc/en-us/articles/23919923330455-Dev-Mode-focus-view
- https://help.figma.com/hc/en-us/articles/7938814091287-Add-descriptions-to-styles-components-and-variables
