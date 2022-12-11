To test the lambda function using the the docker runtime interface emulator:
1. Build the docker image locally using the docker build command
```
docker build -t mylambda:latest .
```
2. Run the container image locally uding the docker run command
```
docker run -p 9000:8080 mylambda:latest
```

This command runs the image as a container and starts up an endpoint locally at ```localhost:90000/2015-03-31/functions/function/invocations```.

3. From a new terminal window, post an event with a base64 encode message ("Hello, from David Fox")
Run 
```
python3 test-lambda-client.py
```

This command will use the python requests library to send a post request to the container. It will invoke the lambda function running in the container image and will return a response.
