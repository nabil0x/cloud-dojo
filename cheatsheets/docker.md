# Docker Cheat Sheet (Cloud Dojo)

Containers live here. Images, volumes, networks, Compose — one page.

## Containers
```bash
docker run hello-world              # smoke test
docker run -d --name web -p 8080:80 nginx     # detached + named + port HOST:CONTAINER
docker ps                           # running only
docker ps -a                        # including stopped
docker logs web                     # stdout/stderr
docker logs -f web                  # follow
docker stop web                     # graceful SIGTERM, then SIGKILL
docker rm web                       # delete (must be stopped; -f forces)
docker exec -it web sh              # shell inside a running container
docker inspect web                  # full JSON: IP, mounts, env
```

## Images
```bash
docker images                       # local images
docker build -t myapp:v1 .          # build (`.` = build context)
docker image history myapp:v1       # layers + sizes + commands
docker tag myapp:v1 user/myapp:v1
docker push user/myapp:v1
docker rmi myapp:v1                 # delete image
docker run --rm myapp:v1            # auto-remove container on exit
```

## Dockerfile (order = cache)
```dockerfile
FROM python:3.13-slim   # pinned base, never :latest for keepers
WORKDIR /app
COPY requirements.txt . # slow-changing first → cached
RUN pip install --no-cache-dir -r requirements.txt
COPY . .                # fast-changing last
EXPOSE 8080             # metadata only; -p publishes
CMD ["python", "app.py"]
```
Rebuild twice (unchanged, then one file edited) and watch `CACHED` steps.

## Volumes (persistence)
```bash
docker volume create pgdata
docker volume ls
docker run -d --name db -v pgdata:/var/lib/postgresql/data postgres:16
docker volume inspect pgdata        # where data lives on the host
docker volume rm pgdata             # delete (data gone)
```

## Networks (DNS by name)
```bash
docker network create dojo-net
docker network ls
docker run -d --name cache --network dojo-net redis
docker run --rm --network dojo-net alpine ping -c1 cache   # name resolves
```
Rule: host → `localhost:PORT`, container → `<name>:PORT`.

## Compose (one-command stacks)
```bash
docker compose up -d --build        # build + start everything
docker compose ps
docker compose logs -f app          # one service
docker compose down                 # stop + remove containers
docker compose down -v              # also delete volumes (the nuke)
```

## Cleanup
```bash
docker ps -aq | xargs docker rm -f  # remove all containers (careful)
docker image prune                  # dangling images
docker system df                    # what eats disk
```

*From the [Cloud Dojo](../README.md) Phase 0–2 path. Full lessons in `phase-00/`, `phase-01/`, `phase-02/`.*
