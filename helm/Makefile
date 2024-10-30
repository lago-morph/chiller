define DOCS
Convenience helpers for Watch and Chill deployment

cicd           Installs with CI/CD images for current checked out branch
ttl            Installs with ttl.io images with files in /tmp

uninstall      Uninstalls helm chart


port-prom      Port forwarding for Prometheus
port-graf      Port forwarding for Grafana
port-load      Port forwarding for load testing
port-app       Port forwarding for accessing app locally

endef

define KHEADER
resources:
- resources.yaml

images:
endef

define KPOSTSH
#!/bin/bash
cat <&0 > resources.yaml
kubectl kustomize
endef

MAKEFLAGS += --jobs

CICD_TAG := $(shell git describe --tags)

.ONESHELL:

# dummy target does nothing when make without arguments
export DOCS
show-usage: 
	@echo "$$DOCS"

export KPOSTSH KHEADER
install-common:
	echo "$$KPOSTSH" > kpost.sh
	chmod a+x kpost.sh
	echo "$$KHEADER" > kustomization.yaml

ttl-debug: install-common
	cat /tmp/ttl_frontend_values.yaml /tmp/ttl_api_values.yaml /tmp/ttl_load_values.yaml >> kustomization.yaml
	helm install chiller ./chiller --post-renderer ./kpost.sh

ttl: ttl-debug
	rm kustomization.yaml
	rm kpost.sh
	rm resources.yaml

cicd-debug: install-common
	echo "- name: ghcr.io/lago-morph/chiller_frontend" >> kustomization.yaml
	echo "  newTag: $(CICD_TAG)" >> kustomization.yaml
	echo "- name: ghcr.io/lago-morph/chiller_load" >> kustomization.yaml
	echo "  newTag: $(CICD_TAG)" >> kustomization.yaml
	echo "- name: ghcr.io/lago-morph/chiller_api" >> kustomization.yaml
	echo "  newTag: $(CICD_TAG)" >> kustomization.yaml
	helm install chiller ./chiller --post-renderer ./kpost.sh

cicd: cicd-debug
	rm kustomization.yaml
	rm kpost.sh
	rm resources.yaml

uninstall:
	helm uninstall chiller

port-prom:
	kubectl port-forward -n monitoring --address=192.168.88.130 svc/prometheus-k8s 9090

port-graf:
	kubectl port-forward -n monitoring --address=192.168.88.130 svc/grafana 3000

port-load:
	kubectl port-forward --address=127.0.0.1 svc/chiller-frontend 8222:80

port-app:
	kubectl port-forward --address=192.168.88.130 svc/chiller-frontend 8080:80

