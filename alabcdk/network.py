from aws_cdk import (
  aws_ec2 as ec2
)
from constructs import Construct

def fetch_vpc(scope: Construct, id: str, *, vpc_name: str) -> ec2.IVpc:
  return ec2.Vpc.from_lookup(scope, id, vpc_name=vpc_name)

