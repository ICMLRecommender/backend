Backend for ICML app.

## Renew SSL certificate
Link to [certbot](https://certbot.eff.org/).
```
sudo certbot renew --dry-run
sudo certbot renew
```
## Run uwsgi
```
cd /home/icmlapp/backend/server/icml # Optional
uwsgi --ini /home/icmlapp/backend/server/icml/icml_uwsgi.ini
```

## Start nginx
```
sudo /etc/init.d/nginx restart
```
