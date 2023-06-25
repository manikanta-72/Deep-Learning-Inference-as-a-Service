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
![alt_text](https://github.com/manikanta-72/Deep-Learning-Inference-as-a-Service/blob/main/final_sd.jpg)

# Application Workflow

## User workflow
A client can use inference service by interacting with web application through either API requests or web browser. As web applications are being run in Google Cloud Platform(GCP), users can access it from any web browser or device. Clients need to provide input(Images for this project) and a query that they need to infer(Currently, Is it a cat or not ?). The backend of the system then processes the request and replies back the answer. We use HTTP protocol for communication between users and web applications.

## Application Middleware
As soon as the user provides their query, these queries are then pushed to RabbitMQ. Here Web Applications acts as a publisher to RabbitMQ. In order to get the processed output back to the publisher for a remote consumer we implemented the RPC procedure with RabbitMQ. When a publisher publishes a message to the queue, it passes along a unique identifier for the message and information about the callback queue to which the consumer has to write the messages.

![alt_text](https://github.com/manikanta-72/Deep-Learning-Inference-as-a-Service/blob/main/rabbit_rpc%20(1).jpg)

When RabbitClient(consumer) receives a message from a web application through RabbitMQ. It queries the ML Model server for further processing of images and inferences. Upon receiving a response from ML Model, it sends the response with a unique identifier along the callback queue it received as part of the query. We can use ‘routing keys’ to manage multiple queues and a variety of queries.

## ML Model Server:
We use a pre-trained object detection computer vision model Resnet. Resnet is trained on the ImageNet dataset which contains 1000 classes. We use this model to predict whether the given image is a cat or dog. As part of the project we serve two different models one for cat detection and other for dog detection. Apart from these tasks we can have any number and variety of ML models as our backend. Each of these models host a web server to process the requests. And each of them can be containerized as an individual image. In addition, our ML model server also
keeps updated with the latest model. We periodically fetch the latest model from the TensorFlow server. To prevent any downtime during the model update, we used a rolling deployment strategy where the old pods are deleted one by one as the new pods with the latest model update them.

# Steps to run:
** For serving from Docker

docker-compose up

** For serving from kubernetes

kubectl apply -f k8s


To start the service:

minikube service tfweb-load-balancer-service

**

  Server Url : http://127.0.0.1:8080/home
  
  Test Url : https://tensorflow.org/images/blogs/serving/cat.jpg
