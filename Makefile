ARGS  ?=
UNAME := $(shell uname -s)

ifeq ($(UNAME),Darwin)
	HOST_IP = $(shell ipconfig getifaddr en0 || ipconfig getifaddr en1)
else
	HOST_IP = $(shell ip addr | grep "192.168" | cut -d ' ' -f6 | cut -d '/' -f1)
endif

DEV_COMPOSE  = docker compose -f compose.yaml -f compose.dev.yaml
PROD_COMPOSE = docker compose -f compose.yaml

all: up

build:
	@HOST_IP=$(HOST_IP) $(DEV_COMPOSE) build $(ARGS)

up:
	@HOST_IP=$(HOST_IP) $(DEV_COMPOSE) up -d $(ARGS)
	@OLLAMA_HOST=http://0.0.0.0:11434 ollama serve

down:
	@HOST_IP=$(HOST_IP) $(DEV_COMPOSE) down $(ARGS)

stop: 
	@HOST_IP=$(HOST_IP) $(DEV_COMPOSE) stop $(ARGS)

start:
	@HOST_IP=$(HOST_IP) $(DEV_COMPOSE) start $(ARGS)

re: down build up

# Production: image code only (no source mounts), fastapi run instead of fastapi dev.
prod-build:
	@HOST_IP=$(HOST_IP) $(PROD_COMPOSE) build $(ARGS)

prod:
	@HOST_IP=$(HOST_IP) $(PROD_COMPOSE) up -d $(ARGS)
	@OLLAMA_HOST=http://0.0.0.0:11434 ollama serve

prod-re: down prod-build prod

boom:
	@HOST_IP=$(HOST_IP) $(DEV_COMPOSE) down -v --rmi all $(ARGS)

nuke: boom
	@docker system prune -af

status: 
	@docker ps

logs:
	@HOST_IP=$(HOST_IP) $(DEV_COMPOSE) logs -f $(ARGS)


.PHONY: all up down stop start boom nuke status logs build re prod prod-build prod-re