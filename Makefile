.PHONY: exe run

app:
	pyinstaller --clean --noupx -w -F -n aut0game ./src/aut0game/gui.py

run:
	aut0game
