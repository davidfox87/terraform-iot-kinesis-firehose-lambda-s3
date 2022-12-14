resource "aws_iot_topic_rule" "rule" {
  name        = "${local.project_name}Kinesis"
  description = "Kinesis Rule"
  enabled     = true
  sql         = "SELECT * FROM 'topic/${local.iot_topic}'"
  sql_version = "2016-03-23"

  kinesis {
    role_arn    = "${aws_iam_role.iot.arn}"
    stream_name = "${aws_kinesis_stream.sensors.name}"
    partition_key = "$${newuuid()}"
  }

  firehose {
    delivery_stream_name = "${aws_kinesis_firehose_delivery_stream.sensors.name}"
    role_arn = "${aws_iam_role.iot.arn}"
  }
}

resource "aws_iam_role" "iot" {
  name = "${local.project_name}-iot-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "iot.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}

resource "aws_iam_role_policy" "iot_firehose" {
  name = "${local.project_name}-iot-firehose-policy"
  role = "${aws_iam_role.iot.id}"


  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "firehose:PutRecord",
          "firehose:PutRecordBatch",
        ],
        Resource = [
          "${aws_kinesis_firehose_delivery_stream.sensors.arn}"
        ],
        Effect = "Allow"
      },
    ]
  })
}


# Writes records to Kinesis Data Streams.
resource "aws_iam_role_policy" "iot_kinesis" {
  name = "${local.project_name}-iot-kinesis-policy"
  role = "${aws_iam_role.iot.id}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "kinesis:PutRecord",
        ],
        Resource = [
          "${aws_kinesis_stream.sensors.arn}"
        ],
        Effect = "Allow"
      },
    ]
  })
}
