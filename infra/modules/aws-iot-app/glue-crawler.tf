# resource "aws_glue_crawler" "example" {
#   database_name = aws_glue_catalog_database.aws_glue_catalog_database.name
#   name          = "example"
#   role          = aws_iam_role.example.arn

#   s3_target {
#     path = "s3://${aws_s3_bucket.sensor_storage.arn}"
#   }
# }

# resource "aws_glue_catalog_database" "aws_glue_catalog_database" {
#   name = "MyCatalogDatabase"
# }



# resource "aws_iam_role" "glue_crawler" {
#   name = local.name

#   assume_role_policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "Service": [
#           "glue.amazonaws.com"
#         ]
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }
# EOF
# }


# attach iam policies
# https://docs.aws.amazon.com/glue/latest/dg/getting-started-access.html