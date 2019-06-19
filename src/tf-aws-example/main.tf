
variable "access_key" {}
variable "secret_key" {}
variable "region" {
  default = "us-east-1"
}

terraform {
    backend "s3" {
    }
}


provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.region}"
  version = "~> 2.7"
}

resource "aws_instance" "example" {
  ami           = "ami-2757f631"
  instance_type = "t2.micro"

  tags = {
    name = "example_ec2_micro"
  }
}

output "aws_instance_ip" {
    value = "not_impl"
}