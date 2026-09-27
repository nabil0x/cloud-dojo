# T.4 — Budgets and alarms (25 XP)

**Phase:** Track T — Real-AWS Parallel Track

## Concept
On real AWS, forgetting to delete something can cost money, so you build the safety net first.
A budget watches your spend and emails you when it crosses a threshold; Cost Anomaly Detection watches for spend patterns that look unusual and tells you about them.
In this quest you create a one-dollar budget with an alert and turn on anomaly detection.
Then you learn the rogues' gallery of surprise-bill causes: the services that quietly charge while you think nothing is running.
Emulators never bill you, which is exactly why this instinct has to be built here, on the one track that is real.
Money is the lesson an emulator can never teach, so treat this quest as mandatory before you create anything else.

## Uses
- Catching runaway spend within days instead of at the end of the month.
- Getting an automatic warning when usage suddenly spikes.
- Budgeting for learning, so a lab never turns into a surprise invoice.
- Reviewing the usual culprits before you create any resources.
- Setting a habit that protects every later phase, on real or shared accounts.

## Key info
- Create a $1 budget with an email alert in AWS Budgets.
- Enable Cost Anomaly Detection for automatic unusual-spend notices.
- Top surprise-bill culprits to know cold: NAT Gateway (hourly plus data, 24/7), idle Elastic IP, outbound data transfer, EBS volumes on stopped EC2 instances, public IPv4 addresses, and CloudWatch Logs with no retention policy.
- Budgets and anomaly detection live in the billing and cost management console.
- Delete or stop resources after each session. Sandboxes auto-clean; real accounts do not.
- This runs on real AWS only, because only a real account sends a real bill.
- Tag resources so you can find and delete them later without guesswork.
- A budget alerts, it does not stop spend. Deleting resources is still your job.

## Pitfalls
- Creating a budget but no alert, so it never reaches you.
- Assuming stopped means free. A stopped EC2 instance still bills its EBS volumes.
- Leaving CloudWatch Logs with retention set to never expire, so storage grows forever.

## Done check
paste the budget confirmation + your own one-line explanation of each culprit.

## Links
- Managing costs with AWS Budgets: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- Avoiding unexpected charges: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/checklistforunwantedcharges.html
- Cost Anomaly Detection: https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html
