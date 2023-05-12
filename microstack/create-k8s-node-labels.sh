# Add labels to the k8s nodes (after cluster is setup)
kubectl label nodes k8s-worker-1 disktype=ssd ostype=normal appstype=user flavor=medium
kubectl label nodes k8s-worker-2 disktype=ssd ostype=normal appstype=observability flavor=large
kubectl label nodes k8s-worker-3 disktype=ssd ostype=normal appstype=user flavor=small
kubectl label nodes k8s-worker-4 disktype=ssd ostype=normal appstype=user flavor=medium
kubectl label nodes k8s-worker-5 disktype=ssd ostype=normal appstype=user flavor=small
kubectl label nodes k8s-worker-6 disktype=ssd ostype=normal appstype=user flavor=small
kubectl label nodes k8s-worker-7 disktype=ssd ostype=normal appstype=user flavor=small
kubectl label nodes k8s-worker-8 disktype=ssd ostype=normal appstype=user flavor=tiny
kubectl label nodes k8s-worker-9 disktype=ssd ostype=normal appstype=user flavor=tiny
kubectl get no --show-labels