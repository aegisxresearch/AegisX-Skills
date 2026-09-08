# GitHub Actions Workflow Engineering

## Goal
Workflows CI/CD yang cepat, berkeamanan default, dan DRY — perubahan pola CI dilakukan di satu tempat, bukan di setiap file workflow.

## Operating Model
```text
PR -> lint + test (parallel, cached) -> build artifact -> deploy (OIDC)
Semua job: permissions minimum, actions di-pin ke SHA
```

## Konsep Inti

### 1. Least privilege permissions
```yaml
permissions:
  contents: read        # default untuk semua job
jobs:
  release:
    permissions:
      contents: write   # hanya job ini yang butuh
```
Tanpa blok `permissions`, workflow mendapat token dengan hak luas — ini default yang harus diubah di setiap repo.

### 2. Pinning actions
```yaml
# Lemah: bisa berubah kapan saja
- uses: actions/checkout@v4
# Kuat: SHA penuh + versi sebagai komentar
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```
Untuk third-party actions (bukan `actions/*`), pinning ke SHA mencegah tag dipindah ke kode berbahaya.

### 3. Caching yang benar
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: npm            # cache package berdasarkan lockfile hash
```
Untuk Docker, gunakan buildx cache:
```yaml
- uses: docker/build-push-action@v6
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```
Cache yang sering gagal: menyimpan `node_modules` manual tanpa key berbasis lockfile — restore hit turun dan cache basi menumpuk.

### 4. Matrix tanpa duplikasi
```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest]
    python: ["3.11", "3.12"]
    exclude: [{ os: macos-latest, python: "3.11" }]
```
`fail-fast: false` penting: satu kegagalan di satu kombinasi tidak boleh menyembunyikan hasil kombinasi lain.

### 5. OIDC untuk cloud deploy
```yaml
permissions:
  id-token: write   # bukan simpan AWS_ACCESS_KEY_ID di secrets
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/ci-deploy
      aws-region: ap-southeast-1
```
Token berumur pendek, terikat ke repo dan branch — secret statis tidak pernah ada untuk dicuri.

### 6. Reusable workflows
```yaml
# .github/workflows/test.yml (dipanggil)
jobs:
  test:
    uses: org/shared-workflows/.github/workflows/node-test.yml@v1
    with:
      node-version: 22
```
Pola CI yang sama di 10 repo berubah di satu tempat. Batasi `@v1` dengan tag yang dikelola, bukan `@main`.

## Acceptance Checklist
- [ ] Blok `permissions` eksplisit di setiap workflow
- [ ] Actions pihak ketiga di-pin ke SHA penuh
- [ ] Dependensi di-cache dengan key berbasis lockfile
- [ ] Deploy cloud memakai OIDC, bukan long-lived secrets
- [ ] Pola CI yang berulang diekstrak ke reusable workflow
- [ ] Waktu CI p95 per PR terukur dan tidak melebihi 10 menit

## Kesalahan Umum / Pitfalls
- `pull_request_target` dengan checkout kode PR dan secret — langkah langsung untuk penyusupan.
- Secret di environment variable global job — terbaca oleh step apa pun termasuk script pihak ketiga.
- Semua dalam satu job raksasa — satu lint gagal membatalkan test yang sudah lama selesai.
- `continue-on-error: true` pada step security — status hijau yang berbohong.
- Cache tanpa batas — storage penuh, cache lama mengalahkan yang baru.

## Trade-off dan Kapan Tidak Pakai
- Matrix besar mempercepat feedback tapi menghabiskan menit billing — pilih kombinasi yang benar-benar berbeda perilakunya.
- Reusable workflow menambah indirection — untuk repo tunggal dengan satu workflow, ekstraksi berlebihan.
- OIDC butuh setup per cloud provider — untuk cloud yang tidak didukung, secrets terbatas scope masih wajar.
- Self-hosted runner memberi kontrol tapi memindahkan beban patching security ke Anda.

## Referensi
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
- https://docs.github.com/en/actions/using-workflows/reusing-workflows
- https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/caching-dependencies-to-speed-up-workflows

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
