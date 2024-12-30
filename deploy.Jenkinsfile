pipeline {
    agent any
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

        stage('Deploy') {
            steps {
                sh '''
                    echo "Deploying Docker image: ${WEB_APP_URL}"
                    ssh -o StrictHostKeyChecking=no -i /home/ubuntu/pem-file/jenkinsKey.pem ubuntu@
                    sudo docker pull ${WEB_APP_URL}
                    sudo docker run -d -p 5000:5000 ${WEB_APP_URL}

                '''
            }
        }
    }
}
