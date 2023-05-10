IMAGE_NAME = my-password-bot

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm -it $(IMAGE_NAME)

clean:
	docker rmi $(IMAGE_NAME)