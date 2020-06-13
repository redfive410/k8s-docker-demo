# Intro to k8s and docker

## Steps

### Install docker
```
https://docs.docker.com/get-docker/
```

### Install awscli
```
https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
```

### Install kubectl, virtualbox, minikube
```
https://kubernetes.io/docs/tasks/tools/install-minikube/
```

After the basics are installed and you can run minikube and kubectl you are ready for learning.
```
minikube start --driver=virtualbox
minikube ssh
minikube dashboard
```

### Create docker image and push to ECR

```
#task.py
import boto3

def main():
  print("Running task...")
  client = boto3.client('sts')
  response = client.get_caller_identity()
  print(response)

main()
```

```
# Dockerfile
FROM python:3.7.0a2-alpine3.6
COPY task.py /tmp
CMD python /tmp/task.py
```

```
# my-private-reg-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: private-reg
spec:
  containers:
  - name: private-reg-container
    image: ${REPO}/${NAMESPACE}/python-batch-job:latest
  imagePullSecrets:
  - name: regcred
```

Commands
```
# Test python task
python3.7 task.py

export REPO=[YOUR_REPO]
export NAMESPACE=[YOUR_NAMESPACE]
export AWS_ACCESS_KEY_ID=[YOUR_AWSKEY]
export AWS_SECRET_ACCESS_KEY=[YOUR_AWSSECRET]

# Build, Test and Push docker image
docker build .
docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY a4b868bd4c76
docker tag a4b868bd4c76 python-sample-job:latest
docker tag python-sample-job:latest $REPO/$NAMESPACE/python-sample-job:latest

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $REPO
docker push $REPO/$NAMESPACE/python-sample-job:latest

kubectl create secret generic regcred --from-file=.dockerconfigjson=$HOME/.docker/config.json --type=kubernetes.io/dockerconfigjson
kubectl create secret generic awscred --from-literal AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --from-literal AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# Fill out templated values and create pod
envsubst < my-private-reg-pod.yaml | kubectl apply -f -

kubectl get pods
kubectl logs private-reg
kubectl delete pod private-reg
```
