#!/bin/bash

echo "Starting Assignment 3 Kubernetes deployment..."

echo "Applying Kubernetes manifests..."

kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/mysql-secret.yml
kubectl apply -f k8s/flask-configmap.yml
kubectl apply -f k8s/mysql-pv.yml
kubectl apply -f k8s/mysql-pvc.yml
kubectl apply -f k8s/mysql-deployment.yml
kubectl apply -f k8s/mysql-service.yml
kubectl apply -f k8s/flask-deployment.yml
kubectl apply -f k8s/flask-service.yml
kubectl apply -f k8s/nginx-configmap.yml
kubectl apply -f k8s/nginx-deployment.yml
kubectl apply -f k8s/nginx-service.yml

echo "Waiting for pods to become ready..."
kubectl wait --for=condition=ready pod --all -n assignment3 --timeout=300s

echo "Deployment status:"
kubectl get all -n assignment3

echo "Application URL:"
echo "http://$(minikube ip):3008
