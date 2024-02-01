import streamlit as st
from src.processings.document_processing import create_txt
from src import neuro


def main():
    # Display title and description
    st.title("Резюмирование текста")
    st.write("Здесь вы можете загрузить документ и получить сокращённый текст")

    # Allow user to upload a document
    file = st.file_uploader("Загрузите документ", type=["pdf", "docx", "doc", "rtf"],
                            accept_multiple_files=False)

    # If a file is uploaded
    if file is not None:
        # Summarize the uploaded file
        text = neuro.summarize_file(file)

        # Display processing message
        st.write('Обработка запроса...')

        # Display the summarized text
        st.subheader("Сокращенный текст:")
        st.write(text)

        # Create a .txt file with the new text
        file = create_txt(text)

        # Allow user to download the .txt file
        st.download_button(
            label="Загрузить txt с сокращённым текстом",
            data=file,
            file_name='short_doc.txt'
        )


if __name__ == '__main__':
    main()
