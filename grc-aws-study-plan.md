# GRC Engineering for AWS – 10-Week Study Plan

> A hands-on path that follows *GRC Engineering for AWS: A Hands-On Guide to Governance, Risk, and Compliance Engineering* by AJ Yawn.  Each week produces portfolio artifacts you can publish.

---
## Week-0 – Environment Prep (2-4 h)
• Create AWS Organization (mgmt + 2 member accounts, free-tier).  
• Install AWS CLI, SAM/CFN CLI, Git, Python 3.11, VS Code.  
• Clone book repo: `git clone https://github.com/ajy0127/thegrcengineeringbook.git`  
• Create private repo `grc-engineering-portfolio` for all lab work.

---
## Section 1 – Foundations
### Week 1 – Ch 1-2
1. Read Ch 1 *First-Principles Revolution* & Ch 2 *GRC Engineering 101*.  
2. Write a one-page press release (Amazon “working-backwards” style) describing an ideal future-state compliance program.  
3. Commit to portfolio repo (`docs/press-release.md`).

### Week 2 – Ch 3 – *Bootstrap Baseline Compliance*
1. **Enable AWS Config** in sandbox Account A  
   a. Console → Config → *Get started* → *Record all resources* → *Include global resources*.  
2. **Add 3 managed rules**:  
   • `s3-bucket-server-side-encryption-enabled`  
   • `iam-password-policy`  
   • `ec2-instance-managed-by-ssm`  
3. **Start AWS Audit Manager**  
   a. Audit Manager → *Create assessment* → Framework = *A﻿WS Foundational Security* → link to Config.  
4. Verify evidence appears in assessment dashboard.  
5. Document commands & screenshots in `runbooks/bootstrap-compliance.md`.

---
## Section 2 – AWS Fundamentals
### Week 3 – Ch 4 – *Core AWS Security Services*
1. **Org CloudTrail** (management account)  
   `aws cloudtrail create-trail --name org-trail --is-organization-trail --s3-bucket-name org-trail-logs --enable-log-file-validation`
2. **GuardDuty**  
   a. Enable delegated admin.  
   b. `aws guardduty create-detector --enable` in each member via delegated script.
3. **Security Hub**  
   a. Delegated admin → *Settings* → *Enable organization*.  
4. Commit CFN/Terraform definitions to `infra/security-baseline/` and push screenshots.

### Week 4 – Ch 5 – *Infrastructure as Code (IaC)*
**Lab 1 – Convert baseline to IaC**  
1. Export current Config/GuardDuty/Security Hub settings.  
2. Translate into CloudFormation YAML or Terraform HCL.  
3. Validate (`cfn-lint` or `terraform validate`) and deploy to dev account.

**Lab 2 – Org Guardrail (SCP)**  
1. Policy JSON in `scp/deny-all-ec2.json`.  
2. Create & attach:
```bash
POLICY_ID=$(aws organizations create-policy \
  --name "DenyAllEC2" \
  --type SERVICE_CONTROL_POLICY \
  --content file://scp/deny-all-ec2.json \
  --query 'Policy.PolicySummary.Id' --output text)
aws organizations attach-policy --policy-id $POLICY_ID --target-id <ACCOUNT_ID>
```
3. Test in target account: `aws ec2 describe-instances` → expect *AccessDenied*.

### Week 5 – Ch 6 – *Event-Driven Architecture*
**Lab 1 – Lambda Compliance Logger**  
1. `cd labs/lambda-violation-logger`  
2. Build & deploy: `sam build && sam deploy --guided` (runtime Python 3.11).  
3. Note Lambda ARN for next lab.

**Lab 2 – EventBridge Rule & Alerting**  
1. Create EventBridge rule:  
   • Source = `aws.config`  
   • DetailType = `Config Rules Compliance Change`  
   • Filter where `complianceType` = `NON_COMPLIANT`.  
2. Target = Lambda ARN; add SNS topic `compliance-alerts` email subscription.  
3. **Test**: Make an S3 bucket public in dev account → verify Lambda log + email.  
4. **Reflection**: In `journal.md` record mean-time-to-remediate vs weekly scan baseline.


---
## Section 3 – Python for GRC
### Week 6 – Ch 7-8
• Write Python script listing all S3 buckets + encryption status across Org; export CSV.  
• Add GitHub Action to run nightly.

### Week 7 – Ch 9 FAFO Case Study
• Fork FAFO repo; deploy in sandbox.  
• Submit two PRs: documentation fix & new control check.  
• Write blog/LinkedIn post summarizing lessons.

---
## Section 4 – Career & Portfolio
### Week 8 – Ch 10 Skills Matrix
• Self-assess technical & soft skills; draft 90-day up-skill plan.

### Week 9 – Ch 11 Portfolio
• Publish GitHub repo with READMEs.  
• Record 3-min Loom tour of event-driven pipeline; link in README.

### Week 10 – Ch 12-13 Interview & Brand
• Draft STAR stories from labs.  
• Update LinkedIn headline: *GRC Engineer | AWS Security Automation*.  
• Conduct mock interview.

---
## Ongoing (post-plan)
• Monthly: run automated access review; archive report in Audit Manager.  
• Quarterly: add one new Config rule + remediation.  
• Annually: present automation lessons to security leadership.

---
### Tracking
Use GitHub Projects board → *To Do | In Progress | Done*.  
Commit at least one artifact + `journal.md` reflection each week.

---
**Outcome:** Org-wide guardrails, event-driven remediation, continuous evidence, and a public portfolio that proves your GRC engineering skills.
