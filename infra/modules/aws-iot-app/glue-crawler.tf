resource "aws_glue_crawler" "glue_crawler" {
  database_name = aws_glue_catalog_database.aws_glue_catalog_database.name
  name          = "example"
  role          = aws_iam_role.glue_crawler.arn

  schedule = "cron(0 0 * * ? *)"
  
  description   = "create a Glue DB and the crawler to crawl an s3 bucket "
  s3_target {
    path = "s3://${aws_s3_bucket.sensor_storage.arn}"
  }
}

resource "aws_glue_catalog_database" "aws_glue_catalog_database" {
  name = "MyCatalogDatabase"
}



resource "aws_iam_role" "glue_crawler" {
  name = local.name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "glue.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}


# attach iam policies
# https://docs.aws.amazon.com/glue/latest/dg/getting-started-access.html

data "aws_iam_policy" "AWSGlueServiceRole" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}
data "aws_iam_policy" "AmazonS3FullAccess" {
  arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "glue" {
  role       = "${aws_iam_role.glue_crawler.name}"
  policy_arn = "${aws_iam_policy.AWSGlueServiceRole.arn}"
}

resource "aws_iam_role_policy_attachment" "glue" {
  role       = "${aws_iam_role.glue_crawler.name}"
  policy_arn = "${aws_iam_policy.AmazonS3FullAccess.arn}"
}