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

}
