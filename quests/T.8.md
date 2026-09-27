# T.8 — API Gateway authorizer (25 XP)

**Phase:** Track T — Real-AWS Parallel Track

## Concept
An API in front of a Lambda is only as safe as its front door.
API Gateway authorizers validate callers before your function runs, so rejected requests never cost you a Lambda invocation or a downstream model call.
A JWT authorizer checks a bearer token from an identity provider like Cognito, while an IAM authorizer checks SigV4-signed AWS calls.
In this quest you put a JWT (or IAM) authorizer on an HTTP API in front of a Lambda and prove both paths: a valid token returns 200 with the answer, and a missing or invalid token returns 401 or 403.
This gate is the exact pattern the final capstone reuses, and it only behaves truthfully on real AWS, never on an emulator.

## Uses
- Protecting serverless APIs so only authenticated callers reach the backend.
- Rejecting bad tokens cheaply before any compute or model cost is incurred.
- Reusing one identity provider across many APIs.
- Throttling and quota-gating expensive AI endpoints behind authentication.
- Giving the RAG capstone a secure front door it can build on.

## Key info
- Create an HTTP API with a Lambda integration, then attach a JWT authorizer (issuer URL plus audience) or an IAM authorizer.
- Valid call: `curl -H "Authorization: Bearer <valid-token>" https://<api>/endpoint` returns 200.
- Invalid call: the same request with a missing or bad token returns 401 or 403.
- JWT authorizers need an issuer and an audience; IAM authorizers need SigV4-signed requests.
- The order that matters: auth first, throttle second, validate third.
- Real AWS enforces this gate. The emulator does not.
- Authorizers reject before your integration runs, so a 401 never reaches the Lambda.
- Return 401 for a missing or invalid token and 403 when the token is valid but lacks permission.

## Pitfalls
- Leaving the route open with no authorizer and thinking the Lambda's own checks are enough.
- Using an expired token and concluding the authorizer is broken.
- Testing only the happy path, so a misconfigured gate lets bad requests through unnoticed.

## Done check
paste both `curl` outputs. This gate is what Q8.3 will reuse.

## Links
- JWT authorizers: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html
- IAM authorization for HTTP APIs: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control-iam.html
- Lambda authorizers: https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
