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
    * both operations are __unavoidable__ in distributed systems programming

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

> __Problem__: most programming languages/platforms/OS use _different_ conventions for representing data
> <br> __Solution__: _agree_ on the data format to use for _communication_

__Corollary__: data interchange formats are an _essential_ aspect of every interaction pattern / protocol

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

- Other than supporting encodings, most _programming_ or _data representation languages_ also support
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

# Running Example: Authentication

(Part 1)

---

## How to support authentication

### Assuming a User Database exists...

1. letting users __create__ a _new account_
    - relevant data: _username_, _email addresses_, _full name_, _role_, _password_
        + only _hashed_ password are stored in-memory, [for security reasons](https://stytch.com/blog/what-is-password-hashing/)

2. letting users __get__ information about registered accounts (public information only) by _id_ (i.e., either username or some email)

3. letting users __test__ whether their _password_ is correct or not

### ... an Authentication Service can be implemented

1. letting users __generate__ an _authentication token_ by providing their _credentials_
    - __credentials__: _user id_ (username or email address) + _password_
    - __token__: a _document_ generated by the server, that the client can use to _prove_ its identity in _future_ interactions
        * composed by: _user data_, _expiration date_, _signature_
        * easy for the server to _verify_ the signature, but _hard_ for the client to _forge_
        * signature $\approx$ [Hash-based Message Authentication Code (HMAC)](https://en.wikipedia.org/wiki/HMAC)
2. letting users __test__ whether an _authentication token_ is _valid_ or not
    - __valid__: the token is _not expired_, and the _signature_ is _correct_


---

## Modelling (classes)

{{< plantuml height="50vh" >}}
package "users" {
    class User {
        +username: str
        +emails: set[str]
        +full_name: str
        +role: Role
        +password: str
        +ids: set[str]
    }

    class Credentials {
        +id: str
        +password: str
    }

    class Token {
        +user: User
        +expiration: datetime
        +signature: str
    }

    enum Role {
        ADMIN
        USER
    }

    interface UserDatabase {
        +add_user(user: User)
        +get_user(id: str) : User
        +check_password(credentials) : bool
    }

    interface AuthenticationService {
        +authenticate(credentials, duration) : Token
        +validate_token(token) : bool
    }

    package "impl" {
        class InMemoryUserDatabase {
            +__users: dict[str, User]
            +add_user(user: User)
            +get_user(id: str) : User
            +check_password(credentials) : bool
            +__get_user(id: str) : User
        }

        class InMemoryAuthenticationService {
            +__database: UserDatabase
            +__secret: str
            +authenticate(credentials, duration) : Token
            +validate_token(token) : bool
            +__validate_token_signature(token) : bool
        }

        InMemoryAuthenticationService *-l- InMemoryUserDatabase
    }

    UserDatabase <|.. InMemoryUserDatabase
    AuthenticationService <|.. InMemoryAuthenticationService
}
{{< /plantuml >}}

{{% multicol %}}
{{% col %}}
- Data classes in [`snippets.lab4.users`]({{< github-url repo="lab-snippets" path="snippets/lab4/users/__init__.py"  >}}):
    * `User`: represents an account
    * `Credentials`: an id—password pair
    * `Token`: represents an authentication token
    * `Role`: enumeration with admissible roles
{{% /col %}}
{{% col %}}
- Interfaces in [`snippets.lab4.users`]({{< github-url repo="lab-snippets" path="snippets/lab4/users/__init__.py"  >}}):
    * `UserDatabase`: interface for a user database
    * `AuthenticationService`: interface for an authentication service
- Implementation classes in [`snippets.lab4.users.impl`]({{< github-url repo="lab-snippets" path="snippets/lab4/users/impl.py"  >}}):
    * `InMemoryUserDatabase`: default implementation of user DB
    * `InMemoryAuthenticationService`: default implementation of authentication service
{{% /col %}}
{{% /multicol %}}

---

## Modelling (interaction)

![](https://www.plantuml.com/plantuml/svg/jLNRQXin47tNLynJyMBN7s3OaE8QMkW5ahHzQCeoMKrjaLt9wEAcVr-j54-sD5uKaZxPp4XdvfmvEpft7gqFVITsIXByDCRVc3iXiFN6mXT7LWY97c_G4RpN7watzlSGVdiV5FjuNxLgZzhpWJV1xqZ7C7fbz2NPWsf9YBg6jQKOqzi43NKjHFhp-knHy1MWb4s8aLceXfxK0Vs9FXuBdiPj4ghx7fR3hyQUVa0D0QxrjHybgKVLvSp90aaaIPFT9UuNXF89rBVaCtKbNvPxIFMFB9UnJYennMy5bdom6a8fsVMEsjl8TfYu7Bo0dIiWtGxNcZqwzyjOEMij_NVogSYI5IX6KguvOATaH7it6z2MnxQh2keOJC0SB1EOKOj4_c2sIiFiojoIll-qZ1wA2zPv-fjS0Jw4AJRCirg033RZiVxJM68oMppoKG_FcFm4vQShZPtdqvCi2whpSacEKJ8jb_WtRnwwswkiUWn_-lmDvZo6VC2fhSROFh7hO3w-DOVBpVfYSrLDzlclxPA54jvY1BTug5S9wXo1DkLIS0bKyUPNx09jh3LMa1wBNl1g_9LXmqT49TdonOu_v6lK-CJPluo_2mgF5ePFpmw_FQ3qqHTvpA_YYT5Kpv8NECD3oMicWy4yPfxl1EwoV4Bdf6Nekpy0)

(open in another tab to zoom in)

---

## Exemplify implementation

(cf. <{{< github-url repo="lab-snippets" path="snippets/lab4/example0_users.py"  >}}>)

{{< code path="content/presentation/example0_users.py" >}}
- run with `python -m snippets -l 4 -e 0`
    * analyse the logs to understand what's going on

---

## What's next?

In the remainder of this lecture, we will focus on making the _user database_ and _authentication service_ __distributed__:
1. clients will be able to _register_ and _authenticate_ themselves _remotely_, via __RPC__
2. we will use __JSON__ as the _data interchange format_ for _RPC_ and _(de)serialization_
3. notice that many different sorts of _data_ may be exchanged between _clients_ and _servers_
    + e.g. _user data_, _credentials_, _authentication tokens_, etc.,
    + but also, indirectly: _strings_, _dates_, _roles_, etc.
    + potentially, also _error messages_?
4. let's proceed step by step

{{% /section %}}

---

{{% section %}}

## (De)Serialization

- __Serialization__ $\equiv$ converting _in-memory_ __objects__ into __char__/_byte_ __sequences__, according to some _data interchange format_
- __Deserialization__ $\equiv$ converting __char__/_byte_ __sequences__ back into _in-memory_ __objects__, according to the _same_ data interchange format

{{% multicol %}}
{{% col class="col-5" %}}
```python
from snippets.lab4.users import User, Role

User(
    username='gciatto',
    emails={
        'giovanni.ciatto@unibo.it',
        'giovanni.ciatto@gmail.com'
    },
    full_name='Giovanni Ciatto',
    role=Role.ADMIN,
    password='my secret password',
)
```
{{% /col %}}
{{% col class="col-2" %}}
$\xrightarrow{\text{serialization}}$

$\xleftarrow{\text{deserialization}}$
{{% /col %}}
{{% col class="col-5" %}}
```json
{
    "username": "gciatto",
    "emails": [
        "giovanni.ciatto@unibo.it",
        "giovanni.ciatto@gmail.com"
    ],
    "full_name": "Giovanni Ciatto",
    "role": {"name": "ADMIN"},
    "password": "my secret password",
}
```
{{% /col %}}
{{% /multicol %}}

- One key part in any distributed system _design_ / implementation is how to about _supporting_ __(de)serialization__:
    * _what_ data should be (de)serialized?
    * how exactly should it be (de)serialized?
        - which _data interchange format_ should be used?
        - which _fields_ should be serialized? which ones could be _omitted_?
        - how to deal with _circular references_?

- Engineers will commonly design/implement __(de)serializers__:
    * i.e. _objects_ aimed at _performing_ (de)serialization...
    * ... for _all_ relevant _data types_ in the system
        + and the other _data types_ they depend on
        + there including relevant _built-in_ types from the _programming language_ used (e.g. `datetime`, `set`, etc.)

---

## (De)Serialization in Practice

- _Serialisation_ usually involves the construction of an __Abstract Syntax Tree__ (AST) from the _in-memory_ object
    * the AST is then _converted_ into a _char_/_byte_ sequence

- _Deserialisation_ usually involves the _opposite_ process:
    * the _char_/_byte_ sequence is then _converted back_ into an AST
    * the AST is then _converted back_ into an _in-memory_ object

{{% multicol %}}
{{% col class="col-4" %}}
```python
# Python object

User(
  username='gciatto',
  emails={
    'giovanni.ciatto@unibo.it',
    'giovanni.ciatto@gmail.com'
  },
  full_name='Giovanni Ciatto',
  role=Role.ADMIN,
  password='my secret password',
)
```
{{% /col %}}
{{% col class="col-4" %}}
```python
# Python dict (AST)

dict(
  username='gciatto',
  emails=[
    'giovanni.ciatto@unibo.it',
    'giovanni.ciatto@gmail.com',
  ],
  full_name='Giovanni Ciatto',
  role=dict(name='ADMIN'),
  password='my secret password',
)
```
{{% /col %}}
{{% col class="col-4" %}}
```json
// JSON document

{
  "username": "gciatto",
  "emails": [
    "giovanni.ciatto@unibo.it",
    "giovanni.ciatto@gmail.com"
  ],
  "full_name": "Giovanni Ciatto",
  "role": {"name": "ADMIN"},
  "password": "my secret password",
}
```
{{% /col %}}
{{% /multicol %}}

- Many (de)serialization _libraries_ exist for most common programming languages and data interchange formats
    * e.g. in Python: [`json`](https://docs.python.org/3/library/json.html), [`pickle`](https://docs.python.org/3/library/pickle.html), [`marshmallow`](https://marshmallow.readthedocs.io/en/stable/), [`PyYaml`](https://pypi.org/project/PyYAML/), etc.
- They commonly provide for free:
    * serialization of AST into _char_/_byte_ sequences
    * deserialization of _char_/_byte_ sequences into AST
    * sometimes, AST $\leftrightarrow$ built-in data type conversions
- Users __must__ _define_ AST $\leftrightarrow$ custom data type conversion for all _relevant_ data types in their systems

---

## Serialization in Python (attempt 1)

{{% multicol %}}
{{% col class="col-5" %}}
```python
from snippets.lab4.users import User, Role

to_serialize = User(
  username='gciatto',
  emails={
    'giovanni.ciatto@unibo.it',
    'giovanni.ciatto@gmail.com'
  },
  full_name='Giovanni Ciatto',
  role=Role.ADMIN,
  password='my secret password',
)
```
{{% /col %}}
{{% col class="col-2" %}}
$\xrightarrow{\text{serialization}}$
{{% /col %}}
{{% col class="col-5" %}}
```json
{
  "username": "gciatto",
  "emails": [
    "giovanni.ciatto@unibo.it",
    "giovanni.ciatto@gmail.com"
  ],
  "full_name": "Giovanni Ciatto",
  "role": {"name": "ADMIN"},
  "password": "my secret password",
}
```
{{% /col %}}
{{% /multicol %}}

Let's implement a serializer:

{{% multicol %}}
{{% col class="col-8" %}}
```python
class Serializer:
    def serialize(self, obj: object) -> str:
        return self._ast_to_string(self._to_ast(obj)) # objct -> AST -> JSON string

    def _ast_to_string(self, data):
        return json.dumps(data, indent=2) # AST -> JSON string

    # here we select which conversion to apply based on the type of obj
    def _to_ast(self, obj: object) -> object:
        if isinstance(obj, User):
            return self._user_to_ast(obj)
        elif isinstance(obj, Role):
            return self._role_to_ast(obj)
        else:
            raise ValueError(f'unsupported type: {type(obj)}')

    def _user_to_ast(self, user: User) -> dict: # User -> AST
        return {
            'username': user.username,
            'emails': list(user.emails),
            'full_name': user.full_name,
            'role': self._role_to_ast(user.role),
            'password': user.password,
        }

    def _role_to_ast(self, role: Role) -> dict: # Role -> AST
        return {'name': role.name}
```
{{% /col %}}
{{% col %}}
{{< plantuml >}}
class Serializer {
    +serialize(obj: object) : str
    -_ast_to_string(data) : str
    -_to_ast(obj: object) : object
    -_user_to_ast(user: User) : dict
    -_role_to_ast(role: Role) : dict
}
{{< /plantuml >}}
{{% /col %}}
{{% /multicol %}}

```python
serializer = Serializer()
print(serializer.serialize(to_serialize)) # prints the JSON document
```

---

## Deserialization in Python (attempt 1)

{{% multicol %}}
{{% col class="col-5" %}}
```python
to_deserialize = """{
  "username": "gciatto",
  "emails": [
    "giovanni.ciatto@unibo.it",
    "giovanni.ciatto@gmail.com"
  ],
  "full_name": "Giovanni Ciatto",
  "role": {"name": "ADMIN"},
  "password": "my secret password",
}"""
```
{{% /col %}}
{{% col class="col-2" %}}
$\xrightarrow{\text{deserialization}}$
{{% /col %}}
{{% col class="col-5" %}}
```python
from snippets.lab4.users import User, Role

result = User(
  username='gciatto',
  emails={
    'giovanni.ciatto@unibo.it',
    'giovanni.ciatto@gmail.com'
  },
  full_name='Giovanni Ciatto',
  role=Role.ADMIN,
  password='my secret password',
)
```
{{% /col %}}
{{% /multicol %}}

{{% multicol %}}
{{% col class="col-8" %}}
```python
class Deserializer:
    def deserialize(self, string):
        return self._ast_to_obj(self._string_to_ast(string)) # JSON string -> AST -> object

    def _string_to_ast(self, string):
        return json.loads(string)  # JSON string -> AST

    # here we select which conversion to apply based which keys are present in the AST
    def _ast_to_obj(self, data) -> object:
        if all(k in data for k in ['username', 'emails', 'full_name', 'role', 'password']):
            return self._user_from_ast(data)
        elif 'name' in data:
            return self._role_from_ast(data)
        else:
            raise ValueError(f'unsupported data: {data}')

    def _user_from_ast(self, data) -> User: # AST -> User
        return User(
            username=data['username'],
            emails=set(data['emails']),
            full_name=data['full_name'],
            role=self._ast_to_obj(data['role']), # recursive call!
            password=data['password'],
        )

    def _role_from_ast(self, data) -> Role: # AST -> Role
        return Role[data['name']]
```
{{% /col %}}
{{% col %}}
{{< plantuml >}}
class Deserializer {
    + deserialize(string) : object
    - _string_to_ast(string) : object
    - _ast_to_obj(data) : object
    - _user_from_ast(data) : User
    - _role_from_ast(data) : Role
}
{{< /plantuml >}}
{{% /col %}}
{{% /multicol %}}

```python
deserializer = Deserializer()
print(deserializer.deserialize(to_deserialize) == result) # prints True
```

---

## Analysis of the current approach

- __Pros__:
    * one method per _data type_ to (de)serialize
    * _automatically_ understands _how_ to (de)serilize the provided object/string
    * raises error on attempt to (de)serialize an _unsupported_ data type
    * raises error on attempt to (de)serialize _invalid_ data (e.g. missing fields)
    * _easy_ to _extend_ to support _new_ data types
        1. requires adding _one more_ method to the `Serializer` and `Deserializer` for the _new_ data type
        2. requires _modifying_ the `_to_ast` and `_ast_to_obj` methods to _select_ the _new_ method

- __Cons__:
    * quite _verbose_ and _repetitive_
    * the _type_ of the _object_ to *de*serialize is __inferred__ from the _keys_ present in the _AST_
        + this may lead to _ambiguities_ if _different_ data types _share_ the _same_ _keys_
            * e.g. what if _another_ data type has a `name` key (other than `Role`)?
        + this may lead to _errors_ if _some_ _keys_ are _missing_ in the _AST_

---

## (De)Serialization in Python (attempt 2)

__Improvement__: _explicitly_ _tag_ the _type_ of the object to _serialize_ in the _AST_, and use this tag to _select_ the right method to _**de**serialize_

{{% multicol %}}
{{% col class="col-5" %}}
```python
from snippets.lab4.users import User, Role

User(
    username='gciatto',
    emails={
        'giovanni.ciatto@unibo.it',
        'giovanni.ciatto@gmail.com'
    },
    full_name='Giovanni Ciatto',
    role=Role.ADMIN,
    password='my secret password',
)
```
{{% /col %}}
{{% col class="col-2" %}}
$\xrightarrow{\text{serialization}}$

$\xleftarrow{\text{deserialization}}$
{{% /col %}}
{{% col class="col-5" %}}
```json
{
    "username": "gciatto",
    "emails": [
        "giovanni.ciatto@unibo.it",
        "giovanni.ciatto@gmail.com"
    ],
    "full_name": "Giovanni Ciatto",
    "role": {
        "name": "ADMIN",
        "$type": "Role" // explicit type field
    },
    "password": "my secret password",
    "$type": "User" // explicit type field
}
```
{{% /col %}}
{{% /multicol %}}

Apply these updates to the `Serializer` and `Deserializer` classes:

{{% multicol %}}
{{% col %}}
```python
class Serializer:
    # rest of the class unchanged

    def _to_ast(self, obj: object) -> object:
        if isinstance(obj, User):
            result = self._user_to_ast(obj)
        elif isinstance(obj, Role):
            result = self._role_to_ast(obj)
        else:
            raise ValueError(f'unsupported type: {type(obj)}')
        result['$type'] = type(obj).__name__
        return result
```
{{% /col %}}
{{% col %}}
```python
class Deserializer:
    # rest of the class unchanged

    def _ast_to_obj(self, data) -> object:
        if data['$type'] == type(User).__name__:
            return self._user_from_ast(data)
        elif data['$type'] == type(Role).__name__:
            return self._role_from_ast(data)
        else:
            raise ValueError(f'unsupported data: {data}')
```
{{% /col %}}
{{% /multicol %}}

- Let's use `$type` as the type tag _key_:
    + the _dollar_ is just a character that is _unlikely_ to be used in _real_ data to minimize the risk of _collisions_
        * (but any other unlikely character would work as well)

---

## De(Serialization) in Python (full example)

1. See the example at <{{< github-url repo="lab-snippets" path="snippets/lab4/example1_presentation.py"  >}}>

{{% multicol %}}
{{% col class="col-10" %}}
2. Notice the two new classes: `Request` and `Response`
    <!-- - `Request`: represents an RPC request to the server
        + `name`: the name of the function to call
        + `args`: the arguments to pass to the function
    - `Response`: represents an RPC response from the server
        + `result`: the result of the function call
        + `error`: an error message in case of failure -->

3. Notice how complex the `Serializer` and `Deserializer` classes may become in a real usecase

4. Try to figure out how the following object...
    ```python
    from snippets.lab4.example0_users import gc_credentials_wrong

    request = Request(
        name='my_function',
        args=(
            gc_credentials_wrong, # an instance of Credentials
            gc_user, # an instance of User
            ["a string", 42, 3.14, True, False], # a list, containing various primitive types
            {'key': 'value'}, # a dictionary
            Response(None, 'an error'), # a Response, which contains a None field
        )
    )
    ```

5. ... would be serialized as the following JSON
    ```json
    {
    "name": "my_function",
    "args": [
        { "id": "giovanni.ciatto@unibo.it", "password": "wrong password", "$type": "Credentials"},
        "user": {
            "username": "gciatto",
            "emails": ["giovanni.ciatto@gmail.com", "giovanni.ciatto@unibo.it"],
            "full_name": "Giovanni Ciatto",
            "role": { "name": "ADMIN", "$type": "Role" },
            "password": null,
            "$type": "User"
        },
        ["a string", 42, 3.14, true, false],
        { "key": "value"},
        { "result": null, "error": "an error", "$type": "Response"}
    ],
    "$type": "Request"
    }
    ```

{{% /col %}}
{{% col class="col-2" %}}
{{< plantuml >}}

class Request {
    + name: str
    + args: tuple
}

Request -d[hidden]- Response

class Response {
    + result: object
    + error: str
}
{{< /plantuml >}}

6. Run with `python -m snippets -l 4 -e 1`

{{% /col %}}
{{% /multicol %}}

{{% /section %}}

---

{{% section %}}

## Remote Procedure Call (RPC)

> __RPC__ $\equiv$ a _request—response_ interaction pattern between a _client_ and a _server_ where:
> the client aims at _invoking_ a _procedure_ on the server, and receiving the _result_ of the procedure back
> as if the procedure was _locally_ executed, despite the _server_ being _remote_

- (Remote) __Procedure__ $\equiv$ a _function_ with a clear _signature_, _offered_ by a _server_, to be _invoked_ by a _client_
    * _name_ (or _identifier_)
    * _input_ parameters
    * _returns_ value(s), there including _errors_ that may or may not be _raised_ during the _execution_
    * _side effects_ (if any) which may change the _state_ of the _server_, hence affecting the result of _future_ calls

- Differences w.r.t. _local_ procedure calls:
    1. caller and callee are _not_ in the _same_ _address space_ $\Rightarrow$ can*not* pass arguments _by reference_
        * passage _by value_ is the only option: _copies_ of arguments must be transferred over the network
    2. input parameters and return values must be _serialized_ and _deserialized_ to pass through the _network_
    3. _exceptions_ do not really exist, ad-hoc _return values_ are used instead

---

## RPC Client and Server

<br>

{{< image src="./rpc-time.png" >}}

- The _client_ and the _server_ are __temporally coupled__
    * the _client_ must __wait__ for the _server_ to _respond_
    * the _server_ must __wait__ for the _client_ to _send_ the _request_
    * they must be _online_ at the __same time__
    * the _server_ must be _online_ __before__ the _client_

---

## Common RPC Infrastructure

{{< image src="./rpc-dataflow1.png" height="40vh" >}}

- __protocol__: the low level _transfer_ protocol (e.g. _HTTP_, _TCP_, _UDP_, etc.) + _data representation format_ (e.g. _JSON_, _XML_, _binary_, etc.)
- __client stub__: a _proxy_ object that __mimics__ the _server_ _interface_ on the _client_ side
- __client__: the piece of code which is using the _client stub_
    + it may not even be aware of the fact that the _server_ is _remote_
- __server stub__: a _server_ which listens for requests, handles them (possibly concurrently) and sends back responses
    + it commonly acts as a _proxy_ towards some actual _server_ code
- __server__: the piece of code which is _executing_ the _actual procedure_ on the _server_ side
    + it may not even be aware of the fact that the _client_ is _remote_
    + _beware_! In this case "server" means _"provider of a functionality"_: the infrastructural component is actually the "server stub"!

---

## Marshalling and Unmarshalling

The client and server _stubs_ are essentially aimed at performing these operations:

{{< image src="./rpc-dataflow2.svg" height="50vh" >}}

- __Marshalling__: the process of _serializing_ the arguments/results of a RPC to send them over the network
- __Unmarshalling__: the process of _deserializing_ the arguments/results of a RPC received from the network

---

## Request and Response Types in RPC

To support RPC, implementation will most commonly define two data structures:
- `Request`: a data structure representing the _invokation request_ to be sent to the _server_
    * it will contain the _name_ of the _procedure_ to be _invoked_, and the _arguments_ to be passed to it, etc.
- `Response`: a data structure representing the _response_ to be sent back to the _client_
    * it will contain the _result_ of the _procedure_ (if any), and the _error_ message (if any), etc.

{{% multicol %}}
{{% col class="col-3" %}}
{{< plantuml height="60vh" >}}
class Request {
    + name: str
    + args: tuple
}

Request -d[hidden]- Response

class Response {
    + result: object
    + error: str
}
{{< /plantuml >}}
{{% /col %}}
{{% col %}}
{{< plantuml height="60vh" >}}
@startuml
hide footbox

actor Client
participant "Client Stub" as CS
control "Server Stub" as SS
participant Server

Client -> CS: f(a, b, c)
activate Client
activate CS
CS -> CS: req = Request(name='f', args=(a, b, c)) \n req = serialize(req)
CS -> SS: {"name"="function", "args"=[a, b, c]}
activate SS
SS -> SS : req = deserialize(req)
SS -> SS : lookup function req.name
SS -> Server: f(a, b, c)
activate Server

alt success
Server --> SS: return R
else exception
Server --> SS: raise E
deactivate Server
end
SS -> SS: res = Response(result=R, error=E) \n res = serialize(res)
SS -> CS: {"result": R, "error": E}
deactivate SS
CS -> CS: res = deserialize(res)

alt res.error is None
CS --> Client: return res.result
else
CS --> Client: raise res.error
deactivate CS
end
@enduml
{{< /plantuml >}}
{{% /col %}}
{{% /multicol %}}

{{% /section %}}

---

{{% section %}}

# Running Example: Authentication

(Part 2)

---

## Server Stubs for the User Database

- The "actual" server (provider of functionality) here is some instance of the `InMemoryUserDatabase` class
- We will exemplify how to build a _server stub_ for that server
    * it will leverage on _TCP sockets_ to listen for incoming requests, hence reusing [the `Server` interface from the previous lecture](../communication/#/utilities)

### Design considerations
1. assume each TCP connection is devoted to a _single_ RPC, i.e. just one _request_ and one _response_
2. serve RPCs _concurrently_, by starting a new _thread_ for each incoming connection
3. use the `Serializer` and `Deserializer` classes to (de)serialize _requests_ and _responses_
4. the server stub holds a reference to the _actual_ server, and _delegates_ the _actual_ work to it
    - upon receiving a _request_, it _deserializes_ it, _invokes_ the _actual_ server, _serializes_ the _response_, and _sends_ it back to the _client_
    - if any _error_ occurs, it _serializes_ the _error_ message and _sends_ it back to the _client_

{{< code path="content/presentation/example2_rpc_server.py" >}}

(see code in [`snippets.lab4.example2_rpc_server`]({{< github-url repo="lab-snippets" path="snippets/lab4/example2_rpc_server.py" >}}), run with `python -m snippets -l 4 -e 2`)

---

## Client Stubs for the Authentication Service

- We will exemplify how to build a _client stub_ for the _user database_
    * it will leverage on _TCP sockets_ to send requests to the server, hence reusing [the `Client` interface from the previous lecture](../communication/#/utilities)
- We create a general-purpose _abstract_ class `ClientStub` to be _extended_ by _specific_ client stubs
    * for the user database, we create the `RemoteUserDatabase` class which inherits from `ClientStub` and implements the `UserDatabase` interface
    * this is to make the _RPC-based_ implementation of the user database have the __same interface__ of the in-memory implementation

### Design considerations
1. the `ClientStub` class comes with method `rpc(name, *args)` to issue an RPC to the server
    + the server address and port are passed to the _constructor_, as they are not supposed to change during the lifetime of the client stub
2. the `RemoteUserDatabase` class implements the `UserDatabase` interface by _delegating_ the _actual_ work to the `rpc` method

{{< code path="content/presentation/example3_rpc_client.py" >}}

---

## Exemplify Programming with RPC Client and Server

1. Start the server with `python -m snippets -l 4 -e 2 PORT`
    - where `PORT` is the port number the server will listen to, e.g. `8080`
    - recall to _restart_ the server too if you want to _restart_ the client

2. Run the following Python script (cf. [`snippets.lab4.example3_rpc_client` module]({{< github-url repo="lab-snippets" path="snippets/lab4/example3_rpc_client.py" >}}))
    {{< code path="content/presentation/example3_rpc_client-main.py" >}}
    - launch it with `python -m snippets -l 4 -e 3 SERVER_IP:PORT`
        + where `SERVER_IP` (e.g. `localhost`) is the IP address of the server...
        + ... and `PORT` is the port number the server is listening to (e.g. `8080`)
    - this should succeed with no errors _the first time_
        + it will _fail_ if you run it _one more time_ without restarting the server! __why__?

3. Look at the logs of the client and the server to understand what's going on

---

## Exemplify Command-Line User Database Client

1. (Re)Start the server with `python -m snippets -l 4 -e 2 PORT`
    - where `PORT` is the port number the server will listen to, e.g. `8080`
    - recall to _restart_ the server too if you want to _restart_ the client

2. Play with the Python module [`snippets.lab4.example4_rpc_client_cli`]({{< github-url repo="lab-snippets" path="snippets/lab4/example4_rpc_client_cli.py" >}})
    ```text
    usage: python -m snippets -l 4 -e 4 [-h] [--user USER] [--email EMAIL [EMAIL ...]] [--name NAME] [--role {admin,user}] [--password PASSWORD]
                                        address {add,get,check}

    RPC client for user database

    positional arguments:
    address               Server address in the form ip:port
    {add,get,check}       Method to call

    options:
    -h, --help            show this help message and exit
    --user USER, -u USER  Username
    --email EMAIL [EMAIL ...], --address EMAIL [EMAIL ...], -a EMAIL [EMAIL ...]
                            Email address
    --name NAME, -n NAME  Full name
    --role {admin,user}, -r {admin,user}
                            Role (defaults to "user")
    --password PASSWORD, -p PASSWORD
                            Password
    ```

3. Consider the following sequence of commands:
    ```bash
    python -m snippets -l 4 -e 4 SERVER_IP:PORT get -u gciatto
        # [RuntimeError] User with ID gciatto not found
    python -m snippets -l 4 -e 4 SERVER_IP:PORT add -u gciatto -a giovanni.ciatto@unibo.it giovanni.ciatto@gmail.com -n "Giovanni Ciatto" -r admin -p "my secret password"
        # None
    python -m snippets -l 4 -e 4 SERVER_IP:PORT get -u gciatto
        # User(username='gciatto', emails={'giovanni.ciatto@unibo.it', 'giovanni.ciatto@gmail.com'}, full_name='Giovanni Ciatto', role=<Role.ADMIN: 1>, password=None)
    python -m snippets -l 4 -e 4 SERVER_IP:PORT check -u gciatto -p "my secret password"
        # True
    python -m snippets -l 4 -e 4 SERVER_IP:PORT check -u gciatto -p "wrong password"
        # False
    ```

{{% /section %}}

---

{{< slide id="exercise-rpc-auth-service" >}}

## Exercise: RPC-based Authentication Service

- __Prerequisites__:
    1. understand the _(de)serialization_ we have just exemplified
    1. understand the _RPC_ infrastructure we have just exemplified

- __Goal__: extend the exemplified _RPC_ infrastructure to support an _authentication service_
    * the server stub should _delegate_ the _actual_ work to an _actual_ `InMemoryAuthenticationService` instance
    * one more client stub should be created to for the `AuthenticationService` interface
    * the command-line interface of the client should be extended accordingly

- __Hints__: you must reuse the provided code, modifying it: no need to create further Python files

- __Deadline__: December 31st, 2025

- __Incentive__: +1 point on the final grade (if solution is satisfying)

- __Submission__:
    1. fork the [`lab-snippets` repository]({{< github-url repo="lab-snippets" >}})
    2. create a new branch named `exercise-lab4`
    3. commit your solution in the `snippets/lab4` directory
    4. push the branch to your fork & create a __pull request__ to the original repository, entitled `[{{<academic_year>}} Surname, Name] Exercise: RPC Auth Service`
        - in the pull request, describe your solution, motivate your choices, and explain how to test it

---

{{< slide id="exercise-rpc-auth-service-secure" >}}

## Exercise: Secure RPC-based Authentication Service

- __Prerequisites__: complete previous exercise

- __Goal__: extend the exemplified _RPC_ infrastructure to support __authorization__
    + _reading_ registered user data should _only_ be possible for _authenticated_ users whose _role_ is __admin__
    + any attempt do so by _unauthorized_ or _unauthenticated_ users should result in an _error_ being returned
    + the command-line interface of the client should be extended accordingly

- __Hints__:
    * the `Request` class should be extended to include an optional _metadata_ field
        + when the _client_ performs an operation which __requires__ _authentication_...
        + ... the _metadata_ field should be _filled_ with the _token_ of the _user_
    * the `ServerStub` should be extended to check for the presence and validity of the _token_ in the _metadata_ field
    * the client should be extended to memorize the _token_ upon successful _authentication_ and _pass_ it in the _metadata_ field of any _subsequent_ request

- __Deadline__: December 31st, 2025

- __Incentive__: +1 point on the final grade (if solution is satisfying)

- __Submission__:
    1. fork the [`lab-snippets` repository]({{< github-url repo="lab-snippets" >}})
    2. create a new branch named `exercise-lab4`
    3. commit your solution in the `snippets/lab4` directory
    4. push the branch to your fork & create a __pull request__ to the original repository, entitled `[{{<academic_year>}} Surname, Name] Exercise: RPC Auth Service 2`
        - or just reuse the pull request and branch of the previous exercise, if you already submitted it
        - in the pull request, describe your solution, motivate your choices, and explain how to test it

---

{{% import path="reusable/back.md" %}}