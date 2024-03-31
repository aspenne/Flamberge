FROM curlimages/curl

USER root

COPY FlambergeElastic/mapping/init.sh /tmp/init.sh
COPY FlambergeElastic/mapping/files /tmp/files

RUN chmod u+x /tmp/init.sh

CMD ["/tmp/init.sh"]
