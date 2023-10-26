from python 3.5.1



COPY ./requirements.txt /
RUN pip install -r /requirements.txt

COPY . /fileflow
WORKDIR /fileflow
CMD ["python", "/fileflow/server.py"]
