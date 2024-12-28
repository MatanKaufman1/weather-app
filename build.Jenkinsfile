pipeline {
    environment {
        REGISTRY_URL = "dockerhub_url"
        registryCredential = 'dockerhub_id'
        APP_NAME = 'weather-app'
    }
    agent {
        node {
            label 'agent1'
        }
    }
    stages {
        stage('Cleanup') {
            steps {
                sh 'echo "This is cleanup stage"'
                cleanWs()
                sh 'docker system prune -f --volumes'
            }
        }
        stage('Install Requirements') {
            steps {
                sh '''
                    sudo apt-get update
                    sudo apt install python3.12-venv -y
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Pylint Test') {
            steps {
                sh '''
                    echo "Running pylint on *.py"
                    . venv/bin/activate
                    cd src/
                    pylint --fail-under=5 *.py
                    deactivate
                '''
            }
        }
        stage('Docker Build') {
            steps {
                sh "docker build -t ${APP_NAME}:${BUILD_NUMBER} ."
                sh "docker run --name ${APP_NAME}_${BUILD_NUMBER} -d -p 5000:5000 ${APP_NAME}:${BUILD_NUMBER}"
            }
        }
        stage('Smoke test') {
            steps {
                sh """
                    echo "Checking web-app connectivity"
                    sleep 2
                    . venv/bin/activate
                    cd src/tests/
                    python3 check-connectivity.py
                    docker stop ${APP_NAME}_${BUILD_NUMBER}
                    """
            }
        }
        stage('Tag and Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        sh """
                            docker tag ${APP_NAME}:$BUILD_NUMBER ${REGISTRY_URL}:$BUILD_NUMBER
                            docker push $REGISTRY_URL:$BUILD_NUMBER
                        """
                    }
                }
            }
        }
        stage('Trigger Deploy') {
            steps {
                build job: 'web-app-deploy', wait: false, parameters: [
                    string(name: 'WEB_APP_URL', value: "${REGISTRY_URL}:${BUILD_NUMBER}")
                ]
            }
        }
    }
}
post {
    always {
        sh """
            docker stop ${APP_NAME}_${BUILD_NUMBER} 
            docker rm ${APP_NAME}_${BUILD_NUMBER} 
        """
        cleanWs()
    }
        success {
            slackSend(channel: '#succeeded-build', color: 'good', message: "Build #${env.BUILD_NUMBER} succeeded.")
        }
        failure {
            slackSend(channel: '#devops-alerts', color: 'danger', message: "Build #${env.BUILD_NUMBER} failed.")
        }

    }
