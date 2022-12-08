resource "aws_s3_bucket" "sensor_storage" {
  bucket        = "${local.project_name}-bucket"
    tags = {
        Name        = "sensor bucket"
        Environment = "Dev"
  }
}

resource "aws_s3_bucket_acl" "example" {
  bucket = aws_s3_bucket.sensor_storage.id
  acl    = "private"
}



