# Makefile

# Google Drive file ID
FILE_ID = 1a8r-Xj0b3xIQ-UlpzMACmsqgR9ecKHz5
# Destination file name
DEST = model_weights.zip

# Default target
all: setup

# Target to download the file
download:
	@echo "Downloading file..."
	@curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=$(FILE_ID)" > /dev/null
	@curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/confirm/ {print $NF}' ./cookie`&id=$(FILE_ID)" -o $(DEST)
	@echo "Download complete."

# Target to extract the ZIP file and delete it after extraction
extract: download
	@echo "Extracting file..."
	@unzip -q $(DEST)
	@rm -f $(DEST)
	@rm cookie
	@echo "Extraction complete."

# Setup target to set up the environment and download + extract files
setup:
	python3 -m venv venv/
	. venv/bin/activate && curl -sSL https://install.python-poetry.org | python3 -
	$(MAKE) poetry_install
	$(MAKE) extract
	@echo "Setup complete."

# Target to install dependencies using poetry
poetry_install:
	. venv/bin/activate && poetry install

# Clean target
clean:
	@rm -f cookie

.PHONY: all download extract setup poetry_install clean
