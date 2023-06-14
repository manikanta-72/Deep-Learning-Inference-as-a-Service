Steps:
** For serving from Docker

docker-compose up

** For serving from kubernetes

kubectl apply -f k8s


To start the service:

minikube service tfweb-load-balancer-service

**

  Server Url : http://127.0.0.1:8080/home
  
  Test Url : https://tensorflow.org/images/blogs/serving/cat.jpg
