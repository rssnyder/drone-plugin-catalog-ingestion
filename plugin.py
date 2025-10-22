from os import getenv
from sys import exit

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
    mode = check_env("PLUGIN_MODE")
    entity_ref = check_env("PLUGIN_ENTITY_REF")
    properties = check_env("PLUGIN_PROPERTIES", {})
    prefix = check_env("PLUGIN_PREFIX", "")

    resp = post(
        f"{url}/v1/catalog/custom-properties/entity?dry_run=false",
        headers={
            "Content-Type": "application/json",
            "Harness-Account": account_id,
            "x-api-key": token,
        },
        json={
            "entity_ref": entity_ref,
            "properties": [
                {"property": prefix + property, "value": value, "mode": mode}
                for property, value in properties.items()
            ],
        },
    )

    resp.raise_for_status()

    write_outputs(
        {"status": resp.json().get("status", "unknown"), "response": resp.status_code}
    )


if __name__ == "__main__":
    main()
