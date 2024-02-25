FROM nginx:latest

RUN mkdir -p /misc/django_api_server/log

RUN rm -f /etc/nginx/conf.d/default.conf
COPY ./deploy/dev/nginx/default-nginx.conf /etc/nginx/nginx.conf
COPY ./deploy/dev/nginx/service-nginx.conf /etc/nginx/conf.d

COPY ./deploy/dev/nginx/entrypoint.sh /entrypoint.sh
COPY ./deploy/dev/nginx/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /wait-for-it.sh

ENTRYPOINT ["/entrypoint.sh"]