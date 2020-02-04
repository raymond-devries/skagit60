FROM nginx:mainline

RUN mkdir code
RUN mkdir code/staticfiles
RUN mkdir code/mediafiles

RUN mkdir home/conf.d

COPY conf.d/nginx.conf /home/conf.d

COPY NGINX_API_KEY.txt /

COPY conf.d/stub_status.conf /etc/nginx/conf.d/

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

ADD start.sh /
RUN chmod +x /start.sh
RUN /start.sh

RUN apt-get -y update
RUN apt-get -y install curl
RUN apt-get -y install apt-transport-https
RUN apt-get -y install gnupg
RUN apt install -y python2.7 python-pip

RUN curl -L -O https://github.com/nginxinc/nginx-amplify-agent/raw/master/packages/install.sh
RUN NGINX_API_KEY=`cat NGINX_API_KEY.txt` && API_KEY="$NGINX_API_KEY" sh ./install.sh -y

RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:certbot/certbot

RUN apt-get -y install python-certbot-nginx
