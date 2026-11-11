output "cluster_name" {value=google_container_cluster.main.name}
output "region" {value=var.region}
output "network" {value=google_compute_network.main.id}
