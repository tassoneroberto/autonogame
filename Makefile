.PHONY: run build-app build-package publish

run:
	autonogame

build-app:
	py -m pip install pyinstaller
	pyinstaller --clean --noupx -w -F -n autonogame --distpath ./app/ ./src/autonogame/gui.py

build-package:
	py -m pip install build twine
	py -m build
	py -m twine check dist/*

publish:
	twine upload dist/*
