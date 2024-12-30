pipeline {
    agent {
        node {
         label 'deploy'
        }
    }
      environment {
        AWS_REGION = 'AWS_REGION' 
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-credentials-id' 
    }
    parameters {
        string(name: 'WEB_APP_URL', defaultValue: '', description: '')
    }

    stages {
        stage('Cleanup') {
            steps {
                sh 'echo "This is cleanup stage"'
                sh '''
                    if [ "$(docker ps -q)" ]; then
                        docker stop $(docker ps -q)
                        docker rm $(docker ps -aq)
                    else
                        echo "No running containers to stop or remove"
                    fi
                '''
                sh 'docker system prune -f'
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f k8s-manifest/deployment.yaml'
                    sh 'kubectl apply -f k8s-manifest/service.yaml'
                }
            }
    }
}
post {
    always {
        cleanWs()
    }
        success {
            slackSend(channel: '#succeeded-deploy', color: 'good', message: "Deploy #${env.BUILD_NUMBER} succeeded.")
        }
        failure {
            slackSend(channel: '#devops-alerts', color: 'danger', message: "Deploy #${env.BUILD_NUMBER} failed.")
        }

    }
}


