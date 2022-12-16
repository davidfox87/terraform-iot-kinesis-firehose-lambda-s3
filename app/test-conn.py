import sys
import threading
import time
import json
import argparse
import sys
import base64

from awscrt import mqtt, io
import sys
import threading
import time
from uuid import uuid4
import json
from awsiot import mqtt_connection_builder

import pandas as pd


received_all_event = threading.Event()


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

        parser.add_argument('--endpoint',
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

        parser.add_argument('--count',
                        type=int,
                        help='message to publish',
                        default=5)

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
        endpoint=args.endpoint,
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
        args.endpoint, args.client_id))

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

    message_count = args.count


    if message_count == 0:
        print ("Sending messages until program killed")
    else:
        print ("Sending {} message(s)".format(message_count))


    df = pd.read_csv('records.csv')
    df['json'] = df.apply(lambda x: x.to_json(), axis=1)
    messages = df['json'].values

    for message in messages:
        publish(mqtt_connection, args.topic, message)
    
    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")



def publish(mqtt_connection, topic, message):
    print("Publishing message to topic '{}': {}".format(topic, message))
    mqtt_connection.publish(
        topic=topic,
        payload=message,
        qos=mqtt.QoS.AT_LEAST_ONCE)
    time.sleep(1)
    publish_count += 1


if __name__ == '__main__':
    main()

    