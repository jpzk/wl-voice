PREFIX ?= /usr/local

install:
	@if [ ! -d ".venv" ]; then \
		uv venv; \
	fi; \
	source .venv/bin/activate && \
	uv pip install -r requirements.txt && \
	uv pip install pyinstaller && \
	pyinstaller --onefile wl-voiced.py && \
	pyinstaller --onefile wl-voice.py && \
	cp dist/wl-voiced $(PREFIX)/bin/wl-voiced && \
	cp dist/wl-voice $(PREFIX)/bin/wl-voice

uninstall:
	rm -f $(PREFIX)/bin/wl-voiced $(PREFIX)/bin/wl-voice

.PHONY: install uninstall