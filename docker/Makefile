create:
	docker-machine create --driver virtualbox cm-docker

run:
	docker-machine env cm-docker


image:
	docker build -t docker-cm .

run:
	docker run docker-cm
