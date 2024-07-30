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
                echo 'WHOAMI: ${env.WHOAMI}'
                echo 'building the application...'

                sh 'docker build -t backend_image ./backend'
                sh '''
                    docker run -d \
                        -e WHOAMI=$env.WHOAMI \
                        -e SECRET_KEY=$env.SECRET_KEY \
                        -e ELASTICSEARCH_DSL_IP=$env.ELASTICSEARCH_DSL_IP \
                        -e ELASTICSEARCH_DSL_PORT=$env.ELASTICSEARCH_DSL_PORT \
                        -e LOGSTASH_PORT=$env.LOGSTASH_PORT \
                        -e POSTGRES_DB=$env.POSTGRES_DB \
                        -e POSTGRES_USER=$env.POSTGRES_USER \
                        -e POSTGRES_PASSWORD=$env.POSTGRES_PASSWORD \
                        -e POSTGRES_HOST=$env.POSTGRES_HOST \
                        -e POSTGRES_PORT=$env.POSTGRES_PORT \
                        -e BROKER_URL_=$env.BROKER_URL_ \
                        -e BROKER_PORT_=$env.BROKER_PORT_ \
                        -e REDIS_PASSWORD=$env.REDIS_PASSWORD \
                        -e HOST=$env.HOST \
                        --name backend \
                        backend_image \
                        /opt/scripts/start_server.sh
                '''

                sh '''
                URL="http://localhost:8000/api/swagger/"
                STATUS=0
                while [ $STATUS -ne 200 ]; do
                    STATUS=$(docker exec backend curl -s -o /dev/null -w "%{http_code}" $URL)
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