from aws_cdk import (
  aws_ec2 as ec2
)
from constructs import Construct
from typing import Sequence

def fetch_vpc(scope: Construct, id: str, *, vpc_name: str) -> ec2.IVpc:
  return ec2.Vpc.from_lookup(scope, id, vpc_name=vpc_name)

def get_private_subnet_ids(vpc: ec2.IVpc) -> Sequence[str]:
  isolated_subnet_ids = [subnet.subnet_id for subnet in vpc.isolated_subnets]
  private_subnet_ids = [subnet.subnet_id for subnet in vpc.private_subnets]
  return isolated_subnet_ids + private_subnet_ids
