### Cadre-data-api
- Github [link](https://github.com/iuni-cadre/cadre-data)
- Both production and dev versions deployed from master
- Service restart
    - Managed by supervisor process
    - Make sure data api ec2 instance can create connections to database machines
    (mag postgres + neo4j, wos postgres + neo4j)
    - Logs : `/home/ubuntu/cadre-data/cadre_data.log`
    - Config : `/home/ubuntu/cadre-data/conf/cadre.config`
    - For the dev version, we use two aws sqs queues for now. One for janus graph
    and one for WOS
    - Important configs :
        - [WOS_DATABASE_INFO]
        database-host=10.0.1.134
        database-port=5432
        database-name=wos
        database-username=
        database-password=
        - [CADRE_META_DATABASE_INFO]
        database-host=10.0.1.192
        database-port=5432
        database-name=
        database-username=
        database-password=
        - [MAG_DATABASE_INFO]
        database-host=10.0.1.197
        database-port=5432
        database-name=mag
        database-username=
        database-password=
        - [MAG_GRAPH_DB_INFO]
        database-url=bolt://10.0.1.176:7687
        database-username=
        database-password=
        - [CADRE]
        This is token endpoint from cadre-login repository
        token-api=https://cadre.iu.edu/api/auth/authenticate-token
        - [AWS]
        aws_access_key_id=
        aws_secret_access_key=
        region_name=us-east-1
        queue_url=https://sqs.us-east-1.amazonaws.com/799597216943/cadre-job-listne
        r-vpceast1.fifo
