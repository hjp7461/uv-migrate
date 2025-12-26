# Poetry to uv Migration Tool 개발 계획 (plan.md)

본 문서는 `doc/PRD.md`에 명시된 요구사항을 바탕으로, Poetry 프로젝트를 uv 기반 프로젝트로 변환하는 도구 개발을 위한 상세 작업 계획을 담고 있습니다.

## 1. 프로젝트 초기화 및 환경 구성
- [x] 의존성 라이브러리 설치: `tomlkit`, `typer`
- [x] 프로젝트 구조 재구성
  - `src/uv_migrate/` 디렉토리 생성 및 로직 이동
  - `tests/` 디렉토리 생성 (테스트 코드)
- [x] 개발 환경 검증 (Python 3.10+ 확인)

## 2. 변환 엔진 (Core Logic) 구현
`pyproject.toml`을 읽고 분석하여 PEP 621 표준 및 uv 설정으로 변환하는 핵심 로직을 개발합니다.

### 2.1 메타데이터 변환 (PRD 3.1)
- [x] `tool.poetry.name` -> `project.name`
- [x] `tool.poetry.version` -> `project.version`
- [x] `tool.poetry.description` -> `project.description`
- [x] `tool.poetry.authors` -> `project.authors`
- [x] `tool.poetry.license` -> `project.license`
- [x] `tool.poetry.readme` -> `project.readme`
- [x] `tool.poetry.dependencies.python` -> `project.requires-python` (버전 형식 변환 포함)

### 2.2 의존성 변환 (PRD 3.2)
- [x] `tool.poetry.dependencies` (python 제외) -> `project.dependencies`
- [x] `tool.poetry.group.dev.dependencies` -> `dependency-groups` (PEP 735) 또는 `project.optional-dependencies`
- [x] Poetry 특수 구문 (extras, version inline table) -> 표준 PEP 508 형식 문자열 변환

### 2.3 스크립트 및 설정 변환 (PRD 3.3, 3.4, 3.5)
- [x] `tool.poetry.scripts` -> `project.scripts`
- [x] `build-system` 섹션 업데이트 (hatchling 등 uv 권장 표준으로 변경)
- [x] `tool.poetry.source` -> `tool.uv.sources` 변환 로직 구현

## 3. CLI 및 사용자 인터페이스 (PRD 5)
- [x] `typer`를 이용한 명령어 인터페이스 구현
- [x] 입력 파일 검증 및 `tool.poetry` 섹션 존재 여부 확인
- [x] 원본 파일 백업 기능 구현 (`.bak` 생성)
- [x] 변환 완료 후 `uv lock` 실행 안내 메시지 출력

## 4. 품질 보증 및 테스트
- [x] 다양한 Poetry `pyproject.toml` 샘플에 대한 단위 테스트
- [x] 복잡한 의존성 구조(extras, git, path 등) 변환 정확도 검증
- [x] `tomlkit`을 이용한 기존 서식(주석 등) 보존 여부 확인

## 5. 배포 준비 및 마무리
- [x] README.md 업데이트 (사용법 포함)
- [x] 최종 빌드 및 설치 테스트
- [x] (선택) `uv-migrate` 실행 스크립트 등록
