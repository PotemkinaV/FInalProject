# My final project

## Overview

Task is to create web-service to sort documents by type of contract. \
Also we need to interpret the contract and extract some information from it.

## Methods

I have created web-service with streamlit. \

I used 2 methods to solve this task:

1. Classification using ruBert - accuracy 0.73 on test data (mean)
2. Summarization using GPT

You could find unrealized methods in some notebooks in the `notebooks` folder.

## Setup environment

### Linux/macOS

```bash
python3 -m venv venv/ 
venv/bin/activate
pip install poetry
poetry install
```

### Windows

```bash
python -m venv venv/
venv/Scripts/activate
pip install poetry
poetry install
```

Also install `model_weights` from
this [url](https://drive.google.com/uc?export=download&id=1a8r-Xj0b3xIQ-UlpzMACmsqgR9ecKHz5)
and extract it to `model_weights/` folder in the root folder.

## Run code

You should create .env in root folder and add your OPENAI_API_KEY to it.

```.env
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

## Web-service

![](.images/summarization.png)

```bash
streamlit run streamlit_app.py
```

And go by link in terminal.
