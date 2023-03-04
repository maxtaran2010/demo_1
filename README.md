# demo_1

## create network

```bash
docker network create -d bridge demo_1
```

## creating docker containers

### nginx

```
docker run -d --name nginx_demo_1 --network demo_1 -it -p 8080:80 nginx
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
docker run --name demo_1_mysql --network demo_1 -e MYSQL_ROOT_PASSWORD=*password* -d mysql
```

### phpmyadmin

for simple DB manegment you can run phpmyadmin:

```
docker run --name phpmyadmin -d -e PMA_HOST=demo_1_mysql --network demo_1 -p 8080:80 phpmyadmin
```

### creating DB
* create db named `main`
* create 2 tables: <br>
user (id (auto increment), date_insert (CURRENT_TIMESTAMP), date_update (CURRENT_TIMESTAMP), phone, password_hash), <br> user_token (id (auto increment), date_insert (CURRENT_TIMESTAMP), date_update (CURRENT_TIMESTAMP), user_id, token, expires)


### main container
you need to create in root folder file named `secrets.txt` and put password, that you entered in last step
```
chmod +x build.sh
./build.sh
```

## done

now, nginx running on `localhost:8080`. If not, try restarting nginx
