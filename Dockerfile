FROM python:3.12

WORKDIR app/

COPY aplicacao/ ./aplicacao/
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

ENV FLASK_APP aplicacao.app:APP

RUN flask db init && flask db migrate -m "First" && flask db upgrade

CMD ["flask", "run", "--host", "0.0.0.0"]