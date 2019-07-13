FROM alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk update && \
    apk add python3 python3-dev mysql-client mysql-dev\
            musl-dev py3-pip openssl-dev g++ linux-headers\
            py3-numpy py3-scipy 
RUN apk add --no-cache -X http://mirrors.ustc.edu.cn/alpine/edge/testing py3-matplotlib

RUN mkdir -p /opt/backend
WORKDIR /opt/backend

RUN pip3 install flask PyMySQL coloredlogs uwsgi dtw interval\
     -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache

COPY . /opt/backend
RUN chmod +x /opt/backend/docker-entrypoint.sh
EXPOSE 8081

CMD ["/opt/backend/docker-entrypoint.sh"]
