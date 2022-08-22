terraform {
  #   backend "s3" {
  #     bucket         = "terraform-state-backend"
  #     key            = "terraform.tfstate"
  #     region         = "ap-southeast-2"
  #     dynamodb_table = "terraform_state"
  #   }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.24.0"
    }
  }
}

provider "aws" {
  region     = var.region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}