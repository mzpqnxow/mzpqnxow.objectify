# objectify

A best effort XML to Dict package for Python3, with some additional input types just for convenience. The ordered YaML loader comes in handy at times. This is overall a very underwhelming package, but it's the cleanest way to break out XML to native Python3 datatype functions

## Design and Implementation Goals

There are a few specific use-cases that this was written for which required a few specific design requirements

1. Must be able to deal with very large (>1GB) files without causing enormous allocations in the Python process. This is only really possible for line-based text files and JSON-lines format files. Luckily the primary use-case is multi-gigabyte JSON Lines formatted files. For this reason, all file loading functions are implemented as generators whenever technically possible
2. Must have a flexible caller interface that accepts a filename, a stream-like object or a string of data as the input. This must be seamless without the caller even knowing or caring about what the context of the incoming data is
3. Must be able to load all supported formats into native, built-in Python objects. For example, XML must be loaded into a `dict()` and not as an in-memory XML object
4. XML ingestion must be as robust as possible to avoid failing to load unusually structured XML documents into an object
5. YaML ingestion must support preserving order as well as "self-templating"

That's pretty much it. The focus is on avoiding memory-pressure but still dealing with data as built-in Python data types as well as providing easy to use interfaces and templating where applicable

## Note about encoding

The default file encoding is `ISO-8859-1`. You can change this if you want, there is no proper mechanism to do so but you can edit `objectify/encoding.py` and replace it with `utf-8` or whatever you need

## Testing

There are two simple test-cases, one is XML, the other is YAML with self-templating. These can be found in `tests/` and can be tested using `test.py`. These are really just for regression tests when simple changes are made, they don't demonstrate a small memory footprint as they are very small

## Dependencies

You'll need both jinja2 as well as ujson. No other dependencies are required

## Loaders

The following loaders are provided, some more useful than others

### XML Loader

The XML loader will do as best as possible to load XML into a native Python `dict()` type. There is not necessarily any "perfect" or "correct" way to do this, so test your input and output carefully before relying on it

### YaML Loader

The YaML loader will perform an ordered load, which can be very useful for configuration files and self-templated YaML files. The use-case for the loader is self-referencing configuration or data description files. The following is an example of self-templating:

```
user: user
root: /
home: "{{ root }}/home"
user_home: "{{ home }}/{{ user }}"
user_ssh: "{{ user_home }}/.ssh"
...
```

This should render into a Python `dict()` as:

```
{
	"user": "user",
	"root": "/",
	"home": "/home",
	"user_home": "/home/user",
	"user_ssh": "/home/user/.ssh"

}
```

This feature is very useful for configuration files where values are repeated throughout the file

### JSON / JSON Lines Loader

The JSON loader is trivial and is only more convenient that a basic one-line loader because it has exception handling and supports a string, file path or file stream as the first argument. It will determine what action to take without any hints from the caller.

The JSON-Lines loader provides the same functionality as the JSON loader except it emphasizes loading the file one object at a time to avoid memory pressure. This is done using a very simple generator

### Text Lines Loader

Reads files that are line-based and may contain comments. Also built to avoid memory pressure in the face of multi-gigabyte files

### CSV Loader

There is currently no CSV loader but the approach will be much the same as the Lines Loader, loading a single line at a time to avoid memory pressure with very large files

## TODO

Consider adding dynamic compression detection and loading. This will break the avoidance of memory pressure though, depending on the file format and the compression algorithm

## FIN

That's all. There's not much to this, really

## License

BSD 3-Clause License, 2020, copyright@mzpqnxow.com
