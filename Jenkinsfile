pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Checking Python..."
                    python3 --version

                    echo "Creating Python virtual environment..."
                    python3 -m venv venv

                    echo "Checking virtual environment..."
                    ./venv/bin/python --version

                    echo "Upgrading pip..."
                    ./venv/bin/pip install --upgrade pip

                    echo "Installing project dependencies..."
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'

                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=Task-Manager \
                              -Dsonar.projectName=Task-Manager \
                              -Dsonar.sources=.
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t task-manager:latest .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

                        docker tag task-manager:latest dockerymal/taskmanager:latest

                        docker push dockerymal/taskmanager:latest

                        docker logout
                    '''
                }
            }
        }
    }
}
