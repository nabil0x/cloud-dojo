# GitHub Actions Cheat Sheet (Cloud Dojo)

Every push builds + tests in a clean room. Green main ships itself.

## Minimal CI (build + test on push)
```yaml
name: dojo-ci
on:
  push:
    branches: [main]
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t dojo-app:ci .
      - run: docker run --rm dojo-app:ci pytest -q
```

## Push to ECR by commit SHA
```yaml
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::<acct>:role/gh-actions  # OIDC, no stored keys
          aws-region: us-east-1
      - uses: aws-actions/amazon-ecr-login@v2
      - run: |
          IMG=<acct>.dkr.ecr.us-east-1.amazonaws.com/dojo-app
          docker build -t $IMG:${{ github.sha }} .
          docker push $IMG:${{ github.sha }}
```

## Deploy to ECS (rolling update)
```bash
aws ecs update-service --cluster dojo --service dojo-svc --force-new-deployment
aws ecs describe-services --cluster dojo --services dojo-svc \
  --query 'services[0].{running:runningCount,deployments:length(deployments)}'
```

## Contexts & expressions
- `${{ github.sha }}` commit, `${{ github.ref_name }}` branch, `${{ secrets.NAME }}`, `${{ vars.NAME }}`
- `if: github.ref == 'refs/heads/main'` gate deploy jobs to main
- Pin actions to SHAs (`actions/checkout@<sha>`) for supply-chain strictness; tags (`@v4`) otherwise

## Debugging red builds
- Logs read top-down; first error is usually the only real one
- Re-run failed jobs (not the whole workflow) from the run page
- `tmate` action for SSH-ing a live runner (debug only, never on main)

## Teardown (billing hygiene)
```bash
aws ecs update-service --cluster dojo --service dojo-svc --desired-count 0
aws ecs delete-service --cluster dojo --service dojo-svc --force
aws ecs delete-cluster --cluster dojo
```

*From the [Cloud Dojo](../README.md) Phase 7 path. Full lesson in `phase-07-cicd-ecs/`.*
