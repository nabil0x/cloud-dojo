# Phase 3 starter: Lambda container image.
# Build:  docker build -t dojo-lambda .
# The base image provides the Runtime Interface Client; CMD names the handler.
FROM public.ecr.aws/lambda/python:3.13

COPY handler.py ${LAMBDA_TASK_ROOT}/

CMD ["handler.handler"]
