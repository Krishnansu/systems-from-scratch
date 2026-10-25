# Lesson 125 — Envoy Command Reference

Use only local files and environments you are authorized to inspect. Do not restart or reconfigure shared proxies for this lesson.

## Validate a Local Configuration

If Envoy is installed and `./envoy.yaml` is your own local configuration:

```bash
envoy --version
envoy --mode validate -c ./envoy.yaml
```

Check the options supported by your installed Envoy version. Validation checks configuration acceptance; it does not prove that upstream services are reachable or that the intended traffic flow works.

## Inspect an Existing Kubernetes Workload (Optional)

```bash
kubectl config current-context
kubectl get pods -n <namespace>
kubectl get pod <pod-name> -n <namespace> -o yaml
kubectl describe pod <pod-name> -n <namespace>
```

Look at container images, arguments, ports, probes, resources, and configuration references. A container name alone does not prove that it runs Envoy. These commands do not expose the full active Envoy configuration in every deployment.

## Configuration Walkthrough

In a static HTTP proxy configuration, identify:

1. `listeners`: incoming address and port.
2. `filter_chains`: applicable connection-processing path.
3. `http_connection_manager`: HTTP processing and route configuration.
4. `routes`: request matching and selected cluster.
5. `clusters`: upstream connection and load-balancing configuration.
6. `load_assignment` / endpoints: concrete host and port destinations.

A route pointing to a cluster does not itself discover endpoints. Dynamic deployments may receive resource updates through xDS.

## Optional Admin Interface

Envoy's admin interface can expose sensitive configuration and runtime information. Do not assume it is enabled or publicly reachable. Only inspect it when explicitly authorized and when you know the configured local address; never expose it to untrusted networks.

## Safety and Interpretation

- Prefer validation and read-only inspection.
- Do not apply configuration, restart proxies, or change production resources for this exercise.
- Treat configuration, logs, and admin output as potentially sensitive.
- A valid configuration does not prove endpoint reachability, correct routing intent, or application health.
- Retries and health checks depend on the active configuration or surrounding control plane.

## Related Lessons

- [123 — API Gateway](../notes/123-api-gateway.md)
- [124 — Sidecars](../notes/124-sidecars.md)
- [125 — Envoy](../notes/125-envoy.md)
