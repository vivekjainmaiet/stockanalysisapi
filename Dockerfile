FROM python:3.8-buster

COPY api.py api.py
COPY data.py data.py
COPY param.py param.py
COPY utils.py utils.py
COPY requirements.txt requirements.txt
COPY client-cert.pem client-cert.pem
COPY client-key.pem client-key.pem
COPY server-ca.pem server-ca.pem

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD uvicorn api:app --host 0.0.0.0 --port $PORT
