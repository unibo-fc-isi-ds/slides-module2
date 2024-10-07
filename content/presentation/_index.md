+++

title = "[DS] Presentation Mechanisms"
description = "Presentation Mechanisms for Distributed Systems"
outputs = ["Reveal"]
aliases = [
    "/presentation/",
    "/serialization/",
    "/rpc/"
]

+++

# Presentation Mechanisms for Distributed Systems

{{% import path="reusable/footer.md" %}}

---

## Context

- Nodes in distributed systems may be implemented in _different languages_ (e.g. C, Java, Python, etc.)
    * possibly running on _different platforms_ (e.g. Python, JVM, Node, etc.) and _OS_ (e.g. Windows, Linux, etc.)
    * possibly using _different data representations conventions_ (e.g. big-endian, little-endian, etc.)

- As long as nodes comply to the __same__ _communication protocols_ and _patterns_, technological issues should _not_ be a problem
    * __presentation__ mechanisms are responsible for _representing_ data in a __common format__
        + in order to _exchange_ information smoothly between _heterogeneous_ nodes

- So far all examples have been in _Python_ (for simplicity)...
    * so, in practice, the "common format" didn't need to be _explicitly_ defined

- ... but, in the _real world_, we need to _serialize_ and _deserialize_ data explicitly into/from a _common format_
    * this is the role of __data interchange formats__, such as:
        + [JavaScript Object Notation (JSON)](https://en.wikipedia.org/wiki/JSON) (_we will use this one_)
        + [Yet Another Markup Language (YAML)](https://en.wikipedia.org/wiki/YAML) (later renamed in "YAML Ain't Markup Language")
        + [eXtensible Markup Language (XML)](https://en.wikipedia.org/wiki/XML)
        + [Type–length–value (TLV)](https://en.wikipedia.org/wiki/Type-length-value)
        + [Protocol Buffers](https://en.wikipedia.org/wiki/Protocol_Buffers)
        + [Avro](https://avro.apache.org/)

---

## Content of the lecture

A lot of concepts to unpack here:

1. __(De)Serialization__: this is the _main goal_ of this lecture
    * _serialization_ is the process of converting an object into a stream of characters/bytes
    * _deserialization_ is the reverse process
    * both operations imply a _common_ target/source __data interchange format__ (e.g. JSON)
    * both operations are ___unavoidable__ in distributed systems programming

2. __Remote Procedure Call__ (RPC): this is a very common _interaction pattern_ in distributed systems
    * it allows a client program to _invoke_ a procedure from a remote server
    * it implies __(de)serializing__ _parameters_ and _results_ of the procedure
    * so it's the perfect _example_ to illustrate how (de)serialization is used _in practice_

3. __Authentication__: this is another _common_ concern in distributed systems
    * it implies clients providing _credentials_ to servers to _prove_ their identity
    * it is commonly _implemented_ by means of _RPC_...
    * ... so it's a good _example_ to illustrate how RPC is used _in practice_
    * this is _not_ strictly related to (de)serialization, but it's a _good_ example of _RPC_, and it _exploits_ (de)serialization a lot

---

{{% section %}}

# Information Representation 101
## (quick and practical excursus)

---

## Information Representation Recap (pt. 1)

- In electronic systems, information is represented as _binary data_
    * i.e. sequences of _0s_ and _1s_

- For many practical reasons, binary sequences are commonly grouped in _bytes_
    * _byte_ $\equiv$ _8 bits_ $\equiv$ _2 hexadecimal digits_
    * e.g. `0x00`$\equiv$ 0, `0x01` $\equiv$ 1, `0x02` $\equiv$ 2, ..., `0xFF` $\equiv$ 255

- Sequences of _bytes_ can be used to represent many _sorts_ of data, via ad-hoc __conventions__
    * e.g. _ASCII_ (for text): e.g. `0x41` $\equiv$ 45 $\equiv$ `A`  (cf. [ASCII Table](https://www.asciitable.com/))
    * e.g. _UTF-8_ (for text): e.g. `0xC3A0` $\equiv$ 50080 $\equiv$ `à` (cf. [UTF-8 Table](https://www.utf8-chartable.de/))
    * e.g. _little-endian_ (for 32-bit integers): e.g. `0x3000` $\equiv$ 3 (cf. [Endianness](https://en.wikipedia.org/wiki/Endianness))
    * e.g. _big-endian_ (for 32-bit integers): e.g. `0x0003` $\equiv$ 3 (cf. [Endianness](https://en.wikipedia.org/wiki/Endianness))

- Conventions $\approx$ data interchange formats
    * they define how _data_ is _encoded_ into _bytes_
    * they define how _bytes_ should be _decoded_ into _data_

> __The problem__: most programming languages / platforms / OS use _different_ conventions for representing data
> <br> __The solution__: _agree_ on the data format to use for _communication_

corollary: data interchange formats are an __essential__ aspect of every interaction pattern / protocol

---

## Two broad categories of data interchange formats

1. __Text-based__ formats: they rely on _characters_ to represent data (_we will use these ones_)
    * e.g. _JSON_, _YAML_, _XML_
    * __human-readable__, _easy to debug_, _easy to parse_, possibility to _manually_ edit the data
    * _verbose_, _inefficient_ (in terms of space)
    * may require tricks to represent _binary_ data (e.g. _escape sequences_, or _base64_ encoding)

2. __Binary__ formats: they rely on _bytes_ to represent data
    * e.g. _Protocol Buffers_, _Avro_
    * _compact_, _efficient_ (in terms of space)
    * _harder_ to debug, _harder_ to parse, _harder_ to manually edit the data (commonly require _hex editors_)
    * _natively_ support _binary_ data, but can represent _text_ as well


> But aren't _characters_ just _bytes_? Why do we need _different_ formats for _text_ and _binary_ data?

- In practice, engineers may prioritize human-readability if saving space is not a concern
    + e.g. on the Web

---

## Characters vs Bytes: Encoding

- Characters are __equivalent__ to bytes, according to an __encoding__ scheme
    * e.g. _ASCII_, _UTF-8_, _UTF-16_, _ISO-8859-1_, etc.

- _ASCII_ is the _oldest_ encoding scheme, where each character is represented by a _single_ byte (but only 7 bits are used)
    * e.g. `A` $\equiv$ `0x41`, `B` $\equiv$ `0x42`, ..., `a` $\equiv$ `0x61`, `b` $\equiv$ `0x62`, ...
    (this is what strings are represented in _C_ and _Python 2_)

- _Unicode_: an abstract way to represent information, coming with three different encoding schemes:
    - _UTF-8_ is the _most common_ encoding scheme, where each character is represented by _1 to 4_ bytes
        * e.g. `A` $\equiv$ `0x41`, `B` $\equiv$ `0x42`, ..., `à` $\equiv$ `0xC3A0`, `è` $\equiv$ `0xC3A8`, ...
        (this is what strings are represented in _Python 3_, and most modern programming languages)

    - _UTF-16_ is another common encoding scheme, where each character is represented by _2 or 4_ bytes
        * e.g. `A` $\equiv$ `0x0041`, `B` $\equiv$ `0x0042`, ..., `à` $\equiv$ `0x00E0`, `è` $\equiv$ `0x00E8`, ...

    - _UTF-32_ is another encoding scheme, where each character is represented by _4_ bytes
        * e.g. `A` $\equiv$ `0x00000041`, `B` $\equiv$ `0x00000042`, ..., `à` $\equiv$ `0x000000E0`, `è` $\equiv$ `0x000000E8`, ...

- _ISO-8859-1_ is another encoding scheme, where each character is represented by a _single_ byte
    * e.g. `A` $\equiv$ `0x41`, `B` $\equiv$ `0x42`, ..., `à` $\equiv$ `0xE0`, `è` $\equiv$ `0xE8`, ...

> _Notice_ that most of these encoding schemes are _compatible_ with _ASCII_ (i.e. the first 128 characters are the same)
> this is why inexperienced programmers _often_ don't _notice_ the difference between encodings

---

## Encoding in Python

- Python comes with the following _built-in_ types to represent sequences of characters and bytes:
    * `str` for _textual_ data (uses _UTF-8_ encoding in Python 3, _ASCII_ in Python 2), literals are of the from `"..."` or `'''...'''`
    * `bytes`for _binary_ data (similar to byte arrays in other languages), literals are of the form `b"..."` or `b'...'`

- Python also comes with functions to convert between _bytes_ and _strings_:
    * `str.encode(ENCODING)`: converts a string into a sequence of bytes using the specified `ENCODING`
    * `bytes.decode(ENCODING)`: converts a sequence of bytes into a string `ENCODING`
    * in both cases, `ENCODING` is a string representing the encoding scheme to use (e.g. `"utf-8"`, `"ascii"`, etc.)
    * if not specified, the default encoding is used (e.g. `import sys; sys.getdefaultencoding()`)

```python
s = "À l'école, l'élève étudiait l'histoire de la Révolution française et les événements marquants de l'été 1789."
b = s.encode('utf-8')

print(b) # b"\xc3\x80 l'\xc3\xa9cole, l'\xc3\xa9l\xc3\xa8ve \xc3\xa9tudiait l'histoire de la R\xc3\xa9volution fran\xc3\xa7aise et les \xc3\xa9v\xc3\xa9nements marquants de l'\xc3\xa9t\xc3\xa9 1789."
print(b.decode('utf-8')) # "À l'école, l'élève étudiait l'histoire de la Révolution française et les événements marquants de l'été 1789."

print(b.decode('ascii')) # UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 0: ordinal not in range(128)
```

---

## Escape sequences

- When using textual encodings, there maybe situations where some characters _cannot_ be _directly_ represented/inserted in a string
    * e.g. _control characters_ (e.g. `\n`, `\t`, `\r`, etc.)
    * e.g. _non-printable characters_ (e.g. `0x00`, `0x01`, etc.)

- Other than supporting encodings, most _programming_ or _data representation languages_ also support_
    * __escape sequences__ $\approx$ sub-sequences of characters that represent a _single_ character

- Most commonly:
    * there is an _escape character_ (commonly `\`) that _initiates_ the escape sequence
    * what can follow the escape character is _technology-dependent_, but most languages support the following:
        + `\n` $\equiv$ newline
        + `\t` $\equiv$ tab
        + `\r` $\equiv$ carriage return
        + `\\` $\equiv$ backslash (the single `\` is the escape character, so you need `\\` to represent a single `\`)
        + `\"` $\equiv$ double quote
        + `\'` $\equiv$ single quote
        + `\xHH` (or `\uHHHH`, or `\UHHHHHHHH`) $\equiv$ byte with hexadecimal value `HH` (or`HHHH`, or `HHHHHHHH`)

- Two relevant operations:
    * _escaping_: converting a _character string_ into another character string with _escape sequences_ for non-printable characters
    * _unescaping_: the other way around

---

## Escape sequences in Python

Function to _escape_ strings:

```python
def escape(s: str) -> str:
    return s.encode('unicode_escape').decode('ascii')
```

Function to _unescape_ strings:

```python
def unescape(s: str) -> str:
    return s.encode('ascii').decode('unicode_escape')
```

Usage example:

```python
s = """
value1 \ value2
value3 / value4
"""
print(escape(s)) # \nvalue1 \\ value2\nvalue3 / value4\n
print(s == escape(s)) # False
print(s == unescape(escape(s))) # True
```
---

## Data representation formats: JSON

- A `.json` file contains a __document__, i.e. a _characters_ string
    * encoding: _UTF-8_
- The file essentially a representation of a _tree-like_ data structure...
- ... where each _element_ is one of the following:
    * _value_ (e.g. _string_, _number_, _boolean_, _null_)
    * _object_ (i.e. dictionary) of _key-value_ pairs, where _keys_ are _strings_, and _values_ are _values_
    * _array_ (i.e. list) of _values_

### Example:

{{% multicol %}}
{{% col %}}
```json
{
    "name": "John Doe",
    "age": 42,
    "password": null,
    "is_student": false,
    "is_teacher": true,
    "stats": { "height": 1.83, "weight": 82.5 },
    "working_hours": [{"mon": 8}, {"tue": 7}, {"wed": 7}, {"thu": 8}, {"fri": 6}],
    "address": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip": "62701"
    }
}
```
{{% /col %}}
{{% col %}}
![](http://www.plantuml.com/plantuml/svg/JP51JyCm38Nl_HMHpzL4EzWcJZjm0S5fHuIcQ76RG9TKYQCAglntugxTbfFzFLllMTa7afw-WxF5M8ZymCepmhE0DwUjU748vONBbl5ZFRUz365mNcLcOzVDr8HZeAZGKkQDx0BU149vqkYpG3ukFDjJo6WKeD6qclUgrMvT2XYMVbUldaIQ5xBdZx7jKRleUV5pXBEpF9LACG95JhcTwW7LjIOThpEDDxdUfA_bCgKyXYd51EPW7f7TeQhNuaCQAmu4vMtWPEYNvKFlSvx6OAVkPJuCMNzzlyT_fcUugRSF5Kmu5QdOerNy1_y0)
{{% /col %}}
{{% /multicol %}}

---

## JSON parsing / generation in Python

- Python comes with the _built-in_ [module `json`](https://docs.python.org/3/library/json.html) to _parse_ and _generate_ JSON documents
    * `json.loads(s)`: parses a _string_ `s` representing a JSON document into a Python _object_
    * `json.dumps(o)`: generates a JSON document _string_ from a Python _object_ `o`

- Object to JSON conversion table
    * JSON _boolean_ $\leftrightarrow$ Python `bool`
    * JSON _number_ $\leftrightarrow$ Python `int` or `float`
    * JSON _string_ $\leftrightarrow$ Python `str`
    * JSON _array_ $\leftrightarrow$ Python `list`
    * JSON _object_ $\leftrightarrow$ Python `dict`
    * JSON _null_ $\leftrightarrow$ Python `None`

- Example of JSON parsing:

```python
doc: str = '{"name": "John Doe", "age": 42, "password": null, "is_student": false, "is_teacher": true, "stats": {"height": 1.83, "weight": 82.5}, "working_hours": [{"mon": 8}, {"tue": 7}, {"wed": 7}, {"thu": 8}, {"fri": 6}], "address": {"street": "123 Main St", "city": "Springfield", "state": "IL", "zip": "62701"}}'
obj: object = json.loads(doc)

print(type(obj)) # <class 'dict'>
print(type(obj['name']), obj['name']) # <class 'str'> John Doe
print(type(obj['age']), obj['age']) # <class 'int'> 42
print(type(obj['password']), obj['password']) # <class 'NoneType'> None
print(type(obj['is_student']), obj['is_student']) # <class 'bool'> False
print(type(obj['is_teacher']), obj['is_teacher']) # <class 'bool'> True
print(type(obj['stats']), obj['stats']) # <class 'dict'> {'height': 1.83, 'weight': 82.5}
print(type(obj['working_hours']), obj['working_hours']) # <class 'list'> [{'mon': 8}, {'tue': 7}, {'wed': 7}, {'thu': 8}, {'fri': 6}]

print(json.dumps(obj) == doc) # True
```

{{% /section %}}

---

{{% section %}}

# Running Example: Authentication Service

Part 1

---

## Modelling

Class diagram

Sequence diagram

---

## Implementation

Show example 0

{{% /section %}}

---

{{% section %}}

## (De)Serialization

Definition

---

## (De)Serialization in Python

Example

{{% /section %}}

---

{{% section %}}

## RPC

Definition

---

## Marshalling and Unmarshalling

Definition

---

## Request and Response Types in RPC

Class diagram

Sequence diagram

{{% /section %}}

---

{{% section %}}

# Running Example: Authentication Service

Part 2

---

## Modelling the presentation layer

Class diagram

---

## Implementing the presentation layer

Explicit type convention

Show example 1

{{% /section %}}

---

{{% section %}}

## Client and Server Stubs for the Authentication Service

Class diagram

Sequence diagram

Code examples

{{% /section %}}

---

{{% import path="reusable/back.md" %}}