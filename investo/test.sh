docker stop investo_server
docker rm investo_server
docker build --no-cache -t gaurav28/investo_server:latest .
docker run -d --net=host -e CONTAINER_MODE=1 --name backend gaurav28/investo_server:latest
docker logs -f investo_server