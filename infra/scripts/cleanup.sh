#!/bin/bash
set -e

echo "=== Developing on AWS - Student Environment Cleanup ==="
echo ""
echo "This will destroy all student environments and related resources."
read -p "Are you sure you want to continue? (y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# CDK ディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CDK_DIR="$SCRIPT_DIR/../cdk"

cd "$CDK_DIR"

# CDK destroy
echo ""
echo "Destroying CDK stack..."
npx cdk destroy --force

echo ""
echo "=== Cleanup Complete ==="
echo "All student environments have been terminated."
