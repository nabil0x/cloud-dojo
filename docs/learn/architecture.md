# Architecture Maps (rendered natively by GitHub)

## The journey: phases → capstone
```mermaid
flowchart LR
    P0["0 · Docker foundations"] --> P1["1 · S3/SQS/DynamoDB"]
    P1 --> P2["2 · Compose stack"]
    P2 --> P3["3 · Lambda images"]
    P1 --> M["M · Moto testing"]
    P1 --> T["T · Real-AWS IAM/billing"]
    P3 --> P4["4 · EC2/VPC/RDS"]
    P4 --> P5["5 · Bedrock/SageMaker"]
    P3 --> P6["6 · Terraform"]
    P6 --> P7["7 · CI/CD + ECS"]
    P5 --> P8["8 · RAG capstone"]
    P7 --> P8
    T --> P8
    style P8 fill:#3fb950,color:#0d1117
```

## Phase 2 stack: who talks to whom
```mermaid
flowchart LR
    You(["you: laptop"]) -- "localhost:4566" --> EMU(["emulator :4566"])
    You -- "localhost:8080" --> APP(["app :8080"])
    APP -- "http://emulator:4566\n(service DNS, NOT localhost)" --> EMU
    SEED(["seed.sh (host)"]) -.-> EMU
    subgraph compose["one `docker compose up`"]
        EMU
        APP
    end
```

## Capstone (Phase 8): request path
```mermaid
flowchart LR
    C(["client"]) -- "HTTPS + JWT" --> GW["API Gateway\n(auth, throttle, CORS)"]
    GW --> L["Lambda\n(retrieve → generate)"]
    L --> KB[("Bedrock Knowledge Base")]
    DOCS[("S3 docs")] --> KB
    L --> M2["Bedrock model"]
    L -- "cited answer" --> C
    TF["Terraform + CI pipeline"] -. "owns everything" .-> GW
    TF -.-> L
    TF -.-> KB
```

## Emulator vs real AWS: what to practice where
```mermaid
flowchart TD
    Q{"What are you learning?"}
    Q -- "APIs, data models,\nCLI/SDK fluency" --> EM["Emulator\n(MiniStack/LocalStack/Moto)"]
    Q -- "IAM enforcement,\nconsole, billing,\nquotas, networking" --> RW["Real sandbox\n(Builder Center / Skill Builder)"]
    Q -- "Shipping code,\npipelines, prod" --> BOTH["Emulator first,\nvalidate on real"]
```
