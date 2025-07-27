import json
import os
import boto3
from datetime import datetime

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

def determine_severity(rule_name: str) -> str:
    """Simple mapping of Config rule names to severity levels."""
    high = {
        "s3-bucket-public-access-prohibited",
        "iam-root-access-key-check",
        "encrypted-volumes",
    }
    return "HIGH" if rule_name in high else "MEDIUM"


def send_notification(message: str):
    """Publish alert to SNS if topic configured."""
    if not SNS_TOPIC_ARN:
        return
    sns = boto3.client("sns")
    sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="AWS Compliance Alert")


def lambda_handler(event, context):
    """Entry point for Config compliance change events."""
    # Allow invocation by multiple sources; guard for missing keys
    detail = event.get("detail", {})
    rule_name = detail.get("configRuleName", "unknown")
    resource_id = detail.get("resourceId", "unknown")
    account_id = detail.get("awsAccountId", "unknown")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "rule": rule_name,
        "resource_id": resource_id,
        "account_id": account_id,
        "severity": determine_severity(rule_name),
        "request_id": context.aws_request_id,
    }

    # Structured log for CloudWatch
    print(json.dumps({"compliance_violation": log_entry}))

    if log_entry["severity"] == "HIGH":
        msg = (
            f"HIGH severity compliance violation detected\nRule: {rule_name}\n"
            f"Resource: {resource_id}\nAccount: {account_id}\nTime: {log_entry['timestamp']}"
        )
        send_notification(msg)

    return {"statusCode": 200, "body": "Processed compliance event"}
