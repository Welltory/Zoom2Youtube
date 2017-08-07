build:
		docker-compose build

up:
		docker-compose up
		
stop:
		docker-compose stop app

remove:
		docker-compose rm --all -f app
