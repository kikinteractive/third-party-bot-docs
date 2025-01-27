#!/usr/bin/env bash
set -e

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
[[ -d generated ]] || mkdir generated
python -m grpc_tools.protoc -I proto --python_betterproto_out=generated $(find proto -type f -name "*.proto")