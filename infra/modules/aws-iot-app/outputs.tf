output "iot_topic" {
  value = "topic/${local.iot_topic}"
}


output "certificate_pem" {
    value = aws_iot_certificate.certificate_pem
}

output "certificate_pem" {
    value = aws_iot_certificate.private_key
}

# need to generate a CA certificate