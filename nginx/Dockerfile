FROM nginx:mainline

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN apt-get -y update
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:certbot/certbot

RUN apt-get -y install python-certbot-nginx

ADD start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]