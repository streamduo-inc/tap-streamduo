#!/usr/bin/env python3
import os
import json
import time

import singer
from singer import utils, Transformer, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema
from streamduo.client import Client


REQUIRED_CONFIG_KEYS = ["streamId", "clientId", "clientSecret"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    """Get Absolute Path"""
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path, encoding='UTF-8') as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():
        stream_metadata = []
        key_properties = []
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def sync(config, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.streams:
        LOGGER.info(f"Syncing stream:" + stream.tap_stream_id)

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )
        polling = True
        tries = 0
        record_controller = Client(config['clientId'],
                                   config['clientSecret']).get_record_controller()
        while polling:
            time.sleep(2*tries)
            read_unread_response = record_controller.read_unread_records(config['streamId'],
                                                                         True, 100)
            if read_unread_response.status_code != 200:
                LOGGER.info(f"API Error, response code {read_unread_response.status_code}.")
                tries = tries + 1
                if tries == 6:
                    polling = False
                    LOGGER.warn("API Error, unable to connect, not responding with 200 code.")
                    raise Exception("API Error, unable to connect.")
            else:
                tap_data = read_unread_response.json()
                for row in tap_data:
                    with Transformer() as transformer:
                        singer.write_record(stream.tap_stream_id, transformer.
                                            filter_data_by_metadata(row, metadata.to_map(stream.metadata)))
                if len(tap_data) < 100:
                    polling = False



@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()
        sync(args.config, catalog)


if __name__ == "__main__":
    main()
