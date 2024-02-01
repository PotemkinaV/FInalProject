import base64

import streamlit as st

from src import neuro
from src.processings.document_processing import create_csv, create_zip, document2text, \
    preprocess_text
import tempfile


def displayPDF(file, is_bytes=False):
    if not is_bytes:
        file = base64.b64encode(file.getvalue()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{file}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


@st.cache_resource()
def load_model():
    model = neuro.init_model()
    return model


@st.cache_resource()
def load_tokenizer():
    tokenizer = neuro.init_tokenizer()
    return tokenizer


def make_prediction(model, tokenizer, file):
    original_text = document2text(file)
    text = preprocess_text(original_text)
    result = neuro.predict(model, tokenizer, text)
    return original_text, text, result


def visualize_file(file, original_text):
    st.subheader("Документ:")
    if file.name.endswith(".pdf"):
        displayPDF(file)
    else:
        # original text to unicode
        st.write("", original_text, disabled=True, height=1000)


def activate():
    st.set_page_config(
        page_title="Помощник с документами",
        layout="wide",
    )

    # load model and tokenizer
    model = load_model()
    tokenizer = load_tokenizer()

    st.title("Маршрутизация документов")
    st.write(
        "Здесь вы можете загрузить документ и получить предсказание, куда его направить")
    files = st.file_uploader("Загрузите документ", type=["pdf", "docx", "doc", "rtf"],
                             accept_multiple_files=True)
    temp_files = []
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as tmp_file:
            tmp_file.write(file.read())
            new_file = {
                "original_name": file.name,
                "original_file": file,
                "temp_name": tmp_file.name,
                "temp_file": tmp_file
            }
            temp_files.append(new_file)

    if len(temp_files) > 0:
        # make prediction
        predictions = [make_prediction(model, tokenizer, file["temp_name"]) for file in temp_files]

        # create table with file names and their predictions
        st.subheader("Результаты:")
        st.table(
            [{"Документ": file["original_name"], "Предсказание": prediction[2]} for file, prediction
             in zip(temp_files, predictions)])

        # create zip file with all files
        zip_file_name = create_zip(temp_files, predictions)
        with open(zip_file_name, "rb") as f:
            zip_file = f.read()

        # click button and download .zip file
        st.download_button(
            label="Загрузить zip с отсортированными документами",
            data=zip_file,
            file_name='data.zip'
        )

        # click button and download .csv file
        csv_file = create_csv(temp_files, predictions)
        st.download_button(
            label="Загрузить csv с предсказаниями",
            data=csv_file,
            file_name='predictions.csv'
        )

        # choose file to visualize
        viz_original_name = st.selectbox("Выберите файл для просмотра",
                                         [file["original_name"] for file in temp_files])
        for file in temp_files:
            if file["original_name"] == viz_original_name:
                viz_file = file

        summarized_text = neuro.summarize_file(viz_file["temp_name"])
        st.subheader("Кратко о документе:")
        st.write("", summarized_text, disabled=True, height=1000)


if __name__ == '__main__':
    activate()
    print('[#] Сайт активен')
