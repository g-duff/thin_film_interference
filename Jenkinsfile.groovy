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
				sh "make lint"
			}
		}
		stage('Test') { 
			steps {
				sh "make test"
			}
		}
	}

	post {

		always {
			sh "make clean"
		}

		success {
			withCredentials([string(credentialsId: 'GitHubStatusToken', variable: 'TOKEN')]) {
				sh '''curl -L \
					-X POST \
					"https://api.github.com/repos/g-duff/thin_film_interference/statuses/$GIT_COMMIT" \
					-H "Accept: application/vnd.github+json" \
					-H "X-GitHub-Api-Version: 2022-11-28" \
					-H "Authorization: Bearer $TOKEN"\
					-d '{\
						"state": "success", \
						"context": "continuous-integration/jenkins", \
						"target_url": "https://github.com/g-duff/Jenkins" \
					}'
					'''
			}
		}

		failure {
			withCredentials([string(credentialsId: 'GitHubStatusToken', variable: 'TOKEN')]) {
				sh '''curl -L \
					-X POST \
					"https://api.github.com/repos/g-duff/thin_film_interference/statuses/$GIT_COMMIT" \
					-H "Accept: application/vnd.github+json" \
					-H "X-GitHub-Api-Version: 2022-11-28" \
					-H "Authorization: Bearer $TOKEN"\
					-d '{\
						"state": "failure", \
						"context": "continuous-integration/jenkins", \
						"target_url": "https://github.com/g-duff/Jenkins" \
					}'
				'''
			}
		}

	}
}
