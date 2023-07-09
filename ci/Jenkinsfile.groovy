@Library('pipeline-lib') _

pipeline {
    
    agent { label 'python' }
    
    stages {
        stage('Install dependencies') {
            steps {
                sh "make dev_dependencies"
            }
        }
        stage('Lint') {
            steps {
                script {
                    try {
                        sh "make lint"
                    } catch (error) {
                        unstable(message: "${STAGE_NAME} is unstable")
                    }
                }
            }
        }
        stage('Test') { 
            steps {
                script {
                    try {
                        sh "make test"
                    } catch (error) {
                        unstable(message: "${STAGE_NAME} is unstable")
                    }
                }
            }
        }
    }

    post {

        success {
            script {
                notifyGitHubBuildStatus("thin_film_interference", "success")
            }
        }

        unstable {
            script {
                notifyGitHubBuildStatus("thin_film_interference", "failure")
            }
        }

        failure {
            script {
                notifyGitHubBuildStatus("thin_film_interference", "error")
            }
        }

        cleanup {
            sh "make clean"
        }

    }
}
