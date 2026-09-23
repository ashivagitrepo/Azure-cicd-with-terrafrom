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
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=Task-Manager \
                          -Dsonar.projectName=Task-Manager \
                          -Dsonar.sources=.
                    '''
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
    }
}
