FROM nginx:mainline

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN apt-get -y update
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:certbot/certbot

RUN apt-get -y install python-certbot-nginx

CMD ["nginx", "-g", "daemon off;"]
CMD certbot --nginx --test-cert --keep-until-expiring --email $EMAIL --agree-tos -n -d skgit60.com -d www.skagit60.com
#CMD ["nginx", "-g", "daemon off;"]