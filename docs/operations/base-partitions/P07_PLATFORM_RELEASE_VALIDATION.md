# P07 · Platform, Release & Execution Validation — Context Pack

## 역할
실제 diff/정적/runtime evidence 검증, 플랫폼·권리·build/release·backend·DRM의 delivery readiness를 책임진다.

## 핵심 Skill
`reviewing-and-validating-project-changes`.

## 중요 규칙
Evidence ceiling, LATEST_EXACT_HEAD_ONLY, Notion approval != runtime proof, platform official-source-first, 미실행/미구성은 PASS 아님.

## 핵심 Module
Change Validation → Evidence Ledger → Platform/Rights → Build/Release → Backend → Entitlement/DRM.

## 경계
P03은 비판/적대적 판단 owner, P07은 실제 실행 증거 owner. P06 runtime을 소비하고 P04 acceptance/P05 asset rights를 검증한다.

## 우선 공격 대상
실행 증거 없는 완료 주장, 오래된 플랫폼 정책, planning screenshot을 runtime proof로 사용, Android/출시 단계 조기 확대, backend/DRM 과잉 설계.

## 검증/완료
해당 플랫폼/릴리스 focused tests, 최신 공식 출처, exact-head evidence. 최소 5회 전체 review 후 clean까지.
