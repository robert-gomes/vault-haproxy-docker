.PHONY: all
all: generate-certs build upd
generate-certs: clear-certs
	cd config/certs; sh generate-certs.sh
clear-certs:
	rm -rf config/certs/*.crt
	rm -rf config/certs/*.key
	rm -rf config/certs/*.pem
	rm -rf config/certs/*.srl
	rm -rf config/certs/*.csr
build:
	docker-compose build
up:
	docker-compose up
upd:
	docker-compose up -d vault-1; sleep 20; docker-compose up -d vault-2; sleep 20; docker-compose up -d vault-3; docker-compose up -d
down:
	docker-compose down
	rm -rf tokens/*
stop:
	docker-compose stop
restart:
	docker-compose restart
ps:
	docker-compose ps