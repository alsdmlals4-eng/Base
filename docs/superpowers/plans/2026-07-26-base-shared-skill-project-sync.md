# Base Shared Skill Project Sync Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans or subagent-driven-development task-by-task.

**Goal:** Base 공용 Skill route와 Godot 에셋 우선 탐색 정책을 네 프로젝트 운영체계에 어댑터 방식으로 연결한다.

**Architecture:** Base는 공용 Skill 본문과 route 계약의 단일 원본을 유지한다. 프로젝트는 전체 운영체계 기준과 공용 Skill route 기준을 구분할 수 있으며, 공용 route는 프로젝트 어댑터를 거쳐 실제 경로·정본·검증기를 주입한다.

## Global Constraints

- Base 공용 Skill 본문을 프로젝트에 복사하지 않는다.
- 프로젝트 전용 Skill만 프로젝트 내부에서 생성·관리한다.
- 게임 코드·Scene·데이터·자산은 수정하지 않는다.
- 두 공용 Skill 묶음은 검증된 Base commit `6a224e450f9420223c00921f3c56e051612f92ad`를 사용한다.
- 최신 Base main의 무관한 CI·Codex·문서 정책을 공용 Skill pin 갱신만으로 자동 도입하지 않는다.
- 실제 실행하지 못한 Godot·Android·플레이테스트 검증은 `NOT_RUN` 또는 `UNVERIFIED`로 남긴다.

## Task 1: Base 기준과 프로젝트 현황 감사

- [x] 각 프로젝트의 Base 기준과 Registry 경로 확인.
- [x] route·adapter·archive adapter 역할 바인딩 확인.
- [x] 기존 운영 문서와 선행 변경의 충돌 범위 확인.
- [x] `6a224e45…`를 두 공용 Skill의 안정 기준으로 선택.

## Task 2: 프로젝트 운영체계 연결

- [x] `skills/BASE_SHARED_SKILL_ROUTES.json`에 Base 메인 Registry route 추가.
- [x] `skills/PROJECT_BASE_SKILL_ADAPTER.json`에 프로젝트 경로·정본·검증기 연결.
- [x] 레거시 Skill을 프로젝트 archive adapter로 연결.
- [x] Godot 자산 우선 탐색 Skill을 프로젝트 공용 adapter로 연결.
- [x] 공용 Skill 본문 복제 금지와 프로젝트 전용 Skill local-only 정책 유지.
- [x] 통합 설명 문서와 제3자 자산·라이선스 기록 위치 구성.

## Task 3: 검증기 갱신

- [x] 각 프로젝트에 `tests/test_base_shared_skill_adapter.py` 추가.
- [x] Base pin 일치, 메인 Registry adapter route, 필수 extension, local policy 검사.
- [x] 어댑터 경로 존재와 archive 비정본 권한 검사.
- [ ] GitHub Actions에서 프로젝트별 테스트 실행 확인.

## Task 4: 증거 확인과 보고

- [ ] 각 branch와 main의 변경 파일 비교.
- [ ] 제품 코드·Scene·데이터·자산 무변경 확인.
- [ ] PR 생성 후 CI 상태 확인.
- [ ] urban-legend 기존 archive Manifest 완전 이관은 별도 reconciliation로 분리.
- [ ] Godot·Android·Windows·사람 플레이 미실행 상태를 구분해 보고.
