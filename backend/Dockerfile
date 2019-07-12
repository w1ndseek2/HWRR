FROM python:3.7.3-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk update && \
    apk add python-dev linux-headers libffi-dev gcc make\
            musl-dev py-pip mysql-client openssl-dev g++\
            py-numpy

RUN mkdir -p /opt/backend
WORKDIR /opt/backend
COPY requirements.txt .

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /opt/backend
EXPOSE 8081

CMD [\
    "uwsgi",\
    "--http", "0.0.0.0:8081",\
    "--plugin", "python",\
    "--wsgi-file", "backend.py",\
    "--callable","app",\
    "--processes", "4",\
    "--threads", "2"\
    ]
