# cloudflare-ddns-update
docker compose
```
version: '3'
services:
  cloudflare-ddns-update:
    image: yingkhun/cloudflare-ddns-update
    container_name: cloudflare-ddns-update
    restart: always
    environment:
      - email=${email}
      - domain=${domain}
      - api_key=${api_key}
      - interval_time=${interval_time}
      - time_zone=Asia/Bangkok
```
cil
```
sudo docker run -d --restart always \
--name cloudflare-ddns-update \
-e email=<email> \
-e domain=<domain.com> \
-e api_key=<api_key> \
-e interval_time=<interval_time> \
-e time_zone=<time_zone> \
yingkhun/cloudflare-ddns-update
```
 `Global API Key : https://dash.cloudflare.com/profile/api-tokens` <br>
`interval_time minimum : 20`
