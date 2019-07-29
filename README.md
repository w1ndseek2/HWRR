# HWR 

## deployment

docker-compose up -d
curl 127.0.0.1/api/db_init

## development

python*3* backend/backend.py  
cp nginx_conf/default.conf /etc/nginx/conf.d  
** start nginx