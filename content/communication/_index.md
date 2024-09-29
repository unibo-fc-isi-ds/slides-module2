+++

title = "[DS] Communication Mechanisms"
description = "Communication Mechanisms for Distributed Systems"
outputs = ["Reveal"]
aliases = [
    "/communication/",
    "/sockets/"
]

+++

# Communication Mechanisms for Distributed Systems

{{% import path="reusable/footer.md" %}}

---

## Context

- Distributes systems requires distributed nodes to _communicate_ over the _network_

- So far, we described communication as _"sending messages"_ between nodes...

- ... but how exactly do we _send_ and _receive_ messages?

- Okay, we know from our _networking_ course that __network protocols__ are the answer...
    + e.g. [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) and [UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)

- But how do we __use__ these protocols in our programs, _in practice_?

---

## Sockets

- Most OS support the [Berkeley **sockets**](https://en.wikipedia.org/wiki/Berkeley_sockets) API...

- ... and virtually all programming languages provide a _wrapper_ around this API
    + there including Python, via the [`socket` module](https://docs.python.org/3/library/socket.html)

- Sockets are:
    * an _ancient_, and _stable_ __API__ for low-level networking in TCP/UDP (and more)
    * very _didactic_: they require a good understanding of DS fundamentals
        + e.g. client/server, or local/remote dichotomies
    + very _elementary_: higher-level communication abstractions can be built on top of them
        + e.g. RPC, _HTTP_, and virtually any application-level protocol

---

## Definition

> A __socket__ is an abstract representation for the _local_ endpoint of a network communication path.

{{< image src="./sockets.svg" height="50vh" alt="Concept of a socket" >}}

### Interpretation

A _process_’s gateway towards the network, providing a __full-duplex__,
__multiplexable__, _point-to-point_ or _point-to-*multi*-point_ __communication__ means towards other
processes, _distributed_ over the network

(see next slide)

---

- __distributed processes__: sockets aims at letting processes communicate, so
    * multiple processes on the same machine may communicate via sockets too
    * the same socket on the same machine may be shared among threads

- __communication__: information exchange is explicit
    * data is _sent/received_ via ad-hoc socket methods

- __point-to-point__: each socket mediates the interaction among _two (and only two)_ processes
    * as opposed to __point-to-*multi*point__ communication, a socket may communicate with multiple other processes

- __multiplexable__: multiple independent sockets may be created, on different ports
    * ports are positive 2-bytes integers in the range from $1$ to $2^{16} - 1$,
    * the $1\ldots1023$ range is reserved for well-known protocols
    * ports in the rage $1024\ldots2^{16} - 1$ are for custom usage

- __full-duplex__: exchanged data may flow in both verses, simultaneously
    * i.e. the receiver may send data while receiving
    * i.e. the sender may receive data while sending

---

## Two types of sockets

- __stream sockets__ allowing the exchange of possibly unlimited _streams_ of bytes
    + commonly based on TCP
    + commonly operating in a _connection_-oriented way

- __datagram sockets__ allowing the exchange of finite-sized _packets_ of bytes
    + commonly based on UDP
    + commonly operating in a _connectionless_ way

- both packets and streams are _byte-oriented_ communication means
    + i.e. the _unit_ of communication is the _byte_

- sockets do not care about the _content_ of the exchanged data
    + i.e. it is up to the _application_ to interpret the bytes

---

## Some jargon

- Client vs. Server
    + _client_ socket: the socket initiating the communication
    + _server_ socket: the socket accepting the communication

- Local vs. Remote
    + _local_ socket: the socket on the _local_ machine
    + _remote_ socket: the socket on the _remote_ machine
    + in the eyes of the _client_ socket, the server socket is _remote_, and vice-versa

- Address and Port
    + the _address_ is the IP address of the machine
        * recall that a machine may have _multiple_ IP addresses, one per _network interface_
    + the _port_ is the port number of the socket
    + the _address:port_ pair is the _endpoint_ of the communication path

---

{{% section %}}

## Datagram sockets

{{< image src="./udp-sockets.svg" alt="Datagram sockets representation" height="50vh" >}}

- Datagram sockets aim at exchanging _packets_ of bytes, called _datagrams_, among _endpoints_
    + __datagram__ $\approx$ self-contained packet of a given size
        * in __UDP__ the upper-bound is _64 KiB_, i.e. $(2^{16} - 1)$ bytes of _maximum datagram size_
- __No__ _connection_ is established between the endpoints
    + each datagram send/receive is _independent_ from the others
- There is no difference among client and server sockets
    + each datagram socket may act as a _client_ or a _server_ in any moment
- Each datagram is _self-contained_ can be used to communicate with __many__ other sockets
    + the _address:port_ pair is specified upon sending _each_ datagram
    + $\Rightarrow$ support for _broadcast_ and _multicast_ communication

---

### Datagram sockets in Python (pt. 1)

1. Python provides a `socket` _module_, with a `socket` _class_
    + use the _constructor_ to create a new socket
    + the `socket` class provides methods for _sending_ and _receiving_ datagrams

2. Example of socket _creation_:
    ```python
    import socket

    # create a new datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ```
    + `AF_INET` specifies the _address family_ (IPv4)
    + `SOCK_DGRAM` specifies the _socket type_ (datagram)

3. _Before_ being used, the socket must be _bound_ to a local _address_ and _port_ (in order to _receive_ datagrams)
    ```python
    # bind the socket to the local address and port
    sock.bind(('W.X.Y.Z', 12345))
    ```
    + __binding__ $\approx$ associating the socket to a local address and port, so that the OS knows where to deliver incoming datagrams
    + class `socket` provides the `bind` method which accept a _single_ argument, which must be a _tuple of two_ elements, represening one _endpoint_
        * the $1^{st}$ element is the _address string_ (use `'0.0.0.0'` to bind to _all_ local addresses)
        * the $2^{nd}$ element is the _port number_ (use `0` to let the OS choose a free port)

---

### Datagram sockets in Python (pt. 2)

<!-- (let us assume that a costant has been defined as follows:)
```python
THRESHOLD_DGRAM_SIZE = 65536
``` -->


{{% multicol %}}
{{% col class="col-6" %}}
4. Example of datagram __send__:
    ```python
    payload = 'Hello, world!'
    recipient = ('A.B.C.D', 54321)
    sock.sendto(payload.encode(), recipient)
    ```
    + `sendto` method sends a _datagram_ to a _remote recipient_
    + the $1^{st}$ argument is the _byte sequence_ to be sent
    + the $2^{nd}$ argument is the recipient endpoint (as a _tuple_)
    + documentation: [socket.sendto](https://docs.python.org/3/library/socket.html#socket.socket.sendto) 
{{% /col %}}
{{% col %}}
5. Example of datagram __receive__
    ```python
    data, sender = sock.recvfrom(bufsize=4096)
    data = data.decode()
    print(f'Received: "{data}" from "{sender}"')
    ```
    + `recvfrom` method receives a _datagram_ from a _remote sender_
    + the $1^{st}$ is the _buffer size_, according to doc: _"a relatively small power of 2"_, e.g. 4096
    + the method returns a _tuple_ with the _received data_ and the _sender endpoint_
        * the _received data_ is a _byte sequence_
    + documentation: [socket.recvfrom](https://docs.python.org/3/library/socket.html#socket.socket.recvfrom) 
{{% /col %}}
{{% /multicol %}}

6. about _encoding_ and _decoding_:
    + sockets send and receive _byte sequences_ (type `byte`), not _strings_ (type `str`)
    + byte sequences _literals_ can be created via the `b` prefix, e.g. `b'Hello, world!'`
    + the `encode` and `decode` methods are used to convert between _byte sequences_ and _strings_
        ```python
        data = b'Hello, world' # alternatively data = 'Hello, world'.encode()
        data = data + bytes([33]) # append byte 33, corresponding to '!'
        data = data.decode() # convert to string
        print(data) # prints 'Hello, world!'
        ```
    + default encoding is [UTF-8](https://en.wikipedia.org/wiki/UTF-8), but other encodings are possible
    + the _encoding_ and _decoding_ must be _consistent_ among the sender and the receiver

7. the socket must be _closed_ when no longer needed
    ```python
    sock.close()
    try:
        sock.sendto(...)
        sock.recvfrom(...)
    except OSError as e:
        print(f'Any subseqent send/receive will raise: {e}')
    ```

{{% /section %}}

---


---

{{% import path="reusable/back.md" %}}
