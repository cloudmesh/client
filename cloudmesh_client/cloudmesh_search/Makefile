all:
	python setup.py install
	sphinx-apidoc -o docs/source cloudmesh_search
	cd docs; make -f Makefile html

view:
	open docs/build/html/index.html

clean:
	rm -rf docs/build
	rm -rf build
	rm -rf cloudmesh_search.egg-info
	rm -rf dist

requirements:
	pip install -r requirements.txt
	pip install -r requirements-other.txt
