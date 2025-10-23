# drone-plugin-catalog-ingestion

update idp catalog properties in harness pipelines

you can set multiple properties in a single step by using `PLUGIN_PROPERTIES` set to a json mapping of property names to values

```json
{
    "some_key": "some_value",
    "some_other_key": "some_other_value"
}
```

you can also set single keys by using `PLUGIN_PROPERTY` and `PLUGIN_VALUE`

to set all keys under a common prefix, use `PLUGIN_PREFIX`, for example `metadata.custom_properties`

## environment variables

- `PLUGIN_HARNESS_URL`: harness url (default: `https://app.harness.io`)
- `PLUGIN_HARNESS_PLATFORM_API_KEY`: harness platform api key
- `PLUGIN_HARNESS_ACCOUNT_ID`: harness account id

- `PLUGIN_MODE`: mode to use when updating properties (default: `append`)
- `PLUGIN_ENTITY_REF`: entity ref to update properties for
- `PLUGIN_PREFIX`: prefix to use when updating properties (example: `metadata.custom_properties`)

- `PLUGIN_PROPERTY`: property to update (optional, required if `PLUGIN_PROPERTIES` is not set)
- `PLUGIN_VALUE`: value to update property to (optional, required if `PLUGIN_PROPERTY` is set)

- `PLUGIN_PROPERTIES`: properties to update (optional, required if `PLUGIN_PROPERTY` is not set)
- `PLUGIN_SUB_PROPERTIES`: sub property to access from `PLUGIN_PROPERTIES` to use for update (optional)

## usage

```yaml
- step:
    type: Plugin
    name: Add IDP Properties
    identifier: add_idp_properties
    spec:
        connectorRef: account.harnessImage
        image: harnesscommunity/drone-plugin-catalog-ingestion
        settings:
            HARNESS_URL: app.harness.io
            HARNESS_PLATFORM_API_KEY: <+secrets.getValue("account.account_admin")>
            HARNESS_ACCOUNT_ID: <+account.identifier>
            PROPERTIES: "{\"some_property\":\"some_value\"}"
            MODE: append
            ENTITY_REF: resource:account.<+org.identifier>.<+project.identifier>/ansible_step_group_template
            PREFIX: metadata.custom_properties
```