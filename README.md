# K8s-Deployment-Verifier

```bash
python verifier.py --help
usage: verifier.py [-h] --deployment DEPLOYMENT [--namespace NAMESPACE] [--project PROJECT] [--zone ZONE] [--cluster CLUSTER] [--get-credentials GET_CREDENTIALS]

Simple tool to verify kubernetes deployments

optional arguments:
  -h, --help            show this help message and exit
  --deployment DEPLOYMENT, -d DEPLOYMENT
                        Deployment Name
  --namespace NAMESPACE, -n NAMESPACE
                        Namespace name
  --project PROJECT, -p PROJECT
                        GCP Project ID
  --zone ZONE, -z ZONE  GKE Cluster Zone
  --cluster CLUSTER, -c CLUSTER
                        Cluster Name
  --get-credentials GET_CREDENTIALS
                        Fetch GKE Kubectl credentials.
```
