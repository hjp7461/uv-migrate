# Poetry to uv Migration Tool

Poetry 기반 프로젝트의 `pyproject.toml`을 uv(PEP 621) 표준으로 변환해주는 도구입니다.

## 주요 기능
- 메타데이터 변환 (Name, Version, Description 등)
- 의존성 변환 (PEP 508 형식으로 자동 변환)
- 개발 의존성 그룹 변환 (PEP 735 지원)
- 스크립트 및 빌드 시스템 업데이트
- 소스(Private Registry) 설정 변환

## 설치 및 사용법

### 설치
```bash
uv tool install .
```

### 사용법
기본적으로 현재 디렉토리의 `pyproject.toml`을 변환합니다.
```bash
uv-migrate
```

특정 파일을 지정하거나 출력을 별도로 저장할 수 있습니다.
```bash
uv-migrate path/to/pyproject.toml --output new_pyproject.toml
```

## 개발 및 테스트
```bash
# 테스트 실행
uv run pytest
```
