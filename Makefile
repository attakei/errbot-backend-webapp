STATIC_DIR = ./errbot_backend_webapp/resources/static


.PHONY: wheel
wheel: js
	python setup.py sdist bdist_wheel


.PHONY: js
js:
	yarn build -d $(STATIC_DIR)/ --no-source-maps views/app.js 
