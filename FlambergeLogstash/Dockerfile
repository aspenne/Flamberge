FROM docker.elastic.co/logstash/logstash:7.17.17

USER root

RUN logstash-plugin install logstash-integration-jdbc
# copy the postgres jdbc driver to the external library folder of logstash
COPY FlambergeLogstash/postgresql-42.7.3.jar /usr/share/logstash/
# RUN chmod 744 usr/share/logstash/postgresql-42.7.3.jar

# copy all our pipelines to the config file of logstash
COPY FlambergeLogstash/datasync.conf /usr/share/logstash/pipeline/datasync.conf

CMD ["logstash", "-f", "/usr/share/logstash/pipeline/datasync.conf"]
