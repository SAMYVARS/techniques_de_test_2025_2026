# Lance tous les tests (unitaires + performance)
test:
	python3 -m pytest tests/

# tests unitaires (exclu les tests de performance)
unit_test:
	python3 -m pytest tests/ -m "not performance"

# tests de performance
perf_test:
	python3 -m pytest tests/ -m "performance"

# rapport de couverture de code
coverage:
	python3 -m coverage run -m pytest tests/
	python3 -m coverage report
	python3 -m coverage html

# qualité du code avec ruff
lint:
	python3 -m ruff check src/ tests/

# documentation HTML
doc:
	python3 -m pdoc --html --output-dir docs src/triangulator

