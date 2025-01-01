# Weather App

The **Weather App** is a  simple Flask-based web application designed to provide users with a 7-day weather forecast for any city. This project emphasizes DevOps practices with automated infrastructure provisioning, CI/CD pipelines, and Kubernetes deployment on AWS EKS.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation and Setup](#installation-and-setup)
3. [Usage](#usage)
4. [Infrastructure as Code (IaC) Details](#infrastructure-as-code-iac-details)
5. [Continuous Integration/Continuous Deployment (CI/CD) Pipeline](#continuous-integrationcontinuous-deployment-cicd-pipeline)
6. [Kubernetes Deployment](#kubernetes-deployment)
7. [Configuration](#configuration)
8. [Testing](#testing)
9. [Contributing](#contributing)
10. [License](#license)
11. [Contact Information](#contact-information)
12. [Acknowledgments](#acknowledgments)

---

## Prerequisites
- **Python**: Version 3.11+
- **Docker**: Installed and running
- **Kubernetes**: `kubectl` configured for your cluster
- **AWS CLI**: Configured with appropriate access keys
- **Terraform**: Installed on your local machine
- **Jenkins**: Installed with Docker and Kubernetes plugins

---

## Installation and Setup

### Local Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd weather-app
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the application locally:
   ```bash
   python src/app.py
   ```

4. Access the app at `http://127.0.0.1:5000`.

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t your-dockerhub-username/weather-app:latest .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 your-dockerhub-username/weather-app:latest
   ```

---

## Usage
- Open the application in your browser.
- Enter a city name in the search bar to fetch the 7-day weather forecast.
- View day/night temperatures and humidity levels for the selected city.

---

## Infrastructure as Code (IaC) Details

### Overview
- **Cloud Provider**: AWS
- **Services Used**:
  - EKS for Kubernetes cluster
  - VPC with subnets and NAT gateways

### Tools
- **Terraform**: Used to provision the infrastructure.

### Setup Instructions
1. Navigate to the Terraform directory:
   ```bash
   cd terraform
   ```

2. Initialize and apply Terraform:
   ```bash
   terraform init
   terraform apply
   ```

3. Configure `kubectl` to connect to the EKS cluster:
   ```bash
   aws eks update-kubeconfig --region <AWS_REGION> --name <CLUSTER_NAME>
   ```

---

## Continuous Integration/Continuous Deployment (CI/CD) Pipeline

### Build Pipeline (`build.Jenkinsfile`)
- **Stages**:
  1. Cleanup
  2. Install Requirements
  3. Pylint Test
  4. Docker Build
  5. Smoke Test
  6. Tag and Push to DockerHub
  7. Trigger Deploy Pipeline

### Deploy Pipeline (`deploy.Jenkinsfile`)
- **Stages**:
  1. Cleanup
  2. Deploy to EKS

---

## Kubernetes Deployment

### Deployment Manifest (`k8s-manifest/deployment.yaml`)
- Deploys 2 replicas of the Weather App container.

### Service Manifest (`k8s-manifest/service.yaml`)
- Exposes the app on a NodePort (port 5000).

### Deployment Steps
1. Apply Kubernetes manifests:
   ```bash
   kubectl apply -f k8s-manifest/deployment.yaml
   kubectl apply -f k8s-manifest/service.yaml
   ```

2. Verify deployment:
   ```bash
   kubectl get pods -n weather-app
   kubectl get svc -n weather-app
   ```

---

## Configuration

### Environment Variables
- `APP_NAME`: Application name
- `REGISTRY_URL`: DockerHub registry URL
- `AWS_REGION`: AWS region for deployment
- `KUBECONFIG_CREDENTIALS_ID`: Jenkins credentials ID for Kubernetes config

### Configuration Files
- **Terraform**:
  - `main.tf`, `vpc.tf`, `eks-cluster.tf`: Define AWS infrastructure.
- **Jenkinsfiles**:
  - `build.Jenkinsfile`, `deploy.Jenkinsfile`: Define CI/CD pipelines.

---

## Testing

### Unit Tests
1. Run Pylint for static code analysis:
   ```bash
   pylint src/*.py
   ```

2. Run Python unit tests:
   ```bash
   python -m unittest discover src/tests
   ```

### Smoke Tests
1. Test app connectivity:
   ```bash
   python src/tests/check-connectivity.py
   ```

### Selenium Tests
1. Ensure Selenium WebDriver is installed.
2. Run:
   ```bash
   python src/tests/test-selenium.py
   ```

---

## Contributing
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Submit a pull request for review.

---

## License
This project is licensed under the MIT License.

---

## Contact Information
- **Maintainer**: Your Name
- **Email**: your-email@example.com

---

## Acknowledgments
- **OpenMeteo API**: For weather data
- **Terraform AWS Modules**: For infrastructure setup
- **Jenkins Community**: For CI/CD support


