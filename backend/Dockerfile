FROM alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk update && \
    apk add python3 python3-dev mysql-client mysql-dev\
            musl-dev py3-pip openssl-dev g++\
            py3-numpy py3-scipy 
RUN apk add --no-cache -X http://mirrors.ustc.edu.cn/alpine/edge/testing py3-matplotlib

RUN mkdir -p /opt/backend
WORKDIR /opt/backend

RUN pip3 install flask PyMySQL coloredlogs uwsgi\
     -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache

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
