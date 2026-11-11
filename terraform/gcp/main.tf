resource "google_compute_network" "main" {
  name = var.network_name
  auto_create_subnetworks = false
}
resource "google_compute_subnetwork" "private" {
  name = "${var.cluster_name}-subnet"
  region = var.region
  network = google_compute_network.main.id
  ip_cidr_range = "10.40.0.0/20"
  secondary_ip_range {range_name="pods",ip_cidr_range="10.44.0.0/16"}
  secondary_ip_range {range_name="services",ip_cidr_range="10.45.0.0/20"}
  private_ip_google_access = true
}
resource "google_container_cluster" "main" {
  name = var.cluster_name
  location = var.region
  network = google_compute_network.main.id
  subnetwork = google_compute_subnetwork.private.id
  remove_default_node_pool = true
  initial_node_count = 1
  deletion_protection = true
  ip_allocation_policy {
    cluster_secondary_range_name = "pods"
    services_secondary_range_name = "services"
  }
  private_cluster_config {
    enable_private_nodes = true
    enable_private_endpoint = false
    master_ipv4_cidr_block = "172.16.1.0/28"
  }
  workload_identity_config {workload_pool="${var.project_id}.svc.id.goog"}
  release_channel {channel="REGULAR"}
  network_policy {enabled=true}
}
resource "google_container_node_pool" "cpu" {
  name = "cpu-pool"
  location = var.region
  cluster = google_container_cluster.main.name
  node_count = var.node_count
  node_config {
    machine_type = "e2-standard-4"
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    workload_metadata_config {mode="GKE_METADATA"}
    labels = {workload="cpu"}
  }
}
