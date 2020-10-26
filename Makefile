generate-certs:
	cd config/certs; sh generate-certs.sh
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
reload:
	docker-compose down up
ps:
	docker-compose ps
