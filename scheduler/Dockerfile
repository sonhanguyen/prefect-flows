FROM python:3.7.9-slim
RUN apt-get update &&\
    apt-get install -y \
      build-essential \
      graphviz \
      docker.io
RUN pip install docker-compose
# for whatever reason installing it with apt conflicts with prefect

RUN pip install poetry

ENV HOME /root
ENV PATH="$HOME/.poetry/bin:$PATH"

ENV APP /usr/app
RUN mkdir $APP
WORKDIR $APP
COPY . .
RUN   poetry env use python &&\
      poetry install

ENV PATH="$APP/.venv/bin:$PATH"

RUN mkdir -p $HOME/.prefect/flows
EXPOSE 4001 8080

CMD invoke dev
