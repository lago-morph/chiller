#!/bin/bash

cat kustomization_template.yaml /tmp/ttl_frontend_values.yaml /tmp/ttl_api_values.yaml /tmp/ttl_load_values.yaml > kustomization.yaml

cat > resources.yaml

kubectl kustomize

rm resources.yaml
rm kustomization.yaml
