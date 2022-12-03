resource "aws_iot_policy" "tf_policy" {
  name = "PubSubToAnyTopic"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
            "iot:Publish",
            "iot:Subscribe",
            "iot:Connect",
            "iot:Receive"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

// attach policy to certificate
resource "aws_iot_policy_attachment" "thing_policy_attachment" {
  policy = aws_iot_policy.tf_policy.name
  target = aws_iot_certificate.things_cert.arn
}