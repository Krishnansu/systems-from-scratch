# Lesson 103 — Docker Networks

## Objectives
- Explain how containers communicate with other containers, the host, and external systems.
- Understand network namespaces, virtual Ethernet pairs, and Linux bridges.
- Distinguish the default bridge from user-defined bridge networks.
- Explain container ports versus published host ports.
- Troubleshoot common container connectivity problems.

## Prerequisites
- Lesson 100 — Namespaces
- Lesson 102 — Volumes
- Basic IP networking, TCP ports, and DNS

## Theory
Containers need networking to communicate with APIs, databases, caches, and external services. Docker configures networking so containers can communicate without sharing the host's entire network environment.

A container's **network namespace** isolates its network interfaces, routes, and network-related state. On typical Linux bridge networking, a virtual Ethernet (veth) pair connects the container's network interface to a Linux bridge on the host. Docker configures addressing, routing, name resolution, and any required firewall or NAT rules.

```text
Container A                         Container B
+------------------+                +------------------+
| Network namespace|                | Network namespace|
| eth0             |                | eth0             |
+--------+---------+                +---------+--------+
         | veth pair                          | veth pair
         +----------------+  +----------------+
                          v  v
                    Linux bridge
                          |
                 Host routing / NAT
                          |
                    External network
```

This is a simplified model of common Linux bridge networking. Exact implementation details differ by network driver and platform.

## Real World Example
Consider a web application with three services:

```text
Browser
   |
   | http://localhost:8080
   v
Web container (port 80)
   |
   | internal network connection
   v
API container (port 3000)
   |
   | postgres:5432
   v
PostgreSQL container (port 5432)
```

The web service may publish a port for host access. The API and PostgreSQL can communicate over a shared private Docker network without publishing PostgreSQL's port to the host.

Inside the API container, `localhost` refers to the API container itself, not the PostgreSQL container. The API should connect to the database using its network name, such as `postgres:5432`, when both are attached to a suitable user-defined network.

## Deep Dive

### Network drivers
- **Bridge:** Common choice for containers on one Docker host.
- **Host:** Uses the host network namespace on supported Linux configurations, reducing network isolation.
- **None:** Provides no normal external container networking.
- **Overlay:** Connects services across multiple Docker hosts in supported configurations.

Docker Desktop networking differs in implementation from native Linux Docker. Driver availability and behavior depend on the environment.

### Default bridge versus user-defined bridge
A user-defined bridge is generally preferable for a multi-container application because Docker provides automatic container-name resolution on that network and allows better network segmentation. Containers must share a network to communicate directly over it.

### Container ports versus published ports
- A **container port** is the port on which the application listens inside its network namespace.
- A **published host port** forwards traffic arriving at a host address and port to a container port.
- `-p 8080:80` maps host port `8080` to container port `80`.
- `-p 127.0.0.1:8081:80` binds the published port to the host's loopback address, limiting access through that binding to the host itself.

Container-to-container communication normally uses the destination container's service port, not its published host port.

### DNS, reachability, and health
These are separate checks:
1. **Name resolution:** Does the name resolve to an address?
2. **Reachability:** Can packets and connections reach the destination?
3. **Listening service:** Is a process listening on the expected address and port?
4. **Application health:** Does the service successfully handle the request?

A successful DNS lookup does not guarantee that a TCP connection or application request will succeed.

### Troubleshooting checklist
1. Check whether the containers are running: `docker ps -a`.
2. Inspect logs: `docker logs <container>`.
3. Inspect network membership and configuration: `docker network inspect <network>`.
4. Confirm both containers share a network when direct communication is expected.
5. Test name resolution and connectivity from the relevant container or network.
6. Verify the application listens on the expected port and interface; binding only to `127.0.0.1` inside a container can prevent access from other containers.
7. Inspect published ports with `docker port <container>`.
8. Check host firewall rules, routing, and application-level authentication when appropriate.

## Hands-on Exercise

### 1. Inspect the default bridge
```bash
docker network ls
docker network inspect bridge
```

### 2. Create a user-defined network
```bash
docker network create sfs-app
docker network inspect sfs-app
```

### 3. Test container-name resolution and HTTP connectivity
```bash
docker run -d --name sfs-api --network sfs-app nginx:alpine
docker run --rm --network sfs-app alpine wget -qO- http://sfs-api
```

The temporary Alpine container should retrieve the NGINX welcome page through the network name. This demonstrates name resolution and connectivity on the user-defined bridge.

### 4. Publish a port for host access
```bash
docker run -d --name sfs-web -p 127.0.0.1:8081:80 nginx:alpine
docker port sfs-web
```

Open `http://127.0.0.1:8081` on the Docker host. If Docker is running inside a VM or Docker Desktop, host-access behavior may differ by environment.

### 5. Inspect and clean up
```bash
docker network inspect sfs-app
docker rm -f sfs-api sfs-web
docker network rm sfs-app
```

Only remove the named learning containers and network created in this exercise.

## Common Misconceptions
- Containers do not automatically share `localhost` or the same network namespace.
- A container port does not have to be published for another container on the same network to reach it.
- Publishing a port is not the same as attaching containers to a shared network.
- The default bridge does not provide the same automatic container-name resolution behavior as a user-defined bridge.
- DNS resolution does not prove that the service is listening or healthy.
- A published port should not be exposed unnecessarily, especially for private databases.
- Network isolation is not a substitute for application authentication and authorization.

## Summary
Docker networking provides connectivity and isolation between containers and other systems. Network namespaces isolate network state, while drivers such as bridge and overlay define connectivity. User-defined bridge networks make multi-container communication easier through container-name resolution. Port publishing controls how traffic reaches a container through a host address and port.

## Key Takeaways
- Network namespaces isolate interfaces, routes, and other network state.
- On typical Linux bridge networking, veth pairs connect container interfaces to a host-side bridge.
- User-defined bridges are a good default for communicating services on one Docker host.
- Use container or service names and container ports for communication over a shared Docker network.
- `-p 8080:80` maps host port 8080 to container port 80.
- Inside a container, `localhost` means that container itself.
- Diagnose DNS, connectivity, listening ports, and application health separately.
- Publish only the ports that need host or external access.

## Reflection Questions
1. What does a network namespace isolate?
2. How does a veth pair connect a container to a Linux bridge?
3. Why is a user-defined bridge useful for a multi-container application?
4. In `-p 8080:80`, which port belongs to the host and which belongs to the container?
5. Why does `localhost` inside an API container not refer to a separate PostgreSQL container?
6. If `postgres` resolves to an IP but `postgres:5432` cannot be reached, what would you investigate?
7. Why should a database port usually remain unpublished when only the application needs access?

## What's Next
Lesson 104 — Docker Compose: defining and operating multi-container applications declaratively.
