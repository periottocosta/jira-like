
coverage-test:
	coverage run manage.py test ./tests && coverage report --show-missing

run-server:
	python manage.py makemigrations && \
	python manage.py migrate && \
	python manage.py makemigrations clients && \
	python manage.py migrate clients && \
	python manage.py makemigrations projects && \
	python manage.py migrate projects && \
	python manage.py makemigrations tasks && \
	python manage.py migrate tasks && \
	python manage.py runserver
