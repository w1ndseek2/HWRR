# HWR 

## deployment

cd frontend && npm run build  
docker-compose up -d

## development

python*3* backend/backend.py  
cd frontend && npm run dev  
cp nginx_conf/default.conf /etc/nginx/conf.d  
** start nginx