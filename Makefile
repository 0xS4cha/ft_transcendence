all: up
ARGS ?:

.PHONY: all up down stop start boom nuke status logs build re

build:
	@docker compose -f compose.yaml build $(ARGS)

up:
	@docker compose -f compose.yaml up -d $(ARGS)

down:
	@docker compose -f compose.yaml down $(ARGS)

stop: 
	@docker compose -f compose.yaml stop $(ARGS)

start:
	@docker compose -f compose.yaml start $(ARGS)

re: down build up

boom:
	@docker compose -f compose.yaml down -v --rmi all $(ARGS)

nuke: boom
	@docker system prune -af

status: 
	@docker ps

logs:
	@docker compose -f compose.yaml logs -f $(ARGS)
