FROM nginx:mainline

RUN mkdir code
RUN mkdir code/staticfiles
RUN mkdir code/mediafiles
COPY nginx.conf /home/
COPY NGINX_API_KEY.txt /
COPY stub_status.conf /etc/nginx/conf.d/
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
