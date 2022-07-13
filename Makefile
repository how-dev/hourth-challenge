create_db_volume:
	@echo "--> Creating a local database volume"
	docker volume create --name=db_local

run:
	@echo "--> \033[0;32mUping\033[0m"
	docker-compose up

down:
	docker-compose down

build:
	@echo "--> \033[0;32mBuilding\033[0m"
	docker-compose build --no-cache

cache-build:
	@echo "--> \033[0;32mBuilding\033[0m"
	docker-compose build

migrations:
	@echo "--> \033[0;32mMaking migrations...\033[0m"
	docker-compose run web bash -c "python manage.py makemigrations"

migrate:
	@echo "--> \033[0;32mMigrating...\033[0m"
	docker-compose run web bash -c "python manage.py migrate"

bash:
	@echo "--> \033[0;32mLogging into the Docker machine via bash\033[0m"
	docker-compose run web bash

sh:
	@echo "--> \033[0;32mLogging into the Docker machine via sh\033[0m"
	docker-compose run web sh

test:
	@echo "--> \033[0;32mUping the services to run tests\033[0m"
	docker-compose run web bash -c "pytest $(path) -s -v --disable-warnings --cov-report term-missing"

startapp:
	@echo "--> \033[0;32mCreating app\033[0m"
	docker-compose run web bash -c " \
			python manage.py startapp $(name) && \
			mv $(name) apps && cd ./apps/$(name) && \
			awk 'NR>0 && \
			NR < 6' apps.py > apps2.py && \
			echo \"    name = 'apps.$(name)'\" >> apps2.py && \
			rm apps.py && mv apps2.py apps.py \
	"

setup:
	@echo "--> Creating a local database volume"
	docker volume create --name=db_local

	@echo "--> \033[0;32mBuilding\033[0m"
	docker-compose build --no-cache

	@echo "--> \033[0;32mMaking migrations...\033[0m"
	docker-compose run web bash -c "python manage.py makemigrations"

	@echo "--> \033[0;32mMigrating...\033[0m"
	docker-compose run web bash -c "python manage.py migrate"

	@echo "--> \033[0;32mSetuping application\033[0m"
	@echo "--> \033[0;32mCreating Hourth Super User\033[0m"
	docker-compose run web bash -c "python manage.py create_superuser"

	@echo "--> \033[0;32mCreating 100 random Products with random Categories\033[0m"
	docker-compose run web bash -c "python manage.py create_products"

	@echo "--> \033[0;32mCreating 100 random Users\033[0m"
	docker-compose run web bash -c "python manage.py create_randomusers"

	@echo "--> \033[0;32mUping the services to run tests\033[0m"
	docker-compose run web bash -c "pytest -s -v --disable-warnings --cov-report term-missing"
