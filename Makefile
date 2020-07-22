init:
	pipenv install --dev --skip-lock
proxy:
	pipenv run mitmdump -s proxy/catch.py
y = example.yml
yml:
	pipenv run python3 mock/app.py mock/$(y)