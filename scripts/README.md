# Scripts 디렉토리

프로젝트 유틸리티 스크립트 모음

## 📂 스크립트 목록

### cleanup-nul.sh / cleanup-nul.ps1
**기능**: 프로젝트 내 불필요한 `nul` 파일 자동 정리

**nul 파일이란?**
- Windows 명령어에서 에러 리다이렉트 실패 시 생성되는 불필요한 파일
- Git Bash 환경에서 `2>nul` 사용 시 실제 파일로 생성됨
- 프로젝트에 불필요하며 삭제해도 무방

**사용법:**

```bash
# Git Bash에서
bash scripts/cleanup-nul.sh

# PowerShell에서
powershell -ExecutionPolicy Bypass -File scripts\cleanup-nul.ps1

# 또는 PowerShell에서 직접
.\scripts\cleanup-nul.ps1
```

**자동 실행:**
- Git Hook (`post-commit`)에 설정되어 커밋 후 자동 삭제됨
- `.gitignore`에 추가되어 Git 추적 안됨

---

## 🔧 Git Hook 설정

### post-commit Hook
**위치**: `.git/hooks/post-commit`

**기능**:
- 커밋 후 자동으로 `nul` 파일 삭제
- 작업 디렉토리를 깨끗하게 유지

**확인:**
```bash
# Hook이 실행 가능한지 확인
ls -la .git/hooks/post-commit

# 수동 실행 테스트
.git/hooks/post-commit
```

---

## 📝 문제 해결

### Q1. nul 파일이 계속 생기는 이유는?

**A:** Git Bash에서 Windows 명령어 에러 리다이렉션 때문입니다.

```bash
# ❌ 잘못된 사용 (Git Bash)
command 2>nul      # "nul" 파일 생성됨

# ✅ 올바른 사용
command 2>/dev/null    # Git Bash/Unix
```

### Q2. nul 파일을 삭제해도 되나요?

**A:** 네! 완전히 불필요한 파일입니다.
- 프로젝트 동작에 영향 없음
- 언제든 안전하게 삭제 가능
- `.gitignore`에 추가되어 Git에서 무시됨

### Q3. Hook이 작동하지 않아요

**A:** Hook 실행 권한을 확인하세요.

```bash
# 권한 부여
chmod +x .git/hooks/post-commit

# 테스트
.git/hooks/post-commit
```

### Q4. 수동으로 빠르게 삭제하려면?

**A:** 명령어 한 줄로 삭제 가능:

```bash
# Git Bash
find . -name "nul" -type f -delete

# PowerShell
Get-ChildItem -Path . -Filter "nul" -Recurse -File | Remove-Item -Force
```

---

## 📋 체크리스트

- [x] `.gitignore`에 `nul` 추가
- [x] Git Hook (`post-commit`) 설정
- [x] 정리 스크립트 작성 (Bash/PowerShell)
- [x] 스크립트 실행 권한 부여
- [ ] 테스트 커밋으로 자동 삭제 확인

---

**작성일**: 2025-10-24
**작성자**: Bern
