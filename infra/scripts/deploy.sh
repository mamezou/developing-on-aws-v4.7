#!/bin/bash
set -e

# デフォルト値
STUDENT_COUNT=3
INSTANCE_TYPE="t3.small"

# ヘルプ表示
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -n, --students NUMBER    受講者数 (デフォルト: 3)"
    echo "  -t, --type TYPE          インスタンスタイプ (デフォルト: t3.small)"
    echo "  -h, --help               このヘルプを表示"
    echo ""
    echo "Example:"
    echo "  $0 -n 5 -t t3.medium"
}

# パラメータ解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--students)
            STUDENT_COUNT="$2"
            shift 2
            ;;
        -t|--type)
            INSTANCE_TYPE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# パラメータ検証
if [[ $STUDENT_COUNT -lt 1 || $STUDENT_COUNT -gt 10 ]]; then
    echo "Error: Student count must be between 1 and 10"
    exit 1
fi

if [[ ! "$INSTANCE_TYPE" =~ ^t3\.(small|medium|large)$ ]]; then
    echo "Error: Instance type must be t3.small, t3.medium, or t3.large"
    exit 1
fi

echo "=== Developing on AWS - Student Environment Deployment ==="
echo "Students: $STUDENT_COUNT"
echo "Instance Type: $INSTANCE_TYPE"
echo ""

# CDK ディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CDK_DIR="$SCRIPT_DIR/../cdk"

cd "$CDK_DIR"

# 依存関係インストール
echo "Installing dependencies..."
npm install

# CDK デプロイ
echo "Deploying CDK stack..."
npx cdk deploy \
    --context studentCount=$STUDENT_COUNT \
    --context instanceType=$INSTANCE_TYPE \
    --require-approval never \
    --outputs-file outputs.json

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Access Information:"
cat outputs.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
stack = data.get('StudentEnvironmentStack', {})
students = {}
for key, value in stack.items():
    parts = key.rsplit('-', 1)
    if len(parts) == 2:
        student_id, field = parts
        if student_id not in students:
            students[student_id] = {}
        students[student_id][field] = value

for student_id in sorted(students.keys()):
    info = students[student_id]
    print(f'\\n{student_id}:')
    print(f'  URL: {info.get(\"URL\", \"N/A\")}')
    print(f'  Password: {info.get(\"Password\", \"N/A\")}')
"
