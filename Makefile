VENV := .virtual_environment

all: install

$(VENV):
	python3 -m venv $(VENV)

install: install-deb install-pip

install-deb:
	@echo

install-pip: $(VENV)
	. $(VENV)/bin/activate; pip3 install --upgrade -r requirements.txt

playlist-agent:
	. $(VENV)/bin/activate; src/playlist_agent.py

menu-agent:
	. $(VENV)/bin/activate; src/menu_agent.py

preptime-agent:
	. $(VENV)/bin/activate; src/preptime_agent.py


