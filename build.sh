docker build -t demo_1_api .
docker run -it --rm --network demo_1 -p 80:80 --name demo_1_api demo_1_api
