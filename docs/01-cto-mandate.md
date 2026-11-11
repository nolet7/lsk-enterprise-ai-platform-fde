# CTO mandate and measurable acceptance
Customer: fictional LSK commercial IT, B2B sales, procurement, finance, support.
Existing workflows must remain usable when inference fails.
**POC gate:** legacy ticket/create/deployment request endpoints and browser console work; real inference returns a grounded answer when configured; tests and local smoke pass.
**Pilot gate:** identity verification, tenant-scoped data boundaries, denial tests, audit, load and evaluation evidence; no demo headers.
**Production gate:** cloud infrastructure must be deployed in a customer-approved environment, monitored, restored from backups, load-tested, and security signed off. IaC in Git alone is NOT a deployment.
Non-goals: autonomous payment, supplier approval, and unrestricted CRM/ERP writes.
