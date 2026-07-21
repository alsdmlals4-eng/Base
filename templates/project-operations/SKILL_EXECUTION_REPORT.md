# Skill 실행 보고

사용자가 Skill 이름이나 mode를 직접 선언하지 않아도 Registry trigger로 자동 선택한다. 실제로 실행한 Skill만 기록하며, 선택 후보였지만 사용하지 않은 Skill은 중요한 경우에만 제외 이유를 남긴다.

## 자동 라우팅

```yaml
request_summary:
work_level:
primary_discipline:
affected_disciplines: []
routing_source: automatic-trigger-match
user_skill_declaration_required: false
```

## 사용한 Skill

| Skill | Mode | 사용 이유·Trigger | 수행한 작업 | 얻은 결과 | 증거·경로 | 상태 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  | PASS/PARTIAL/FAIL/UNVERIFIED |

## 사용하지 않은 중요 후보

| Skill | 제외 이유 |
|---|---|
|  | trigger 불일치 / 비사용 조건 / 현재 단계 아님 / 도구·입력 없음 |

## 결과 요약

- 실제 변경:
- 확인한 사실:
- 검증 결과:
- 미검증·실패:
- 남은 위험·롤백:
- 다음 작업:

## 규칙

- “도움이 될 것 같아서”가 아니라 Registry trigger와 현재 단계로 이유를 쓴다.
- Skill 파일을 읽은 것과 Skill을 실제 실행한 것을 구분한다.
- mode별 결과를 합치지 말고, 어떤 판단·산출물·검증을 만들었는지 적는다.
- 실행하지 않은 Skill·테스트·도구를 사용했다고 보고하지 않는다.
- 사용자가 결과만 요청한 짧은 작업에서는 최종 보고의 `사용한 Skill` 항목으로 압축할 수 있다.
