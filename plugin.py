from os import getenv
from sys import exit
from json import loads

from requests import post


def write_outputs(outputs: dict[str, str]):
    """
    write key value outputs to a local file to be rendered in the plugin step

    args:
        outputs (dict[str, str]): string to string mappings
    """

    output_file = open(getenv("DRONE_OUTPUT"), "a")

    for k, v in outputs.items():
        output_file.write(f"{k}={v}\n")

    output_file.close()


def write_secret_outputs(outputs: dict[str, str]):
    """
    write key value outputs to a local file to be rendered in the plugin step as secret

    args:
        outputs (dict[str, str]): string to string mappings
    """

    output_file = open(getenv("HARNESS_OUTPUT_SECRET_FILE"), "a")

    for k, v in outputs.items():
        output_file.write(f"{k}={v}\n")

    output_file.close()


def check_env(variable: str, default: str = None):
    """
    resolves an environment variable, returning a default if not found
    if no default is given, variable is considered required and must be set
    if not, print the required var and fail the program

    args:
        variable (str): environment variable to resolve
        default (str): default value for variable if not found

    returns:
        str: the value of the variable
    """

    value = getenv(variable, default)
    if value == None:
        # if we are missing a PLUGIN_ var, ask the user for the expected setting
        stripped_variable = variable if "PLUGIN_" not in variable else variable[7:]
        print(f"{stripped_variable} required")
        exit(1)

    return value


def main():
    url = check_env("PLUGIN_HARNESS_URL", "https://app.harness.io")
    token = check_env("PLUGIN_HARNESS_PLATFORM_API_KEY")
    account_id = check_env("PLUGIN_HARNESS_ACCOUNT_ID")

    mode = check_env("PLUGIN_MODE", "append")
    entity_ref = check_env("PLUGIN_ENTITY_REF")
    prefix = check_env("PLUGIN_PREFIX", "")
    if not prefix.endswith("."):
        prefix += "."

    property = check_env("PLUGIN_PROPERTY", "")
    value = check_env("PLUGIN_VALUE", "")

    properties = loads(check_env("PLUGIN_PROPERTIES", "{}"))
    sub_properties = check_env("PLUGIN_SUB_PROPERTIES", "")

    payload = {"entity_ref": entity_ref}

    if properties:
        # unpack properties to find nested properties we need
        if sub_properties:
            properties_copy = properties.copy()
            for prop in sub_properties.split("."):
                properties_copy = properties_copy[prop]
            properties = properties_copy

        payload["properties"] = [
            {"property": prefix + property, "value": value, "mode": mode}
            for property, value in properties.items()
        ]
    elif property:
        payload["properties"] = [
            {"property": prefix + property, "value": value, "mode": mode}
        ]
    else:
        raise ValueError("No PROPERTIES or PROPERTY provided")

    resp = post(
        f"{url}/v1/catalog/custom-properties/entity?dry_run=false",
        headers={
            "Content-Type": "application/json",
            "Harness-Account": account_id,
            "x-api-key": token,
        },
        json=payload,
    )

    resp.raise_for_status()

    write_outputs(
        {"status": resp.json().get("status", "unknown"), "response": resp.status_code}
    )

    print(resp.text)


if __name__ == "__main__":
    main()
