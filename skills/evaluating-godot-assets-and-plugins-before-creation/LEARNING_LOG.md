# Evaluating Godot Assets and Plugins Learning Log

## 2026-08-05 — Direct adoption versus reference-to-original

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** 외부 에셋·플러그인·이미지·사운드의 구조와 기술을 조사하되 원본을 그대로 또는 약간 변형해 사용하지 않고 새 자산을 만들라는 승인된 Base 변경.
- **Finding:** 기존 `ADOPT / ADAPT / TRIAL / REJECT / BUILD_CUSTOM` 판정은 후보 도입에는 충분했지만, 직접 제품 포함과 `REFERENCE_TO_ORIGINAL` 분석 입력을 명시적으로 분리하지 않아 상업 사용·게임 포함 배포·원본 재배포와 유사성 증거가 섞일 수 있었다.
- **Decision:** 새 광역 Skill을 추가하지 않음. 기존 Skill에서 직접 포함은 `LICENSED_THIRD_PARTY`·`OPEN_SOURCE`, 참조 전용은 `REFERENCE_TO_ORIGINAL`, 직접 제작은 `OWNED_ORIGINAL`·`COMMISSIONED_ORIGINAL`·`AI_GENERATED`·`MIXED_ROUTE`로 연결한다.
- **Evidence contract:** `commercial_use`, `distribution_in_game_build`, `raw_source_redistribution`을 분리한다. 참조 전용 입력은 shipping package에서 제외하고 `reference_brief`, `forbidden_expression`, `final_asset_record`, `reference_similarity_status`를 요구한다.
- **Boundary:** 자동 법률 판정기를 추가하지 않음. 정적 검사는 누락·불일치만 차단하며 실제 권리 해석·침해 여부·플랫폼 승인·법률 clearance를 확정하지 않는다.
- **Verification state:** focused RED는 확인됨. exact-head GREEN, 공유 Route·reference freshness·전체 회귀는 후속 증거로 분리한다.
- **Next trigger:** 여러 프로젝트에서 같은 자산 유형과 라이선스 조건이 반복되고 기계 판정 가능한 안정 입력이 확보될 때 자동 validator를 별도 제안으로 검토한다.
