import json
from .utils import gen_name
from constructs import Construct
from aws_cdk import RemovalPolicy, SecretValue, aws_kms as kms, aws_secretsmanager as sm


def define_db_secret(
    scope: Construct,
    *,
    name: str,
    description: str,
    encryption_key: kms.IKey = None,
    host: str = "no-host",
    db_engine: str,
    username: str,
    password: str = None
) -> sm.Secret:
    secret_structure = {
        "engine": db_engine,
        "host": host,
        "username": username,
    }
    gen_secret = sm.SecretStringGenerator(
        secret_string_template=json.dumps(secret_structure),
        generate_string_key="password",
        exclude_punctuation=True,
        password_length=32,
    )
    set_secret = {
        "engine": SecretValue.unsafe_plain_text(db_engine),
        "host": SecretValue.unsafe_plain_text(host),
        "username": SecretValue.unsafe_plain_text(username),
    }
    if password is not None:
        set_secret["password"] = SecretValue.unsafe_plain_text(password)

    secret = sm.Secret(
        scope,
        gen_name(scope, name),
        description=description,
        removal_policy=RemovalPolicy.DESTROY,
        secret_name=name,
        encryption_key=encryption_key,
        generate_secret_string=gen_secret if password is None else None,
        secret_object_value=set_secret if password is not None else None,
    )
    return secret
