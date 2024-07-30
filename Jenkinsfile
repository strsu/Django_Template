pipeline {
    agent any

    environment {
        WHOAMI="dev"

        SECRET_KEY="0&4cf&euo3dm#&**9@7ljwq37h9debg@b1yuulzsyat2ug2gjo"
        ELASTICSEARCH_DSL_IP="0.0.0.0"
        ELASTICSEARCH_DSL_PORT="5000"
        LOGSTASH_PORT="0.0.0.0"

        POSTGRES_DB="postgres"
        POSTGRES_USER="postgres"
        POSTGRES_PASSWORD="postgres"
        POSTGRES_HOST="anhae.asuscomm.com"
        POSTGRES_PORT="54320"

        BROKER_URL_="anhae.asuscomm.com"
        BROKER_PORT_="6379"

        REDIS_PASSWORD="RRartDMW3fhT4rb"

        HOST="anhae.asuscomm.com"
    }

    stages {
        stage('build') {
            steps {
                echo 'WHOAMI: $env.WHOAMI'
                echo 'building the application...'
                
                sh 'docker build -t backend_image ./backend'
                sh '''
                    docker run -d \
                        --name backend \
                        --env-file .env \
                        backend_image \
                        /opt/scripts/start_server.sh
                '''

                sh '''
                STATUS=0
                while [ $STATUS -ne 200 ]; do
                    STATUS=$(docker-compose -f docker-compose-cicd.yml -p prup exec backend curl -s -o /dev/null -w "%{http_code}" $URL)
                    echo -n -e "\\r[`date`] Waiting for the server to respond with status 200... Current State : $STATUS"
                    sleep 1
                done
                '''
            }
        }
        stage('test') {
            steps {
                echo 'testing the application...'
            }
        }
        stage('deploy') {
            steps {
                echo 'deploying the application...'
            }
        }
    }
}