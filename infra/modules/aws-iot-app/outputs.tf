output "iot_topic" {
  value = "topic/${local.iot_topic}"
}


resource "local_sensitive_file" "public_key" {
  filename = "${path.module}/../certs/test.public.key"
  content  = aws_iot_certificate.things_cert.public_key
}

resource "local_sensitive_file" "private_key" {
  filename = "${path.module}/../certs/test.private.key"
  content  = aws_iot_certificate.things_cert.private_key
}

resource "local_sensitive_file" "cert_pem" {
  filename = "${path.module}/../certs/test.cert.pem"
  content  = aws_iot_certificate.things_cert.certificate_pem
}

output "iot_endpoint" {
  value = data.aws_iot_endpoint.endpointIOT.endpoint_address
}

output "lambda_name" {
 value = aws_lambda_function.kinesis.id
}