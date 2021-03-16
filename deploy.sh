service docker start
docker stack rm investo
docker swarm leave --force
sleep 10
docker swarm init
docker stack deploy -c docker-compose.yml investo