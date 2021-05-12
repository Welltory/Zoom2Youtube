build:
		docker-compose build

up:
		docker-compose up
		
stop:
		docker-compose stop app

remove:
		docker-compose rm --all -f app

bash:
		docker-compose run app bash

check-env:
		docker-compose run app python3.6 src/check_env.py

get-google-refresh-token:
		docker-compose run app python3.6 src/get_google_refresh_token.py

prepare-pipenv:
		pip install pipenv
		pipenv install --dev

sync-setup-py: prepare-pipenv
		pipenv run pipenv-setup sync
