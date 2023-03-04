# demo_1

## creating docker containers

### nginx

```
docker run -d --name nginx_demo_1 --network demo_1 -it -v c:/Projects/School/demo_1/nginx:/etc/nginx -p 8080:80 nginx
```

configure 
```
events {}

http {

    server {

        listen 80;

        location / {

            proxy_pass http://demo_1_api;

        }

    }

}

```

### mysql
```

```

```
