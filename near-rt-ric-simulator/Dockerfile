FROM python:3

WORKDIR /usr/src/app

RUN pip install connexion[swagger-ui]

COPY src src

COPY api api

CMD src/start.sh ${A1_VERSION}
