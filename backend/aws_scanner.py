import boto3

def scan_ec2():
    ec2 = boto3.client("ec2")
    instances = ec2.describe_instances()
    return {"ec2_instances": instances}

def scan_s3():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()
    findings = []
    for bucket in buckets["Buckets"]:
        acl = s3.get_bucket_acl(Bucket=bucket["Name"])
        findings.append({"bucket": bucket["Name"], "acl": acl})
    return {"s3_buckets": findings}

def scan_iam():
    iam = boto3.client("iam")
    users = iam.list_users()
    return {"iam_users": users}

def scan_all():
    return {
        "ec2": scan_ec2(),
        "s3": scan_s3(),
        "iam": scan_iam(),
    }
