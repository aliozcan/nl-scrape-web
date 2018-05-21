FROM python:3.6.5-alpine3.7

ADD provision.sh entrypoint.sh

RUN chmod +x entrypoint.sh
RUN /entrypoint.sh

