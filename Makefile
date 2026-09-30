ARGS		?=
HOST_IP		= ${shell ip addr | grep "192.168" | cut -d ' ' -f6 | cut -d '/' -f1}

all: up

build:
	@ollama pull "qwen3:0.6b"
	@HOST_IP=$(HOST_IP) docker compose -f compose.yaml build $(ARGS)

up:
	@HOST_IP=$(HOST_IP) docker compose -f compose.yaml up -d $(ARGS)
	@ollama serve

down:
	@HOST_IP=$(HOST_IP) docker compose -f compose.yaml down $(ARGS)

stop: 
	@HOST_IP=$(HOST_IP) docker compose -f compose.yaml stop $(ARGS)

start:
	@HOST_IP=$(HOST_IP) docker compose -f compose.yaml start $(ARGS)

re: down build up

boom:
	@HOST_IP=$(HOST_IP) docker compose -f compose.yaml down -v --rmi all $(ARGS)

nuke: boom
	@docker system prune -af

status: 
	@docker ps

logs:
	@HOST_IP=$(HOST_IP) docker compose -f compose.yaml logs -f $(ARGS)


.PHONY: all up down stop start boom nuke status logs build re