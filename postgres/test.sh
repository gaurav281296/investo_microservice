docker run -d --name postgres --net=host -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -v ~/var/lib/postgresql/data:/var/lib/postgresql/data/  postgres:alpine