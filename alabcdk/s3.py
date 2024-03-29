from typing import Sequence
from .utils import (
    gen_name,
    get_params,
    remove_params,
    stage_based_removal_policy,
    generate_output,
)
from constructs import Construct
from aws_cdk import aws_s3, aws_iam, aws_lambda


class Bucket(aws_s3.Bucket):
    def grant_access(self, *, grantees, grantfunc, env_var_name) -> None:
        for grantee in grantees:
            grantfunc(grantee)
            if isinstance(grantee, aws_lambda.Function):
                grantee.add_environment(env_var_name, self.bucket_name)

    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
        readers: Sequence[aws_iam.IGrantable] = None,
        writers: Sequence[aws_iam.IGrantable] = None,
        readers_writers: Sequence[aws_iam.IGrantable] = None,
        env_var_name: str = None,
        **kwargs
    ):
        """
        Creates an S3 bucket, using some sensible defaults for security.

        See https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
        for a detailed description of parameters.

        - :param bucket_name: defaults to gen_name(scope, id) if not set
        """
        kwargs = get_params(locals())

        # Set the name to a standard
        bucket_name = gen_name(
            scope, id, globalize=True, all_lower=True, clean_string=True
        )

        kwargs.setdefault("bucket_name", bucket_name)
        kwargs.setdefault("removal_policy", stage_based_removal_policy(scope))
        remove_params(kwargs, ["env_var_name", "readers", "writers", "readers_writers"])

        super().__init__(scope, id, **kwargs)
        env_var_name = env_var_name or id
        generate_output(self, env_var_name, self.bucket_name)

        self.grant_access(
            grantees=readers or [], grantfunc=self.grant_read, env_var_name=env_var_name
        )
        self.grant_access(
            grantees=writers or [],
            grantfunc=self.grant_write,
            env_var_name=env_var_name,
        )
        self.grant_access(
            grantees=readers_writers or [],
            grantfunc=self.grant_read_write,
            env_var_name=env_var_name,
        )
