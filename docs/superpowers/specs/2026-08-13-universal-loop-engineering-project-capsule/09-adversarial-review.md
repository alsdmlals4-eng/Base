# Adversarial Review

- Capsule이 새 기획 정본이 될 위험: 책임 원본의 ID·SHA·범위만 잠그고 충돌 시 Capsule을 stale 처리한다.
- Coverage가 형식적 완료가 될 위험: 요구사항에서 구현 근거까지 정방향·역방향 연결을 모두 검사한다.
- Visual Lock이 창의적 개선을 막을 위험: 새 아이디어는 현재 구현에 넣지 않고 승인 후보로 분리한다.
- Figma 선택형으로 시각 기준이 약해질 위험: 선택형은 provider뿐이며 시각 영향 Package의 Visual Lock은 필수다.
- 프로젝트별 Adapter 코드가 난립할 위험: 선언형 Profile을 우선하고 반복 custom code는 Capability 재설계 신호로 본다.
- Multi-Agent가 비용과 충돌만 늘릴 위험: 단일 Builder가 기본이며 독립성과 측정 이득 없이는 병렬화하지 않는다.
- Runtime provider가 권위를 장악할 위험: provider는 실행 플러그인이고 상태·권한·Evidence는 Kernel과 GitHub Ledger가 소유한다.
- 잘못된 자동 폐쇄 위험: exact-head CI, Coverage, 중요 finding 0, postmerge main readback을 모두 요구한다.
- Base #314 미해결 위험: 하위 보호 경로를 쓰는 범용 무인 Writer와 A3는 문제 해결 전까지 닫는다.

```yaml
p0_unresolved_in_design: 0
p1_unresolved_in_design: 0
implementation_dependencies:
  - Base#314_before_generic_protected_product_writer
  - written_spec_user_review
```
