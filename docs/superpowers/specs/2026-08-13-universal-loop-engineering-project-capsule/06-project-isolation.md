# Project Isolation

공용으로 공유하는 것은 Base Kernel, Capability, Schema와 승인된 공용 학습뿐이다.

Planning Lock, Visual Lock, Active Run, 작업공간, Agent Session, Asset Registry, Resource Lease와 Agent Context는 프로젝트별로 분리한다. 모든 실행과 도구 호출은 프로젝트 ID, Run ID, 기준 main SHA를 확인한다.

다른 프로젝트의 Canon·시각 레퍼런스·Asset·Session이 들어오면 실행을 중지한다. 공용으로 재사용할 교훈은 직접 복사하지 않고 Base 승격 절차를 거친다. 한 프로젝트의 실패나 비용 초과는 다른 프로젝트 Run의 권한과 상태에 영향을 주지 않는다.
