# Self-check — EC2 + VPC + RDS (no XP, honor system)

Score 7+ before the boss fight.

## 1. What is the defining routing difference between a public and a private subnet?
<details><summary>Show answer</summary>
A public subnet has a route in its route table to the internet gateway, so it can reach the internet directly. A private subnet has no IGW route; if it needs outbound access, it goes through a NAT gateway. Databases belong in private subnets, always.
</details>

## 2. What breaks if you open the RDS security group to `0.0.0.0/0`?
<details><summary>Show answer</summary>
You have exposed the database port to the entire internet, so anyone can attempt connections and your only remaining defense is the password. The correct pattern is an SG-to-SG rule: allow the EC2 app's security group on the DB port, never a world-open CIDR. Even in a sandbox this is the habit you keep.
</details>

## 3. "My app can't reach the database." Which firewall do you check first, and why?
<details><summary>Show answer</summary>
Check the security groups first. The classic cause is that the DB's SG does not allow the app's SG. Security groups are stateful and attach to resources, so a missing inbound rule on the DB SG stops the connection no matter what the rest of the network looks like. NACLs are the second layer to check.
</details>

## 4. What breaks if a database instance lives in a public subnet?
<details><summary>Show answer</summary>
It instantly becomes reachable from the internet path, and you lose the main network boundary that protects it. A DB in a public subnet with an IGW route can be targeted directly; in a private subnet only resources you route to it, like your app, can connect. This is a design bug, not a tuning problem.
</details>

## 5. Stop an EC2 instance. What keeps billing, and why?
<details><summary>Show answer</summary>
The attached EBS volumes keep billing, because EBS is network-attached storage that persists independently of the instance. The instance compute charge stops, but the disk charge continues. Stopped does not mean deleted.
</details>

## 6. What is the difference between stopping and terminating an instance, in billing terms?
<details><summary>Show answer</summary>
Stopping releases the compute but keeps the EBS volume (and its charge). Terminating destroys the instance; by default the root volume is deleted with it, but any other unattached volumes and leftover snapshots still bill until you delete them. That is why Q4.5 explicitly cleans up unattached volumes and snapshots.
</details>

## 7. Why create an AMI from a configured instance?
<details><summary>Show answer</summary>
An AMI captures the OS plus your installed software as a machine image. Launching from it gives you a reproducible clone that already has your setup, so you stop redoing manual configuration. That is how the course has you terminate the original and launch a clone.
</details>

## 8. Why does an Elastic IP bill even when nothing is running?
<details><summary>Show answer</summary>
An Elastic IP is charged when it is allocated but not attached to a running resource. Holding a public address idle is the thing being billed, a classic surprise charge. Release unused Elastic IPs during teardown.
</details>

## 9. What breaks if you lose the private key for your key pair?
<details><summary>Show answer</summary>
You are locked out of the instance over SSH. By default there is no password fallback, and the private key cannot be regenerated from the public key. Recovery means a workaround such as detaching the volume to edit authorized keys, or simply relaunching. Treat the key as unrecoverable.
</details>

## 10. Why is a NAT gateway called out as a billing trap?
<details><summary>Show answer</summary>
A NAT gateway charges an hourly rate around the clock plus a data processing fee, so an idle one costs real money (about $32+/month). It exists to give private subnets outbound access. If nothing in the private subnet needs the internet, the NAT is pure cost and should not exist.
</details>
