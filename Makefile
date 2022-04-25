run:
	uvicorn main:app --reload
install:
	pip install -r requirements.txt
	python setup.py
test:
	echo "Make sure server is running"
	pytest .