FROM nginx:mainline

RUN mkdir code
RUN mkdir code/staticfiles
RUN mkdir code/mediafiles

RUN mkdir home/conf.d
RUN mkdir home/nginx_logs

COPY conf.d/nginx.conf /home/conf.d

RUN rm etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

ADD start.sh /
RUN chmod +x /start.sh
RUN /start.sh

RUN apt-get -y update
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:certbot/certbot

RUN apt-get -y install python-certbot-nginx
