# Lesson 103 — Docker Networks

A practical reference for inspecting Docker networks, connecting containers, testing container-name resolution, publishing ports, and troubleshooting connectivity.

## List and inspect networks

```bash
docker network ls
docker network inspect bridge
docker network inspect <NETWORK_NAME>
```

Replace `<NETWORK_NAME>` with an actual network name. Network inspection shows attached containers and network configuration.

## Create a user-defined bridge network

```bash
docker network create sfs-app
docker network inspect sfs-app
```

User-defined bridge networks are useful for application services on one Docker host. Containers attached to the same network can communicate using container names through Docker's embedded DNS.

## Connect containers using their names

Start an NGINX container on the network:

```bash
docker run -d --name sfs-api --network sfs-app nginx:alpine
```

Use a temporary container to request it by name:

```bash
docker run --rm --network sfs-app alpine wget -qO- http://sfs-api
```

The request should return the NGINX welcome page. This tests name resolution and HTTP connectivity from another container on the same network. The name `sfs-api` is only a learning-example name; the container is running NGINX, not an actual API.

## Publish a container port

```bash
docker run -d --name sfs-web -p 127.0.0.1:8081:80 nginx:alpine
docker port sfs-web
```

Open `http://127.0.0.1:8081` on the Docker host. The mapping publishes host loopback port `8081` to container port `80`.

For a general host-port mapping, the syntax is:

```bash
docker run -d --name sfs-web-public -p 8080:80 nginx:alpine
```

This publishes host port `8080` to container port `80`. Binding without an explicit host IP can expose the port on host interfaces, subject to Docker and host networking configuration. Publish only ports that need host access.

## Inspect containers and published ports

```bash
docker ps -a
docker inspect sfs-api
docker port sfs-web
docker logs sfs-api
```

Check that the container is running, that it belongs to the expected network, and that the application is listening on the expected port and interface.

## Troubleshoot connectivity

```bash
docker network inspect sfs-app
docker exec sfs-api hostname
```

Check these in order:

1. Are both containers running?
2. Are they attached to a shared network?
3. Does the destination name resolve from the source container?
4. Is the destination application listening on the expected port and a reachable interface?
5. Can a TCP connection be established?
6. Does the application return a successful response?
7. Are firewall rules, routing, or application authentication blocking the request?

DNS resolution alone does not guarantee that a connection or application request will succeed. Inside a container, `localhost` refers to that container itself.

## Cleanup

Remove only the learning resources created above:

```bash
docker rm -f sfs-api sfs-web
```

If you also created `sfs-web-public`, remove it explicitly:

```bash
docker rm -f sfs-web-public
```

Remove the learning network after its containers have been disconnected or removed:

```bash
docker network rm sfs-app
```

Do not remove containers or networks that belong to other projects. Docker Desktop and non-Linux environments may differ in host-port access and network implementation details.
