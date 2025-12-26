# PRD: Poetry to uv Migration Tool

## 1. 개요
본 프로젝트는 기존에 `poetry`를 사용하여 관리되던 Python 프로젝트를 `uv` 기반의 프로젝트 구조로 자동 변환해주는 명령줄 도구(CLI) 개발을 목표로 한다. `pyproject.toml` 내의 `tool.poetry` 섹션을 PEP 621 표준 형식을 따르는 `project` 섹션 및 `uv` 전용 설정으로 변환한다.

## 2. 목표
- `poetry` 기반 프로젝트의 `uv` 전환 비용 최소화
- `pyproject.toml` 설정의 정확한 매핑 및 자동 변환
- 의존성 그룹(Dependency Groups)의 적절한 마이그레이션

## 3. 주요 기능
### 3.1 메타데이터 변환
- `tool.poetry.name`, `version`, `description`, `authors`, `license`, `readme` 등을 `project` 섹션의 해당 필드로 매핑한다.
- Python 버전 제약 조건(`tool.poetry.dependencies.python`)을 `project.requires-python`으로 변환한다.

### 3.2 의존성(Dependencies) 변환
- 기본 의존성(`tool.poetry.dependencies`)을 `project.dependencies` 리스트로 변환한다.
- 개발용 의존성(`tool.poetry.group.dev.dependencies`) 및 기타 그룹을 PEP 735(또는 `uv`의 dependency groups) 형식으로 변환하거나 `project.optional-dependencies`로 매핑한다.
- Poetry의 특수한 의존성 명시 방식(예: `{ version = "^1.0", extras = ["test"] }`)을 표준 형식으로 변환한다.

### 3.3 스크립트 및 진입점 변환
- `tool.poetry.scripts`를 `project.scripts`로 변환한다.

### 3.4 빌드 시스템 설정
- `build-system` 섹션을 `uv`가 사용하는 표준 설정(예: `hatchling` 또는 `setuptools`)으로 업데이트하거나 사용자 선택을 반영한다.

### 3.5 추가 도구 설정
- `tool.poetry.source` 설정을 `tool.uv.sources`로 변환하여 사설 인덱스 설정을 유지한다.

## 4. 기술 요구사항
- **언어**: Python 3.10 이상
- **라이브러리**: 
  - `tomlkit`: 주석 및 서식을 유지하면서 TOML 파일을 읽고 쓰기 위함
  - `typer` 또는 `click`: CLI 인터페이스 구현
- **입력**: Poetry 기반의 `pyproject.toml`
- **출력**: 변환된 `pyproject.toml` (원본은 `.bak`으로 백업 권장)

## 5. 사용자 시나리오
1. 사용자가 Poetry 프로젝트 루트에서 `uv-migrate` 명령어를 실행한다.
2. 프로그램이 `pyproject.toml`을 분석하고 `tool.poetry` 섹션의 존재를 확인한다.
3. 변환을 수행하고 새로운 `pyproject.toml`을 작성한다.
4. (선택 사항) 사용자가 `uv lock`을 실행하여 새로운 잠금 파일을 생성하도록 안내한다.

## 6. 제약 및 예외 사항
- `poetry.lock` 파일 자체를 `uv.lock`으로 직접 변환하는 대신, `pyproject.toml` 변환 후 `uv`를 통한 재해석을 권장한다.
- 매우 복잡한 Poetry 전용 플러그인 설정은 수동 확인이 필요할 수 있음을 알린다.
