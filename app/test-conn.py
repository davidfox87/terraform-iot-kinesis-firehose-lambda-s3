from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json
import argparse
import sys
import os 


received_all_event = threading.Event()

# target_ep = 'axb6ef1ye7l5s-ats.iot.us-west-1.amazonaws.com' # endpoint for the device registered in the cloud
# thing_name = 'ratchet'
ca_filepath = './device-crt-and-keys/RSA-AmazonRootCA1.pem'

# pub_topic = 'device/{}/data'.format(thing_name)


def parse_arguments(argv):
        """Parse command line arguments
        Args:
        argv (list): list of command line arguments including program name
        Returns:
        The parsed arguments as returned by argparse.ArgumentParser
        """
        parser = argparse.ArgumentParser(description='Training')

        parser.add_argument('--client_id',
                        type=str,
                        help="The ID that uniquely identifies this device in the AWS Region")

        parser.add_argument('--target_endpoint',
                        type=str,
                        help="endpoint for the thing device")

        parser.add_argument('--ca_file',
                        type=str,
                        help="AmazonRootCA file path")

        parser.add_argument('--key',
                        type=str,
                        help="Path to your key in PEM format.")

        parser.add_argument('--cert',
                        type=str,
                        help='Path to your client certificate in PEM format.')

        parser.add_argument('--topic',
                        type=str,
                        help='topic name to publish messages to')
        
        parser.add_argument('--message_string',
                        type=str,
                        help='message to publish')

        args, _ = parser.parse_known_args(args=argv[1:])

        return args



# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))
                
# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))


def main(argv=None):
        
    args = parse_arguments(sys.argv if argv is None else argv)

    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    proxy_options = None
    # establish a connection with AWS IoT Core by using the MQTT protocol
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=args.target_endpoint,
        port=8883,
        cert_filepath=args.cert,
        pri_key_filepath=args.key,
        client_bootstrap=client_bootstrap,
        ca_filepath=args.ca_file,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=args.client_id,
        clean_session=True,
        keep_alive_secs=30,
        http_proxy_options=proxy_options)

    print("Connecting to {} with client ID '{}'...".format(
        args.target_endpoint, args.client_id))

    #Connect to the gateway
    while True:
        try:
            connect_future = mqtt_connection.connect()
        # Future.result() waits until a result is available
            connect_future.result()
        except:
            print("Connection to IoT Core failed...  retrying in 5s.")
            time.sleep(5)
            continue
        else:
            print("Connected!")
            break       
    


    pub_topic = args.topic
    print ('Publishing message on topic {}'.format(pub_topic))

    message_count = 5

    if args.message_string:
        if message_count == 0:
            print ("Sending messages until program killed")
        else:
            print ("Sending {} message(s)".format(message_count))

        publish_count = 1
        while (publish_count <= message_count) or (message_count == 0):
            message = "{} [{}]".format(args.message_string, publish_count)
            print("Publishing message to topic '{}': {}".format(args.message_topic, message))
            message_json = json.dumps(message)
            mqtt_connection.publish(
                topic=args.message_topic,
                payload=message_json,
                qos=mqtt.QoS.AT_LEAST_ONCE)
            time.sleep(1)
            publish_count += 1


    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")

if __name__ == '__main__':
    main()

