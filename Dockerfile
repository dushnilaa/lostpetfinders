FROM python:3.8 AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY parser .
RUN apt-get update
RUN apt-get upgrade

RUN apt-get install -y python3-mysqldb
ENV PATH=/root/.local:$PATH

CMD [ "python", "-u", "./run.py" ]