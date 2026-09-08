# `Kubernetes` Production Operations

## Goal
Run containers predictably under failure, scaling, deployment, and security constraints.

## Workload Contract
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
  selector:
    matchLabels: { app: api }
  template:
    metadata:
      labels: { app: api }
    spec:
      containers:
        - name: api
          image: registry.example.com/api:2026.09.08
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
          resources:
            requests: { cpu: 100m, memory: 256Mi }
            limits: { cpu: 500m, memory: 512Mi }
          readinessProbe:
            httpGet: { path: /ready, port: 8080 }
          livenessProbe:
            httpGet: { path: /live, port: 8080 }
          startupProbe:
            httpGet: { path: /live, port: 8080 }
            failureThreshold: 30
            periodSeconds: 5
```
Use immutable image references where possible and separate readiness from liveness. A liveness probe should not restart an instance merely because a dependency is temporarily unavailable.

## Availability
Use PodDisruptionBudgets, topology spread constraints, anti-affinity where justified, graceful termination, and enough replicas for zone failure. Validate that autoscaling has meaningful CPU, memory, or custom signals.

## Security
Use namespaces, RBAC least privilege, network policies, admission controls, non-root containers, restricted capabilities, signed images, secret encryption, and isolated service accounts. Do not assume a namespace alone is a security boundary.

## Configuration
Keep declarative manifests versioned. Separate config from images, validate configuration in CI, and avoid injecting unbounded environment data. Use external secret management where appropriate.

## Rollouts
Use max unavailable/surge deliberately, observe readiness and business metrics, and pause or rollback on error/latency regression. Ensure the application supports mixed-version traffic during rolling updates.

## Operations
Monitor node pressure, pod restarts, pending pods, scheduling failures, resource throttling, API server health, control-plane capacity, and storage. Test backup restore, not backup creation.

## Checklist
- [ ] Images are pinned, scanned, and non-root.
- [ ] Requests/limits reflect measured behavior.
- [ ] Startup, readiness, and liveness probes are distinct.
- [ ] PDB and topology policy protect availability.
- [ ] RBAC and network policies are least-privileged.
- [ ] Secrets are encrypted and access-controlled.
- [ ] Rollout and rollback are observable.
- [ ] Cluster and application backups have restore tests.
- [ ] Resource, restart, and scheduling alerts have owners.

## Kesalahan Umum / Pitfalls

- No resource limits — a runaway pod takes down the node.
- Running as root or with excessive RBAC.
- No probes — rolling updates kill healthy pods.
- State in pods — ephemeral storage is lost on restart.

## Trade-off dan Kapan Tidak Pakai

- `Kubernetes` is powerful but operationally heavy — consider managed platforms.
- Helm charts add abstraction — sometimes plain manifests are clearer.
- Multi-node clusters need careful networking — start small.

## References
- https://kubernetes.io/docs/concepts/configuration/overview/
- https://kubernetes.io/docs/concepts/security/
- https://kubernetes.io/docs/tasks/run-application/configure-pdb/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
