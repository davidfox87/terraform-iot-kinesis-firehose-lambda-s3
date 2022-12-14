# terraform-iot-kinesis-firehose-lambda-s3

```
terraform init
terraform get
terraform plan
terraform apply
```

```
python3 test-conn.py --endpoint axb6ef1ye7l5s-ats.iot.us-west-1.amazonaws.com --ca_file RSA-AmazonRootCA1.pem --cert test.cert.pem --key test.private.key --client_id basicPubSub --topic topic/sensors --count 0 --message 'hello'
```