image-name=test

build:
	docker build -t $(image-name) ${PWD}

copy-venv:
	docker run --rm -i \
		-v ${PWD}/.venv:/.cache \
		$(image-name) /bin/sh -c "cp -r /usr/app/.venv/* /.cache"

start-dev:
	docker run \
		--network=host \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-ti \
		$(image-name)
		