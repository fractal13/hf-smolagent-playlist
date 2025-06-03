VENV := .virtual_environment

all: install

$(VENV):
	python3 -m venv $(VENV)

install: install-deb install-pip

install-deb:
	@echo

install-pip: $(VENV)
	. $(VENV)/bin/activate; pip3 install --upgrade -r requirements.txt

playlist-code-agent:
	. $(VENV)/bin/activate; src/playlist_code_agent.py

menu-code-agent:
	. $(VENV)/bin/activate; src/menu_code_agent.py

preptime-code-agent:
	. $(VENV)/bin/activate; src/preptime_code_agent.py

playlist-tool-agent:
	. $(VENV)/bin/activate; src/playlist_tool_agent.py

super-vision-agent:
	. $(VENV)/bin/activate; src/super_vision_agent.py

image-tools-demo:
	. $(VENV)/bin/activate; src/image_tools.py

r:
	. $(VENV)/bin/activate; alfred_gala/retriever.py

t:
	. $(VENV)/bin/activate; alfred_gala/tools.py

