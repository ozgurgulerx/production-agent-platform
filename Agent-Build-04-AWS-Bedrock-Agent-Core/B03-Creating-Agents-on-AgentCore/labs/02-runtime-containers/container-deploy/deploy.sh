#!/usr/bin/env bash
# Way 3: build the arm64 image, push to ECR, then create the Runtime from the image (create_runtime.py).
set -euo pipefail
: "${AWS_REGION:?}" "${AWS_ACCOUNT_ID:?}"
REPO=ticket-agent
URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO"
aws ecr describe-repositories --repository-names "$REPO" >/dev/null 2>&1 || aws ecr create-repository --repository-name "$REPO" >/dev/null
aws ecr get-login-password | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
docker buildx build --platform linux/arm64 -t "$URI:latest" --push .
echo "pushed $URI:latest"
python create_runtime.py --image "$URI:latest" "$@"
