image-name=test
container-id:=$(shell docker ps -qf "ancestor=$(image-name)" --format="{{.ID}}")

build:
	docker build -t $(image-name) .

copy-venv:
	rm -rf ${PWD}/.venv/*
	docker run --rm -i \
		-v ${PWD}/.venv:/.cache \
		$(image-name) /bin/sh -c "cp -r /usr/app/.venv/* /.cache"

start-dev:
	docker run \
		--network=host \
		-v ${PWD}/.prefect:/root/.prefect \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-ti \
		$(image-name)

stop:
	docker exec -i $(container-id) invoke stop
	docker stop $(container-id)
