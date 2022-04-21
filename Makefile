SELF_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(SELF_DIR)common.mk

.DEFAULT_GOAL := build

ORIGINAL_DOCKER_COMPOSE=VERSION=$(VERSION) docker-compose
DOCKER_COMPOSE=$(ORIGINAL_DOCKER_COMPOSE)

.PHONY: build
build:
	@$(DOCKER_COMPOSE) build

.PHONY: run
run: DOCKER_COMPOSE=DD_API_KEY=$(DD_API_KEY) $(ORIGINAL_DOCKER_COMPOSE)
run:
	@$(DOCKER_COMPOSE) up --build --remove-orphans

.PHONY: stop
stop:
	@$(DOCKER_COMPOSE) down --remove-orphans --volumes


.PHONY: curl
curl: WEB_CONTAINER_ID=$(shell docker ps -q --filter "label=com.docker.compose.project=datadog-otlp" --filter "label=com.docker.compose.service=py-http")
curl: HOST_PORT=$(shell docker port $(WEB_CONTAINER_ID) 8080)
curl: KEY ?= foo
curl: ROUTE ?= /redis/$(KEY)
curl:
	@curl -s $(HOST_PORT)$(ROUTE)


.PHONY: ssh
ssh: COMPONENT?=datadog
ssh: DD_CONTAINER_ID=$(shell docker ps -q --filter "label=com.docker.compose.project=datadog-otlp" --filter "label=com.docker.compose.service=$(COMPONENT)")
ssh:
	@docker exec -it $(DD_CONTAINER_ID) /bin/bash
