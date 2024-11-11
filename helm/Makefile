define DOCS
Convenience helpers for Watch and Chill deployment

cicd           Installs with CI/CD images for current checked out branch
ttl            Installs with ttl.io images with files in /tmp

uninstall-chiller      Uninstalls chiller

port-prom      Port forwarding for Prometheus
port-graf      Port forwarding for Grafana
port-load      Port forwarding for load testing
port-app       Port forwarding for accessing app locally

prom-stack     Installs the kube-prometheus-stack community Helm chart
uninstall-prom-stack  Uninstalls the prometheus stack

get-ingress    Shows the URL for the ingress to an AWS ALB

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

CICD_TAG := $(shell git describe --tags --abbrev=0)

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

uninstall-chiller:
	helm uninstall chiller

port-prom:
	kubectl port-forward -n monitoring --address=192.168.88.130 svc/prometheus-operated 9090

port-graf:
	kubectl port-forward -n monitoring --address=192.168.88.130 svc/kube-prometheus-stack-grafana 3000:80

port-load:
	kubectl port-forward --address=127.0.0.1 svc/chiller-frontend 8222:80

port-app:
	kubectl port-forward --address=192.168.88.130 svc/chiller-frontend 8080:80

cicd:
	helm install chiller ./chiller --set appTag=$(CICD_TAG)

prom-stack:
	helm install prom-stack prometheus-community/kube-prometheus-stack --set grafana.adminPassword=admin --create-namespace --namespace monitoring

uninstall-prom-stack:
	helm uninstall prom-stack --namespace monitoring
	kubectl delete crd alertmanagerconfigs.monitoring.coreos.com
	kubectl delete crd alertmanagers.monitoring.coreos.com
	kubectl delete crd podmonitors.monitoring.coreos.com
	kubectl delete crd probes.monitoring.coreos.com
	kubectl delete crd prometheusagents.monitoring.coreos.com
	kubectl delete crd prometheuses.monitoring.coreos.com
	kubectl delete crd prometheusrules.monitoring.coreos.com
	kubectl delete crd scrapeconfigs.monitoring.coreos.com
	kubectl delete crd servicemonitors.monitoring.coreos.com
	kubectl delete crd thanosrulers.monitoring.coreos.com

get-ingress:
	kubectl get ingress ingress-chiller -o json | jq .status.loadBalancer.ingress[0].hostname | sed -e "s/\"//g" | sed -e "s/^/http:\/\//"
