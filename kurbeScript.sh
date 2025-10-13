#!/bin/bash
# kurbeScript.sh — Start and verify Minikube Kubernetes cluster

set -e  # Exit immediately if a command exits with a non-zero status

echo "Checking if Minikube is installed..."
if ! command -v minikube &> /dev/null; then
    echo "Minikube is not installed. Please install it first."
    exit 1
fi

echo "Checking if kubectl is installed..."
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install it first."
    exit 1
fi

echo "Starting Minikube cluster..."
minikube start --driver=docker

echo "Verifying Kubernetes cluster status..."
kubectl cluster-info

echo "Getting list of pods in all namespaces..."
kubectl get pods -A

echo "Done! Your Minikube cluster is up and running."
