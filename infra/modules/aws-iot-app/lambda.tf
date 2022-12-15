# change the lambda function to use the docker image pushed to ecr
# data aws_ecr_image lambda_image {
#  repository_name = local.ecr_repository_name
#  image_tag       = local.ecr_image_tag
# }
# data "aws_ecr_repository" "lambda_image" {
#   name = local.ecr_repository_name
# }


resource "aws_lambda_function" "lambda_processor" {
    function_name    = "${local.project_name}-lambda"
    role             = "${aws_iam_role.lambda_exec.arn}"
    timeout = 300
    image_uri = "880572800141.dkr.ecr.us-west-1.amazonaws.com/kinesis-lambda:latest"
    package_type = "Image"

    depends_on = [
        aws_iam_role_policy_attachment.lambda_logs,
        aws_cloudwatch_log_group.example,
    ]
}

resource "aws_iam_role" "lambda_exec" {
  name = "${local.project_name}-lambda-exec"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_iam_policy" "AWSLambdaKinesisExecutionRole" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole"
}


resource "aws_iam_role_policy_attachment" "lambda_kinesis" {
  role = "${aws_iam_role.lambda_exec.name}"
  policy_arn = "${data.aws_iam_policy.AWSLambdaKinesisExecutionRole.arn}"
}

# resource "aws_lambda_event_source_mapping" "event_source_mapping" {
#   batch_size        = 10
#   event_source_arn  = "${aws_kinesis_stream.sensors.arn}"
#   enabled           = true
#   function_name     = "${aws_lambda_function.kinesis.id}"
#   starting_position = "LATEST"
# }


# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${local.project_name}-lambda"
  retention_in_days = 14
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}










# resource "aws_lambda_function" "lambda_processor" {
#   filename      = "lambda.zip"
#   function_name = "firehose_lambda_processor"
#   role          = aws_iam_role.lambda_iam.arn
#   handler       = "exports.handler"
#   runtime       = "nodejs16.x"
# }