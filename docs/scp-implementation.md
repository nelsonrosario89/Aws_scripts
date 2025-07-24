# AWS Service Control Policy (SCP) Implementation

## Overview
[Previous content remains the same...]

# AWS Service Control Policy (SCP) Implementation

## Overview
This document outlines the implementation of Service Control Policies (SCPs) to restrict EC2 access in the AWS Organization.

## Environment Details
- **Management Account ID**: 295070998992 (NR-TRAINING-AWS-GENERAL)
- **Target Account ID**: 097089567108 (NR-TRAINING-AWS-PRODUCTION)
- **Region**: us-east-1
- **SCP Policy Type**: Enabled on Root (r-clm4)

## SCP Policy

### Policy: DenyAllEC2
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "ec2:*",
      "Resource": "*"
    }
  ]
}
- AWSConfigServiceRole is now managed by CloudFormation stack `security-config-role` (Week 4 IaC)
