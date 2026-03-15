# PyPI 배포 가이드

PyPI에 패키지를 올리려면 **계정·API 토큰**과 **패키지 메타데이터**가 필요합니다.

---

## 1. PyPI 계정 및 API 토큰

### 계정 만들기

1. [PyPI](https://pypi.org) 접속 후 **Register** 로 가입

### API 토큰 발급

1. PyPI 로그인 → **Account settings** → **API tokens** → **Add API token**
2. **Token name**: 예) `elio-mcp-server`
3. **Scope**:  
   - **Entire account** (모든 패키지 업로드) 또는  
   - **Project: elio-mcp-server** (이 패키지만 업로드, 권장)
4. **Create token** 후 표시되는 `pypi-...` 값을 **한 번만** 복사해 안전한 곳에 보관 (다시 볼 수 없음)

---

## 2. 업로드 방법

### 방법 A: 토큰을 직접 입력

```bash
pip install build twine
python -m build
twine upload dist/*
```

실행 후:

- **Username**: `__token__`
- **Password**: 방금 복사한 `pypi-...` 토큰 전체

### 방법 B: .pypirc에 저장 (로컬만 사용, Git에 올리지 말 것)

`~/.pypirc` 파일 생성:

```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-여기에_토큰_붙여넣기
```

이후:

```bash
twine upload dist/*
```

⚠️ **주의**: `.pypirc`는 Git에 커밋하지 마세요. 이미 `.gitignore`에 없으면 프로젝트 루트에 넣지 말고 홈 디렉터리(`~/.pypirc`)에만 두세요.

---

## 3. 이 프로젝트에 들어 있는 메타데이터

`pyproject.toml`에 PyPI에 노출되는 정보가 들어 있습니다.

| 항목 | 내용 |
|------|------|
| **name** | `elio-mcp-server` |
| **version** | `0.1.0` (배포할 때마다 올려야 함) |
| **description** | 짧은 한 줄 설명 |
| **readme** | `README.md` → PyPI 프로젝트 페이지에 표시 |
| **license** | MIT |
| **urls** | Homepage, Repository, Bug Tracker (GitHub) |
| **authors** | elio robotics \<caram88@mobilian.biz\> |
| **maintainers** | johnsnow-nam |
| **classifiers** | 라이선스, Python 버전 등 |
| **dependencies** | `mcp`, `pyserial` |

수정이 필요하면 `pyproject.toml`만 고치면 됩니다.  
라이선스 전문은 저장소 루트의 **LICENSE** 파일을 사용합니다.

**예전 방식과의 대응** (예: elio-uart의 `setup.py` 기준):

| 예전 (setup.py / setup.cfg) | 현재 (pyproject.toml) |
|-----------------------------|-------------------------|
| `long_description=open('README.md').read()` | `readme = "README.md"` |
| `[metadata] description-file = README.md` | 위와 동일 (readme로 통합) |
| `author`, `author_email` | `authors = [{ name = "...", email = "..." }]` |
| `packages=setuptools.find_packages()` | `[tool.setuptools.packages.find]` + `py-modules` |
| `classifiers` | 그대로 `classifiers = [...]` |

---

## 4. 배포 순서 요약

1. **버전 확인**: `pyproject.toml`의 `version` 수정 (이미 올린 버전이면 반드시 올려야 함)
2. **빌드**: `python -m build` → `dist/` 생성
3. **PyPI 업로드**: `twine upload dist/*` (토큰 입력 또는 `.pypirc` 사용)
