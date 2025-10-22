#!/bin/sh

curl -i -X POST \
  "https://$PLUGIN_HARNESS_URL/v1/catalog/custom-properties/entity?dry_run=false" \
  -H 'Content-Type: application/json' \
  -H "Harness-Account: $PLUGIN_HARNESS_ACCOUNT_ID" \
  -H "x-api-key: $PLUGIN_HARNESS_PLATFORM_API_KEY" \
  -d '{
    "property": "'${PLUGIN_PROPERTY}'",
    "value": "'${PLUGIN_VALUE}'",
    "mode": "'${PLUGIN_MODE}'",
    "entity_ref": "'${PLUGIN_ENTITY_REF}'"
  }'
