#!/bin/sh
sudo uwsgi --http :80  --chdir /home/ubuntu/Weixin_fucaijin_django/ -w Weixin_fucaijin_django.wsgi