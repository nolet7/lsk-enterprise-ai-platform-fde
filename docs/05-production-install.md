# Production deployment rehearsal (NOT EXECUTED)
Prereqs: customer-owned GCP project with required APIs/billing, Terraform, gcloud, kubectl, Helm, Argo CD, private image registry and trusted signed image.
1. Security reviewer approves security/required-gates.md; BLOCK if any incomplete.
2. `cd terraform/gcp; terraform init; terraform fmt -check; terraform validate; terraform plan -var-file=terraform.tfvars`. Review plan, access and cost before apply.
3. Customer operator applies approved plan; `gcloud container clusters get-credentials lsk-ai-demo --region us-central1 --project YOUR_PROJECT`.
4. Configure private endpoint routing, Cloud NAT, WIF, registry and approved secrets. Provision authenticated Prometheus scrape and OTLP collector.
5. Publish reproducibly built, signed image digest; supply helm values with image.digest, OIDC issuer/audience, model endpoint and external secret reference.
6. `helm lint helm/lsk-platform -f customer-values.yaml`; `helm template lsk helm/lsk-platform -f customer-values.yaml`; `kubectl apply -f gitops/app.yaml` only after image and network verification.
7. Run scripts/verify-k8s.sh and tests, synthetic load and manual acceptance. Generate DR/rollback evidence before any production traffic.
8. Roll back with Argo CD previous approved Git revision or `helm rollback` (only when Helm owns the release), plus data migration rollback plan.
Important: default image digest is intentionally unset; chart deployment fails closed without it.
