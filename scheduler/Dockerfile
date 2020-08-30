FROM prefecthq/prefect:latest
RUN apt-get update &&\
    apt-get install -y \
      build-essential \
      curl \
      docker.io
RUN pip install docker-compose
# for whatever reason installing it with apt conflicts with prefect

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV HOME /root
ENV PATH="$HOME/.poetry/bin:$PATH"
RUN poetry self update --preview
# https://github.com/python-poetry/poetry/issues/2711#issuecomment-663938960

ENV APP /usr/app

RUN mkdir $APP
WORKDIR $APP
COPY . .
RUN   poetry env use python &&\
      poetry install

ENV PATH="$APP/.venv/bin:$PATH"

CMD invoke dev
