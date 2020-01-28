# objectify

A best effort XML to Dict package for Python3, with some additional input types just for convenience. The ordered YaML loader comes in handy at times. This is overall a very underwhelming package, but it's the cleanest way to break out XML to native Python3 datatype functions

## Note about encoding

The default file encoding is `ISO-8859-1`. You can specify the encoding as a keyword argument to `objectify_open()` if you'd like

## XML Loader

The XML loader will do as best as possible to load XML into a native Python `dict()` type. There is not necessarily any "perfect" or "correct" way to do this, so test your input and output carefully before relying on it

## YaML Loader

The YaML loader will perform an ordered load, which can be very useful for configuration files and self-templated YaML files. Self-templating may be added later but it may make more sense to keep it separate for now ...

## License

BSD 3-Clause License, 2020, copyright@mzpqnxow.com
