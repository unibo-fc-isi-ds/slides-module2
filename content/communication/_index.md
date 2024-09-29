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
    + the _port_ is the port number of the socket
    + the _address:port_ pair is the _endpoint_ of the communication path

---

{{% section %}}

## Datagram sockets

{{< image src="./udp-sockets.svg" alt="Datagram sockets representation" height="50vh" >}}

- Datagram sockets aim at exchanging _packets_ of bytes, called _datagrams_, among _endpoints_
- __No__ _connection_ is established between the endpoints
    + each datagram send/receive is _independent_ from the others
- There is no difference among client and server sockets
    + each datagram socket may act as a _client_ or a _server_ in any moment
- Each datagram is _self-contained_ can be used to communicate with __many__ other sockets
    + the _address:port_ pair is specified upon sending _each_ datagram
    + $\Rightarrow$ support for _broadcast_ and _multicast_ communication

{{% /section %}}

---


---

{{% import path="reusable/back.md" %}}
