FROM python:3.8-buster

COPY api.py api.py
COPY data.py data.py
COPY param.py param.py
COPY model.joblib model.joblib
COPY requirements.txt requirements.txt

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD uvicorn api:app --host 0.0.0.0 --port $PORT
