#!/bin/bash
set -e

echo "Creating kind cluster..."
kind create cluster --config infrastructure/kind-config.yaml || true

echo "Building Docker images..."
docker build -t app1:latest ./App1
docker build -t app2:latest ./App2
docker build -t app3:latest ./App3

echo "Loading images into kind..."
kind load docker-image app1:latest
kind load docker-image app2:latest
kind load docker-image app3:latest

echo "Deploying to Kubernetes..."
kubectl apply -f infrastructure/redis.yaml
kubectl apply -f App1/deployment.yaml
kubectl apply -f App2/deployment.yaml
kubectl apply -f App3/deployment.yaml

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=redis --timeout=120s
kubectl wait --for=condition=ready pod -l app=app1 --timeout=120s
kubectl wait --for=condition=ready pod -l app=app2 --timeout=120s
kubectl wait --for=condition=ready pod -l app=app3 --timeout=120s

echo "Deployment complete! Apps are running."
