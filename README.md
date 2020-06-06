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
# task.py
import time

print('Task starting...')
time.sleep(5)
print('Task ended, took 5 seconds')
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
    image: 000000000000.dkr.ecr.us-west-2.amazonaws.com/area51/python-batch-job:latest
  imagePullSecrets:
  - name: regcred
```

Commands
```
# Test python task
python3.7 task.py

# Build, Test and Push docker image
docker build .
docker run 7490baba874b
docker tag 7490baba874b python-batch-job:latest
docker tag python-batch-job:latest 000000000000.dkr.ecr.us-west-2.amazonaws.com/area51/python-batch-job:latest

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 000000000000.dkr.ecr.us-west-2.amazonaws.com
docker push 000000000000.dkr.ecr.us-west-2.amazonaws.com/area51/python-batch-job:latest

# Pull docker image from ECR and run python task
kubectl create secret generic regcred --from-file=.dockerconfigjson=/Users/username/.docker/config.json --type=kubernetes.io/dockerconfigjson
kubectl apply -f my-private-reg-pod.yaml
kubectl get pods
kubectl logs private-reg
kubectl delete pod private-reg
```
