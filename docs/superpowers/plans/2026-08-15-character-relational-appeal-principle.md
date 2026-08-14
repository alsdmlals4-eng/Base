# Character Relational Appeal Principle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 캐릭터의 매력을 개별 설정표가 아니라 캐릭터×캐릭터, 캐릭터×세계, 캐릭터×능력의 상호작용에서 발생하는 선택·갈등·행동·결과로 검수하는 `RELATIONAL_APPEAL` 공용 작법 원칙을 기존 Base 서사 Method와 연재소설 consumer에 추가한다.

**Architecture:** 새 Skill·Mode·Registry 항목을 만들지 않는다. `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`를 공용 owner로 삼고, 기존 `developing-and-revising-serial-fiction` Skill 및 캐릭터 감사 reference가 이 owner를 선택적으로 소비하도록 연결한다. 계약 테스트는 공용 owner, 세 조합 축, 관찰 가능한 proof, serial-fiction consumer 연결을 한 번에 검증한다.

**Tech Stack:** Markdown knowledge/Skill contracts, Python `unittest`, GitHub Actions/기존 Base 검증 파이프라인.

## Global Constraints

- 공용 식별자는 정확히 `RELATIONAL_APPEAL`을 사용한다.
- 조합 축은 `CHARACTER_X_CHARACTER`, `CHARACTER_X_WORLD`, `CHARACTER_X_ABILITY` 세 개다.
- 성공 기준은 설정량이 아니라 실제 `new_choice`, `new_conflict_or_cooperation`, `new_dialogue_or_behavior`, `new_consequence` 중 현재 범위에 필요한 관찰 가능한 차이 하나 이상이다.
- 새 Skill을 만들지 않는다.
- 새 Skill Mode를 만들지 않는다.
- `skills/SKILL_REGISTRY.json`을 변경하지 않는다.
- 기존 프로젝트의 캐릭터·세계관·관계 정본을 소급 변경하지 않는다.
- 모든 캐릭터 조합·관계 수치·능력 대가를 의무화하지 않는다.
- 진행 중인 다른 PR은 수정하지 않는다. 이 작업 브랜치의 변경만 다룬다.

---

### Task 1: 관계적 매력 계약 테스트를 먼저 추가한다

**Files:**
- Modify: `tests/test_serial_fiction_discipline.py`
- Test: `tests/test_serial_fiction_discipline.py`

**Interfaces:**
- Consumes: 기존 `ROOT`, `SKILL_PATH`, `REFERENCE_ROOT` 테스트 상수와 현재 Base 경로 구조.
- Produces: 공용 owner와 기존 serial-fiction consumer의 `RELATIONAL_APPEAL` 연결을 고정하는 회귀 테스트 `test_relational_appeal_has_common_owner_and_serial_fiction_consumers`.

- [ ] **Step 1: failing test를 추가한다**

기존 테스트 클래스에 다음 메서드를 추가한다.

```python
    def test_relational_appeal_has_common_owner_and_serial_fiction_consumers(self) -> None:
        common_method = (
            ROOT / "docs" / "knowledge" / "methods" / "NARRATIVE_AND_RELATIONSHIP_METHOD.md"
        ).read_text(encoding="utf-8")
        skill = SKILL_PATH.read_text(encoding="utf-8")
        reference = (
            REFERENCE_ROOT / "character-distinctiveness-and-opponent-threat.md"
        ).read_text(encoding="utf-8")
        combined_consumers = skill + "\n" + reference

        for token in (
            "RELATIONAL_APPEAL",
            "CHARACTER_X_CHARACTER",
            "CHARACTER_X_WORLD",
            "CHARACTER_X_ABILITY",
            "relational_appeal_proof",
            "DECORATIVE_SYNERGY",
            "FORCED_CHEMISTRY",
            "CROSS_PRODUCT_OVERDESIGN",
        ):
            self.assertIn(token, common_method)

        self.assertIn(
            "docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md",
            combined_consumers,
        )
        self.assertIn("RELATIONAL_APPEAL", combined_consumers)
```

- [ ] **Step 2: 새 테스트가 구현 전 실패하는지 확인한다**

Run:

```bash
python -m unittest tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_relational_appeal_has_common_owner_and_serial_fiction_consumers -v
```

Expected: `FAIL` because the common Method does not yet contain `RELATIONAL_APPEAL` and the three relational axes.

- [ ] **Step 3: 테스트 변경을 커밋한다**

```bash
git add tests/test_serial_fiction_discipline.py
git commit -m "test: define relational appeal craft contract"
```

---

### Task 2: 공용 owner에 `RELATIONAL_APPEAL`을 구현한다

**Files:**
- Modify: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- Test: `tests/test_serial_fiction_discipline.py`

**Interfaces:**
- Consumes: 기존 캐릭터 목소리 카드, 관계 설계, 선택 기억, 연속 이벤트 규칙.
- Produces: 소설·게임 서사에서 공유하는 `RELATIONAL_APPEAL` 정의와 세 조합 축, 관찰 가능한 proof, 과설계 방지 failure states.

- [ ] **Step 1: 관계 설계 절 뒤에 공용 원칙을 추가한다**

다음 의미를 유지하는 절을 `NARRATIVE_AND_RELATIONSHIP_METHOD.md`에 추가한다.

```markdown
## 관계적 매력 — `RELATIONAL_APPEAL`

캐릭터는 단독 설정표보다 관계와 상황 속에서 증명한다. `RELATIONAL_APPEAL`은 설정 항목을 더 많이 만드는 규칙이 아니라, 캐릭터와 다른 요소의 조합이 실제로 새로운 선택·갈등·협력·대사·행동·결과를 발생시키는지 보는 공용 Lens다.

### `CHARACTER_X_CHARACTER`

두 인물이 함께 있을 때 욕망·가치관·도덕 경계·권력·정보·책임의 차이가 서로의 다른 면을 드러내는지 본다. 상대에게만 나오는 말투·행동·취약성이나 둘이 함께 있을 때만 가능한 선택·실패·하이라이트가 있으면 강한 증거다.

### `CHARACTER_X_WORLD`

출신·계층·직업·조직·문화·제도·금기·자원·기술·괴이/마법 규칙이 인물의 현재 선택 비용과 생활 방식에 실제 영향을 주는지 본다. 같은 세계 조건을 인물마다 다르게 해석하고, 그 차이가 관계·책임·위험·기회에 흔적을 남겨야 한다.

### `CHARACTER_X_ABILITY`

능력·전투 역할·전문 기술을 캐릭터와 분리된 기능 목록으로 두지 않는다. 무엇에 먼저 쓰고 무엇에는 쓰지 않는지, 비용·한계·부작용을 어떻게 받아들이는지, 가치관과 경험이 해결법을 어떻게 바꾸는지, 능력 사용 뒤 무엇이 남는지를 본다.

최소 증거:

```yaml
relational_appeal_proof:
  new_choice:
  new_conflict_or_cooperation:
  new_dialogue_or_behavior:
  new_consequence:
```

모든 필드를 채우지 않는다. 현재 장면·아크·시스템에서 필요한 관찰 가능한 차이 하나 이상이면 된다.

Failure states:

- `DECORATIVE_SYNERGY`: 조합 설정은 있으나 장면·선택·행동·결과가 달라지지 않는다.
- `FORCED_CHEMISTRY`: 조합을 보여주려고 기존 욕망·판단·정본을 억지로 비튼다.
- `BIOGRAPHY_WITHOUT_PRESSURE`: 과거·계층·문화가 현재 선택과 비용에 영향을 주지 않는다.
- `ABILITY_AS_GIMMICK`: 능력이 가치·비용·문제 해결 방식과 무관한 장식이다.
- `RELATIONSHIP_TAG_ONLY`: 관계 태그·수치만 바뀌고 실제 대사·행동·정보·후속 장면이 달라지지 않는다.
- `CROSS_PRODUCT_OVERDESIGN`: 모든 캐릭터 조합을 의무 설계해 장면·콘텐츠 예산을 폭증시킨다.

모든 캐릭터 쌍의 전용 이벤트, 모든 관계의 수치화, 모든 능력의 서사적 대가를 강제하지 않는다. 프로젝트 정본과 매체별 실행 규칙이 이 공용 Lens보다 우선한다.
```

- [ ] **Step 2: contract test가 아직 consumer 연결 때문에 실패하는지 확인한다**

Run:

```bash
python -m unittest tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_relational_appeal_has_common_owner_and_serial_fiction_consumers -v
```

Expected: `FAIL` because serial-fiction Skill/reference do not yet link the common owner.

- [ ] **Step 3: 공용 owner 변경을 커밋한다**

```bash
git add docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md
git commit -m "docs: add relational appeal craft principle"
```

---

### Task 3: 기존 연재소설 consumer에 공용 원칙을 연결한다

**Files:**
- Modify: `skills/developing-and-revising-serial-fiction/SKILL.md`
- Modify: `skills/developing-and-revising-serial-fiction/references/character-distinctiveness-and-opponent-threat.md`
- Test: `tests/test_serial_fiction_discipline.py`

**Interfaces:**
- Consumes: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`의 `RELATIONAL_APPEAL`.
- Produces: 새 Mode 없이 기존 `pov-and-character-voice` / `character-and-opponent-integrity` 흐름에서 필요할 때 관계적 매력을 감사하는 consumer 연결.

- [ ] **Step 1: `SKILL.md`의 Read first에 공용 Method 경로를 연결한다**

캐릭터 개성·관계·능력 조합이 작업의 핵심일 때 다음 문서를 읽도록 기존 `Read first` 목록에 추가한다.

```markdown
- 캐릭터×캐릭터·캐릭터×세계·캐릭터×능력의 조합이 장면 선택과 관계 변화를 만드는지 점검할 때 `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`의 `RELATIONAL_APPEAL`을 선택적으로 사용한다.
```

- [ ] **Step 2: 기존 캐릭터 감사 reference에 짧은 소비 절을 추가한다**

```markdown
## 관계적 매력 감사 — `RELATIONAL_APPEAL`

개별 캐릭터 카드가 충분해도 조합이 장면을 만들지 못하면 설정은 정지해 있을 수 있다. 필요할 때 공용 owner `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`의 `RELATIONAL_APPEAL`을 사용한다.

```text
CHARACTER_X_CHARACTER | CHARACTER_X_WORLD | CHARACTER_X_ABILITY
→ 현재 조합에서 생기는 압력
→ 새 선택 / 갈등·협력 / 대사·행동 / 결과 중 관찰 가능한 차이
→ 기존 정본·욕망·판단과의 정합성
```

`DECORATIVE_SYNERGY`, `FORCED_CHEMISTRY`, `CROSS_PRODUCT_OVERDESIGN`이 보이면 설정을 더 붙이기보다 장면에서 실제로 필요한 최소 조합만 남긴다.
```

- [ ] **Step 3: focused contract test를 실행한다**

Run:

```bash
python -m unittest tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_relational_appeal_has_common_owner_and_serial_fiction_consumers -v
```

Expected: `PASS`.

- [ ] **Step 4: serial-fiction 계약 전체를 실행한다**

Run:

```bash
python -m unittest tests.test_serial_fiction_discipline -v
```

Expected: all tests `PASS`.

- [ ] **Step 5: consumer 변경을 커밋한다**

```bash
git add skills/developing-and-revising-serial-fiction/SKILL.md skills/developing-and-revising-serial-fiction/references/character-distinctiveness-and-opponent-threat.md
git commit -m "feat: consume relational appeal in serial fiction craft"
```

---

### Task 4: 회귀·적대적 검토 후 PR 검증을 닫는다

**Files:**
- Verify: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- Verify: `skills/developing-and-revising-serial-fiction/SKILL.md`
- Verify: `skills/developing-and-revising-serial-fiction/references/character-distinctiveness-and-opponent-threat.md`
- Verify: `tests/test_serial_fiction_discipline.py`

**Interfaces:**
- Consumes: Tasks 1–3의 문서 계약과 테스트 결과.
- Produces: `attack → validate-critique → regression-recheck → decision-report` 결과와 검증 가능한 PR.

- [ ] **Step 1: 설계 제약 회귀 검색을 수행한다**

Run:

```bash
git diff main...HEAD -- skills/SKILL_REGISTRY.json
git diff main...HEAD --name-only
```

Expected: Registry diff is empty; changed files are 승인된 설계/계획, 공용 Method, 기존 Skill/reference, 계약 테스트로 제한된다.

- [ ] **Step 2: 적대적 검토를 수행한다**

다음 질문을 diff에 적용한다.

```text
1. 기존 캐릭터 개성 규칙을 단순 반복하는가?
2. 모든 캐릭터 조합을 의무화해 콘텐츠 예산을 폭증시키는가?
3. 세계관 설정량 증가를 품질로 오해하게 만드는가?
4. 모든 능력에 대가·트라우마를 강제하는가?
5. 관계 태그·호감도 수치가 실제 관계 경험을 대체하는가?
6. 선형 소설과 인터랙티브 게임의 매체 차이를 침범하는가?
```

Expected: 모두 `No`. `Yes`가 하나라도 나오면 해당 문구만 최소 수정하고 focused test와 전체 serial-fiction contract를 다시 실행한다.

- [ ] **Step 3: Base의 관련 Python 회귀 테스트를 실행한다**

Run:

```bash
python -m unittest tests.test_serial_fiction_discipline -v
python -m unittest tests.test_local_validation -v
```

Expected: all tests `PASS`.

- [ ] **Step 4: PR을 만들고 GitHub Actions를 확인한다**

PR 제목:

```text
feat: add relational appeal craft principle
```

PR 본문에는 다음을 기록한다.

```markdown
## Summary
- add `RELATIONAL_APPEAL` to the existing narrative/relationship common Method
- cover character×character, character×world, and character×ability as observable interaction lenses
- connect the existing serial-fiction Skill/reference without adding a Skill, Mode, or Registry entry

## Validation
- focused relational-appeal contract
- full `tests.test_serial_fiction_discipline`
- `tests.test_local_validation`
- adversarial regression review: no forced cross-product design, no canon override, no registry expansion
```

Expected: required GitHub checks finish Green. 실패하면 로그를 확인해 이 PR에서 발생한 회귀만 최소 수정한다.

- [ ] **Step 5: 완료 증거를 보고한다**

최종 보고는 다음을 분리한다.

```text
실제 변경
검증 증거
미검증
남은 위험
Base 공용 승격 결과
프로젝트 전용 변경 여부
```

`Base 공용 승격 결과`는 `RELATIONAL_APPEAL`이 공용 Method owner에 들어갔음을 기록하고, `프로젝트 전용 변경 여부`는 `없음`으로 기록한다.
