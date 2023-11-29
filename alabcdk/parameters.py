from aws_cdk import aws_kms as kms, aws_ssm as ssm, ArnFormat, ArnComponents, Arn, Stack
from constructs import Construct
from typing import Union, Tuple


def fetch_parameter(scope: Construct, id: str, *, name: str) -> ssm.StringParameter:
    return ssm.StringParameter.from_string_parameter_name(scope, id, name)


def read_parameter(scope: Construct, name: str) -> Union[str, None]:
    try:
        return ssm.StringParameter.value_from_lookup(scope, name)
    except Exception:
        return None


def read_arn_parameter(
    scope: Construct, *, name: str, service: str, resource: str, resource_sep: str = "/"
) -> Union[str, None]:
    try:
        value = ssm.StringParameter.value_from_lookup(scope, name)
        if value.startswith("dummy-value-for"):
            stack = Stack.of(scope)
            arn_format = (
                ArnFormat.SLASH_RESOURCE_NAME
                if resource_sep == "/"
                else ArnFormat.COLON_RESOURCE_NAME
            )
            components = ArnComponents(
                resource=resource,
                resource_name="dummy",
                service=service,
                partition="aws",
                arn_format=arn_format,
            )
            return Arn.format(components=components, stack=stack)
        else:
            return value
    except Exception:
        return None


def add_parameter(scope, id: str, *, name: str, value: str) -> ssm.StringParameter:
    return ssm.StringParameter(scope, name, parameter_name=name, string_value=value)


def read_encryption_key(
    scope: Construct, id: str, *, name: str
) -> Tuple[Union[kms.IKey, None], Union[str, None]]:
    key_arn = read_arn_parameter(scope, name=name, service="kms", resource="key")
    if key_arn is None:
        return None, f"Could not read value from {name}"
    else:
        try:
            return kms.Key.from_key_arn(scope, id, key_arn), None
        except Exception as e:
            return None, f"Could not get encryption key: {str(e)}"
