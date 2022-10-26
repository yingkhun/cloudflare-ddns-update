# cloudflare-ddns-update
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
`interval_time minimum : 20`
