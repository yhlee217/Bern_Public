#!/bin/bash
# nul 파일 정리 스크립트
# 사용법: bash scripts/cleanup-nul.sh

echo "=========================================="
echo "🧹 Cleaning up nul files"
echo "=========================================="

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.." || exit 1

# nul 파일 찾기
echo "Searching for nul files..."
nul_files=$(find . -name "nul" -type f 2>/dev/null)

if [ -z "$nul_files" ]; then
    echo "✅ No nul files found!"
    exit 0
fi

echo "Found nul files:"
echo "$nul_files"
echo ""

# 삭제 확인
read -p "Delete these files? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    find . -name "nul" -type f -delete 2>/dev/null
    echo "✅ Deleted all nul files"
else
    echo "ℹ️ Cancelled"
fi

echo "=========================================="
