terraform {
    backend "s3" {
      bucket         = var.terraform_state_bucket
      key            = "terraform.tfstate"
      region         = "ap-southeast-2"
      dynamodb_table = var.terraform_state_dynamdb
    }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.24.0"
    }
  }
}

provider "aws" {}