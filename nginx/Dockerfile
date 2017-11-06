FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

ADD ./certs /etc/nginx/certs
RUN chmod -R 600 /etc/nginx/certs/*