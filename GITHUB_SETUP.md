# GitHub 저장소 연결하기

로컬 Git 저장소는 이미 초기화되어 있고 첫 커밋까지 완료된 상태입니다.

## 1. GitHub에서 새 저장소 만들기

1. [GitHub](https://github.com/new) 접속 후 **New repository** 클릭
2. **Repository name**: `elio-mcp-server` (또는 원하는 이름)
3. **Public** 선택
4. **"Add a README file"** 등은 체크하지 않음 (이미 로컬에 있음)
5. **Create repository** 클릭

## 2. 로컬과 연결 후 푸시

저장소를 만든 뒤 GitHub에서 표시되는 **저장소 URL**을 사용합니다.

```bash
cd /Users/seokhee/mcp-servers/elio-mcp-server

# GitHub에서 만든 저장소 URL로 변경 (아래는 예시)
git remote add origin https://github.com/YOUR_USERNAME/elio-mcp-server.git

git push -u origin main
```

- **HTTPS**: `https://github.com/YOUR_USERNAME/elio-mcp-server.git`
- **SSH**: `git@github.com:YOUR_USERNAME/elio-mcp-server.git`

`YOUR_USERNAME`을 본인 GitHub 사용자 이름으로 바꾸면 됩니다.

## (선택) GitHub CLI로 한 번에 만들기

GitHub CLI를 설치한 뒤에는 다음으로 저장소 생성과 푸시를 한 번에 할 수 있습니다.

```bash
brew install gh
gh auth login
cd /Users/seokhee/mcp-servers/elio-mcp-server
gh repo create elio-mcp-server --public --source=. --push
```
