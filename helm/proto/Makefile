target-required:

check:
	kubectl get pods,deployments,replicasets,cm,secrets,services -l component!=apiserver

test-curl:
	curl 192.168.88.130:8081/user/login

port-forward:
	kubectl port-forward service/chiller-frontend --address=192.168.88.130 8081:80

delete-all: delete-api delete-frontend delete-db delete-cm delete-secret

create-all: create-frontend create-api create-db

create-secret:
	kubectl apply -f db-auth-secret.yaml

create-cm:
	kubectl apply -f schema-cm.yaml

create-db: create-cm create-secret
	kubectl apply -f db-pod.yaml
	kubectl apply -f db-service.yaml

create-api: create-secret
	kubectl apply -f api-deployment.yaml
	kubectl apply -f api-service.yaml

create-frontend:
	kubectl apply -f frontend-deployment.yaml
	kubectl apply -f frontend-service.yaml

delete-api:
	kubectl delete deployment chiller-api
	kubectl delete service chiller-api

delete-frontend:
	kubectl delete deployment chiller-frontend
	kubectl delete service chiller-frontend

delete-db:
	kubectl delete pod db
	kubectl delete service db

delete-cm:
	kubectl delete cm schema

delete-secret:
	kubectl delete secret db-auth

