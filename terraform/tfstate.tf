terraform {
    backend "s3" {
      bucket         = var.terraform_state_bucket
      key            = "terraform.tfstate"
      region         = "ap-southeast-2"
      dynamodb_table = var.terraform_state_dynamdb
    }
}