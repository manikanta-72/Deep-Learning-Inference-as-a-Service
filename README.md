# Project Goal:
Aim to design and implement a highly available and highly scalable distributed system that can offer Deep Learning Inference-As-A-Service. Application will have two main components: 1) Web Interface, and 2) Backend to process the request. Implement containerization and Google Cloud Platform(GCP) to scale and test application.

# Design Formulation:
In order to facilitate a high volume of uses we add a load balancer and horizontal scaling of resources. Then we decoupled our web interface and backend to optimize the resources for sporadic requests. Furthermore, to exploit batching and support multi-queries we added a queue connecting the web application and ML backend. To test our application in distributed deployment we use cloud services and evaluate metrics.

# Frameworks Used:
1. Docker - To containerize application
2. Kubernetes & Kubernetes pods - To maintian and orchestrate containers
3. RabbitMQ - To batch ML requests and facilitate running multiple ML models
4. Tensorflow Serving - To serve ML models
5. GCP - To increase availability and testing.

# System Design


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
