
import os
from singer import utils
from streamduo.client import Client

REQUIRED_CONFIG_KEYS = ["streamId", "clientId", "clientSecret"]
test_record = {"key1": "val1"}


def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    config = args.config
    # Write a simple Rec
    record_controller = Client(config['clientId'], config['clientSecret']).get_record_controller()
    write_record_response = record_controller.write_record(config['streamId'], test_record)

    # use tap to read unread
    stream = os.popen('tap-streamduo -c config.json')
    output = stream.read()
    if "\"dataPayload\": {\"key1\": \"val1\"}" not in output:
        raise Exception("Record Not Found")


if __name__ == "__main__":
    main()
