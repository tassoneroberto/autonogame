.PHONY: exe run

app:
	pyinstaller --clean --noupx -w -F -n autonogame ./src/autonogame/gui.py

run:
	autonogame
