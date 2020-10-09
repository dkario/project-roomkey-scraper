import boto3
import json
import os


def get_secret(secret_name_env_var, is_json=False):
    secret_name = os.getenv(secret_name_env_var)

    ssm = boto3.client("ssm")
    secret = ssm.get_parameter(Name=secret_name, WithDecryption=True)["Parameter"][
        "Value"
    ]

    return json.loads(secret) if is_json else secret
