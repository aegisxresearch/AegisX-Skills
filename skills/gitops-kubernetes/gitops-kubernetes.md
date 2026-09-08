# GitOps & `Kubernetes` Delivery

## Tujuan

Menjadikan repo Git satu-satunya sumber kebenaran untuk state `Kubernetes`: perubahan lewat PR, sinkronisasi otomatis, drift terdeteksi, rollback = revert commit.

## Prasyarat

- `Kubernetes` dasar (deployment, service, manifest)
- Familiar dengan git dan CI/CD

## Konsep inti

1. **Prinsip GitOps** — (1) state deklaratif di Git, (2) tidak ada perubahan manual ke cluster, (3) operator menarik state dan menyinkronkan, (4) drift selalu dikoreksi/dilaporkan.
2. **`Argo CD` vs Flux** — `Argo CD` populer untuk aplikasi + rollback UI; Flux kuat untuk bootstrap dan dependensi (kustomize-controller). Pilih berdasarkan kebutuhan, keduanya valid.
3. **Struktur repo** — pola *monorepo config* atau *app-of-apps*: environment (`dev`/`staging`/`prod`) terpisah jelas; jangan mencampur.
4. **Kustomize/Helm** — template + overlay; chart di-pin versi; jangan commit `latest` tanpa kontrol.
5. **Sync & drift** — auto-sync dengan prune (hati-hati) atau manual dengan diff review; alert saat drift muncul.
6. **Security** — cluster access via operator (bukan kubeconfig di CI); secret via External Secrets/Sealed Secrets; RBAC di repo config.
7. **Progressive delivery** — Argo Rollouts/Flagger: canary atau blue-green berbasis metrics sebelum full rollout; rollback otomatis saat SLO langgar.

## Contoh Application (illustrative, `Argo CD`)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/infra.git
    path: apps/api/overlays/prod
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: api
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Checklist produksi

- [ ] Semua perubahan cluster lewat PR (review + CI)
- [ ] Auto-sync + selfHeal diputuskan sadar risiko; prune diuji di staging dulu
- [ ] Drift detection aktif; alert saat drift
- [ ] Chart/versi image di-pin; `latest` tidak ada di prod
- [ ] Secrets bukan plaintext di repo (Sealed/External Secrets)
- [ ] RBAC minimum; operator tidak dapat mengubah semua namespace
- [ ] Rollback = revert commit; diuji
- [ ] Progressive delivery untuk service penting (canary + metrics)
- [ ] Disaster recovery: bootstrap ulang cluster dari repo diuji berkala

## Kesalahan umum

- Perubahan manual ke cluster — Git jadi tidak sinkron (drift permanen).
- `prune: true` tanpa hati-hati — resource yang tidak diharapkan terhapus.
- Secret plaintext di repo GitOps.
- Satu repo raksasa tanpa pembatas environment — blast radius besar.
- Sync failure diabaikan — environment lama diam-diam.

## Referensi

- https://argo-cd.readthedocs.io/ — `Argo CD`
- https://fluxcd.io/docs/ — Flux
- https://opengitops.dev/ — prinsip OpenGitOps
- https://argoproj.github.io/argo-rollouts/ — Argo Rollouts

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
