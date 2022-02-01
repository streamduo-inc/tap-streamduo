# tap-streamduo

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [StreamDuo](http://example.com)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

---

Copyright &copy; 2018 Stitch
