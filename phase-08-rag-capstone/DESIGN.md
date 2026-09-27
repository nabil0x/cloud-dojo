# Capstone Design — <your chatbot name> (Q8.1 template)

> Fill every section. Get it reviewed before writing code.
> Delete these prompt lines as you complete them.

## 1. Overview
What it answers, who it's for, in 3 sentences.

## 2. Architecture
Boxes + arrows (ASCII is fine). Show THREE flows:
- Data flow: docs → S3 → indexing → Knowledge Base
- Request flow: client → API Gateway → Lambda → KB → model → answer
- Failure flow: KB down? model throttled? auth fails? What does the user see?

## 3. Service choices
| Choice | Why this, not the alternative |
|---|---|
| (e.g. Bedrock KB vs hand-rolled RAG) | |
| (e.g. HTTP API vs REST API) | |
| (e.g. real-time endpoint vs Batch Transform) | |

Every arrow in §2 needs a row here. No justification = delete the box.

## 4. Cost table
| Scale (req/mo) | Tokens | Endpoint hrs | Storage | Est. total |
|---|---|---|---|---|
| 100 | | | | |
| 10,000 | | | | |
| 1,000,000 | | | | |

Note per-unit rates observed (per-1k-tokens in/out, endpoint $/hr). Which scale breaks the bank, and why?

## 5. Open questions
List at least 2 things you're unsure about. Unknowns you name can't ambush the demo.
