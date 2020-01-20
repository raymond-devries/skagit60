#!/bin/bash

service nginx start
service nginx status
certbot --nginx --test-cert --keep-until-expiring --email $EMAIL --agree-tos -n -d skagit60.com
service nginx stop
nginx -g 'daemon off;'