# T.7 — CloudWatch observability (25 XP)

**Phase:** Track T — Real-AWS Parallel Track

## Concept
Once a function runs in real AWS, you need to see what it is doing without logging into a server.
CloudWatch gives you metrics (numbers over time), logs (raw output for forensics), dashboards (the wall of truth), and alarms (a threshold plus an action).
In this quest you build a dashboard for a real Lambda function showing errors, invocations, and duration.
Then you write a Logs Insights query, for example to find the slowest invocations, and create an alarm on error rate that notifies you.
The rule of thumb: metrics drive alerting, logs drive debugging.
Alarms should fire on symptoms a human cares about, not on every metric wiggle.

## Uses
- Spotting error spikes and latency regressions before users complain.
- Investigating a single request through its log lines.
- Giving a team one dashboard that shows service health at a glance.
- Paging a human only when something genuinely needs attention.
- Building a feedback loop you will reuse for every later capstone function.

## Key info
- Dashboard widgets for a Lambda: `Errors`, `Invocations`, and `Duration` metrics.
- Logs Insights query example: `fields @timestamp, @duration | sort @duration desc | limit 20` for the slowest invocations.
- Create an alarm on error rate (for example, errors over a threshold in five minutes) with an SNS topic as the action.
- CloudWatch metrics come from the service automatically; application logs need permissions to be written.
- Alarm on symptoms that page a person, not on every metric fluctuation.
- This runs on real AWS, where metrics and alarms reflect actual traffic, unlike an emulator.
- Dashboards are cheap to make and pay off the first time an incident starts.
- An SNS topic turns an alarm into an email, which is what makes it act rather than just exist.

## Pitfalls
- Creating an alarm with no action, so it fires into the void.
- Alerting on a noisy metric, which trains the team to ignore alarms entirely.
- Forgetting log retention, so storage grows forever, one of the billing culprits from T.4.

## Done check
paste the Insights query + results + the alarm configuration.

## Links
- CloudWatch dashboards: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html
- Logs Insights queries: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html
- Alarms and notifications: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html
