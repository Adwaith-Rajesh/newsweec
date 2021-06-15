imports:
	reorder-python-imports newsweec/bot/*.py
	reorder-python-imports newsweec/database/*.py
	reorder-python-imports newsweec/meta/*.py
	reorder-python-imports newsweec/utils/*.py
	reorder-python-imports newsweec.py
	reorder-python-imports newsweec/*.py
	reorder-python-imports test/*.py

run-test:
	pytest -rx -v

flake:
	flake8 newsweec/ --max-line-length=120
	flake8 test/ --max-line-length=120
