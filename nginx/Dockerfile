FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

ADD certs/main.crt /etc/ssl/private/main.crt
ADD certs/main.key /etc/ssl/private/main.key
RUN chmod -R 600 /etc/ssl/private/main.*
