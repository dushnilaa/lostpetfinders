FROM python:3.10 AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY config.yaml .
COPY parser_files .
RUN apt-get update
RUN apt-get upgrade

RUN apt-get install -y python3-mysqldb
ENV PATH=/root/.local:$PATH

CMD [ "python", "-u", "./run.py" ]