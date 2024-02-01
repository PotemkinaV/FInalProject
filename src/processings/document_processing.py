import textract
import re
import os
import random
import shutil
import tempfile
import chardet


def document2text(path):
    bytes_data = open(path, 'rb').read()
    encoding = chardet.detect(bytes_data)['encoding']
    text = textract.process(path, encoding=encoding)
    return text.decode('utf-8')


def clear_text(text):
    text = text.replace('HYPERLINK', '')
    text = re.sub("'", "", text)
    text = re.sub("(\\W)+", " ", text)
    text = text.replace("_", "")
    text = text.replace("-", " ")
    text = " ".join(text.split())
    return text


def preprocess_text(text):
    text = clear_text(text)
    return text


def create_temp_name():
    # generate random name from alphabet
    name = ""
    for i in range(20):
        name += random.choice("abcdefghijklmnopqrstuvwxyz")
    return name


def create_temp_folder(name):
    if not os.path.exists("../../temp"):
        os.mkdir("../../temp")
    # generate random folder name)
    folder_path = os.path.join("../../temp", name)
    os.mkdir(folder_path)
    return folder_path


def create_zip(files, predictions):
    name = create_temp_name()
    new_folder = create_temp_folder(name)
    zip_file = os.path.join("../../temp", name + ".zip")
    for file in files:
        # create folder for each class
        class_name = predictions[files.index(file)][2]
        class_folder = os.path.join(new_folder, class_name)
        if not os.path.exists(class_folder):
            os.mkdir(class_folder)
        # write file to folder
        with open(os.path.join(class_folder, file["original_name"]), "wb") as f:
            f.write(file["original_file"].getvalue())
    shutil.make_archive(zip_file[:-4], "zip", new_folder)
    return zip_file


def create_txt(text):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(text.encode('utf-8'))
        tmp_file.seek(0)
        txt_file = tmp_file.read()
    return txt_file


class MyFile:
    def __init__(self, name, bytes):
        self.name = name
        self.bytes = bytes

    def getvalue(self):
        return self.bytes


def create_csv(files, predictions):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write('filename, prediction\n'.encode('utf-8'))
        for file, prediction in zip(files, predictions):
            f.write(f'{file["original_name"]}, {prediction[2]}\n'.encode('utf-8'))
        csv_file = f.read()
    return csv_file
