variable "region" {}
variable "profile" {}

provider "aws" {
  region  = "${var.region}"
  profile = "${var.profile}"
  version = "~> 1.0"
}

terraform {
    backend "s3" {
    }
}

output "aws_region" {
  value = "${var.region}"
}