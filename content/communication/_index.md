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
    * very _didactic_: they support very common communication mechanism, which you may find in many other technologies too
        * e.g. __connection-less__ vs. __connection-oriented__ communication
        * e.g. __message-based__ vs. __stream-based__ communication
    + very _elementary_: higher-level communication abstractions can be __built on top__ of them
        + e.g. RPC, _HTTP_, and virtually any application-level protocol

---

## Definition

> A __socket__ is an abstract representation for the _local_ endpoint of a network communication path.

{{< image src="./sockets.svg" width="70%" max-h="50vh" alt="Concept of a socket" >}}

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

## Useful resources

- [Python `socket` module](https://docs.python.org/3/library/socket.html)
- [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)

---

{{% section %}}

## Datagram sockets

{{< image src="./udp-sockets.svg" alt="Datagram sockets representation" width="80%" max-h="40vh" >}}

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

---

### Datagram sockets in Python (pt. 3)

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

{{% section %}}

{{< slide id="example-udp-chat" >}}

## Example: UDP Group Chat

- Let's implement a simple __group chat__ application using _datagram sockets_

- __Peer-to-peer__ communication: each participant sends messages to _all_ the others

- Each participant is __identified__ by a _nickname_ and/or an _endpoint_

- Each __message__ contains
    1. the _nickname_ of the _sender_
    2. the _text_ of the message
    3. the _timestamp_ of the message

- __Command-line__ UI: each participant can type messages to send, and see incoming messages in the _console_

- See {{< github-url repo="lab-snippets" path="snippets/lab2/" >}}

---

## Example: UDP Group Chat

### [Utilities]({{< github-url repo="lab-snippets" path="snippets/lab2/__init__.py" >}}) (pt. 1)

1. A function to _parse_ the _address_ and _port_ from a string, or validate an _address_ and _port_ pair:
    ```python
    def address(ip='0.0.0.0:0', port=None):
        ip = ip.strip()
        if ':' in ip:
            ip, p = ip.split(':')
            p = int(p)
            port = port or p
        if port is None:
            port = 0
        assert port in range(0, 65536), "Port number must be in the range 0-65535"
        assert isinstance(ip, str), "IP address must be a string"
        return ip, port


    ## Usage
    assert address('localhost:8080') == ('localhost', 8080)
    assert address('127.0.0.1', 8080) == ('127.0.0.1', 8080)
    assert address(port=8080) == ('0.0.0.0', 8080)
    ```

2. A function to compose _messages_ into _strings_:
    ```python
    from datetime import datetime

    def message(text: str, sender: str, timestamp: datetime=None):
        if timestamp is None:
            timestamp = datetime.now()
        return f"[{timestamp.isoformat()}] {sender}:\n\t{text}"


    ## Usage
    assert message("Hello, World!", "Alice", datetime(2024, 2, 3, 12, 15)) == "[2024-02-03T12:15:00] Alice:\n\tHello, World!"
    ```
---

## Example: UDP Group Chat

### [Utilities]({{< github-url repo="lab-snippets" path="snippets/lab2/__init__.py" >}}) (pt. 2)

3. A function to get _all_ the _IP addresses_ of the current machine:
    ```python
    import psutil; import socket

    def local_ips():
        for interface in psutil.net_if_addrs().values():
            for addr in interface:
                if addr.family == socket.AF_INET:
                        yield addr.address

    ## Usage
    print(f"Local IPs: {list(local_ips())}")
    # Local IPs: ['127.0.0.1', '137.204.71.x', ...]
    ```

    - the `psutil` module is not Python standard library, but it is available [on PyPI](https://pypi.org/project/psutil/)

<br>

Recall that:
- each OS may have _multiple_ __network interfaces__
- each network interface may have _multiple_ __IP addresses__
- `127.0.0.1` a.k.a. `localhost` is the _loopback_ address, i.e. the address of the _local_ machine
- if the machine is connected to UniBO network, the _local_ IP address may start with `137.204.x.y`

---

## Example: UDP Group Chat

### Defining a class for participants

{{% multicol %}}
{{% col class="col-8" %}}
```python
class Peer:
    # Initialises the peer, reserving the port and adding the peers (if any)
    def __init__(self, port: int, peers=None):
        if peers is None:
            peers = set()
        self.peers = {address(*peer) for peer in peers}
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind(address(port=port))

    @property # Read-only property to get the local endpoint (ip:port)
    def local_address(self):
        return self.__socket.getsockname()

    # Sends a message to all the peers
    def send_all(self, message: str):
        if not isinstance(message, bytes):
            message = message.encode()
        for peer in self.peers:
            self.__socket.sendto(message, peer)

    # Receives a message from a peer (BLOCKING), keeping track of the peer if new
    def receive(self):
        message, address = self.__socket.recvfrom(1024)
        self.peers.add(address)
        return message.decode(), address

    # Closes the socket (releasing the port)
    def close(self):
        self.__socket.close()
```
{{% /col %}}
{{% col %}}
{{< plantuml height="30vh" >}}
class Peer {
    - __socket: socket
    + peers: set
    + local_address: tuple
    ..
    + \_\_init\_\_(port: int, peers=None)
    ..
    + send_all(message: str)
    + receive(): tuple
    + close()
}
{{< /plantuml >}}
{{% /col %}}
{{% /multicol %}}

- The `Peer` class encapsulates the _socket_ and the _peers_ of a participant
- Socket is _created_ behind the scenes, and bound to the _port_ specified by construction
- 1 participant $\leftrightarrow$ 1 peer

---

## Example: UDP Group Chat

### Attempt 1 -- [`example1_udp_chat_wrong`]({{< github-url repo="lab-snippets" path="snippets/lab2/example1_udp_chat_wrong.py" >}})

```python
import sys

peer = Peer(
    port = int(sys.argv[1]), # port number from first command-line argument
    peers = [address(peer) for peer in sys.argv[2:]] # any other command-line argument is "ip:port"
)

print(f'Bound to: {peer.local_address}')
print(f'Local IP addresses: {list(local_ips())}')
while True:
    content = input('> ')
    peer.send_all(message(content, username))
    print(peer.receive()[0])
```

1. Try to run one peer with `poetry run python -m snippets -l 2 -e 1 PORT_A`
    * choose a _port_ number, e.g. `8080`
    * give it _your name_, say `Alice`

2. Try to run another peer with `poetry run python -m snippets -l 2 -e 1 PORT_B IP_A:PORT_A`
    * choose __another__ _port_ number, e.g. `8081`
    * report the IP and port of the first peer (look at its logs)
    * give it _another name_, say `Bob`

3. Make them chat!

4. \[Optional\] If you want to add one more peer, repeat step 2 with a new port number:
    ```bash
    poetry run python -m snippets -l 2 -e 1 PORT_C IP_A:PORT_A IP_B:PORT_B
    ```

---

## Example: UDP Group Chat

### Attempt 1 -- Example logs

{{% multicol %}}
{{% col %}}
#### Peer 1

```text
Bound to: ('0.0.0.0', 8080)
Local IP addresses: ['127.0.0.1', '137.204.x.y', ...]
Enter your username to start the chat:
Alice
> Is there anybody?
[2024-10-03T15:00:22.175104] Bob:
        Hello Alice!
> Hello Bob, how are you?
[2024-10-03T15:01:09.164902] Bob:
        Fine thanks! What about you?
>
```
Alice's terminal is waiting for inputs
{{% /col %}}
{{% col %}}
#### Peer 2

```text
Bound to: ('0.0.0.0', 8081)
Local IP addresses: ['127.0.0.1', '137.204.x.y']
Enter your username to start the chat:
Bob
> Hello Alice!
[2024-10-03T15:00:52.531766] Alice:
        Hello Bob, how are you?
> Fine thanks! What about you?
```
Bob's terminal is waiting for remote messages
{{% /col %}}
{{% /multicol %}}

---

## Example: UDP Group Chat

### Attempt 1 -- Issues

1. Input operations tend to _block_ the current (and only) __thread of execution__

    * __blocking__ `receive`: receiving a message is a blocking operation
        + the peer is _stuck_ waiting for a message, and cannot send messages, nor gather local user's inputs

    * __blocking__ `input`: gathering user's input is a blocking operation too
        + the peer is _stuck_ waiting for the user to type a message, and cannot receive messages

1. Participants are __peers__ at runtime, but initially one acts as a __client__ and the other as a __server__
    * the __client__ must know the __server__'s address, but the __server__'s address is not known in advance
        + $\Rightarrow$ the $1^{st}$ participant cannot initiate the conversation
        + $\Rightarrow$ the $2^{st}$ participant must know the $1^{st}$ participant's address

1. Lack of __graceful__ termination
    + locally, the only way out is to _forcefully terminate_ the program (e.g. with `Ctrl+C`)
    + the remote peer is _not notified_ of the termination

1. Lack of __authentication__
    + peers are assumed to _declare_ their own identity in an honest way
        * by including it in the payload of the messages
    + the _identity_ is not _verified_ in any
        * e.g. no check that the _username_ is unique, or that the _address_ corresponds to the _username_
        * malicious peers may _impersonate_ other peers

1. UDP is __unreliable__: messages may get _lost_, _delayed_, delivered _out of order_, or _duplicated_
    + our code does not handle these cases at all

---

## Example: UDP Group Chat

### Attempt 1 -- Possible Improvements

1. Input operations tend to _block_ the current (and only) __thread of execution__
    - solution: use __multiple threads__ to handle _input_ (1 per input source + another)

1. Participants are __peers__ at runtime, but initially one acts as a __client__ and the other as a __server__
    - have a central server acting as a __broker__ for the participants

1. Lack of __graceful__ termination
    1. catch the closure of the terminal
    2. send a _termination message_ to the other peers
    3. close the socket and exit
    - upon receiving a _termination message_, do something
        + e.g. print a _farewell_ message for the leaving peer

1. Lack of __authentication__
    - public-key cryptography (out of scope in this course)
    - central server supporting some sort of _authentication_ protocol

1. UDP is __unreliable__: messages may get _lost_, _delayed_, delivered _out of order_, or _duplicated_
    - implement retry mechanisms, or use a reliable protocols (e.g. TCP)

---

## Example: UDP Group Chat

### Attempt 2 -- [`example2_udp_chat`]({{< github-url repo="lab-snippets" path="snippets/lab2/example2_udp_chat.py" >}}) (pt. 1)

1. Let's address the _blocking_ issue by using _threads_ to handle _input_ and _reception_:

    ```python
    import threading

    class AsyncPeer(Peer):
        # Creates a new asynchoronous peer, with a callback for incoming messages
        def __init__(self, port, peers=None, callback=None):
            super().__init__(port, peers)
            self.__receiver_thread = threading.Thread(target=self.__handle_incoming_messages, daemon=True)
            self.__callback = callback or (lambda *_: None) # callback does nothing by default
            self.__receiver_thread.start()

        # This private method is executed in a separate thread, i.e. in background
        def __handle_incoming_messages(self):
            while True:
                message, address = self.receive()
                self.on_message_received(message, address)

        # Callback being invoked when a message is received
        def on_message_received(self, message, sender):
            self.__callback(message, sender)
    ```

2. `AsyncPeer` is a subclass of `Peer` exposing a `callback` for __asynchronously__ handling _incoming_ messages
    ```python
    ## Usage
    AsyncPeer(
        port = ...,
        peers = ... ,
        callback = lambda msg, snd: # handle incoming messages here
    )
    ```

---

> Important notion of ["callback"](https://en.wikipedia.org/wiki/Callback_(computer_programming)):
> a function that is stored as data (a reference) and designed to be called by another function – often back to the original abstraction layer.

![A callback is often back on the level of the original caller.](https://upload.wikimedia.org/wikipedia/commons/d/d4/Callback-notitle.svg)

---

## Example: UDP Group Chat

### Attempt 2 -- [`example2_udp_chat`]({{< github-url repo="lab-snippets" path="snippets/lab2/example2_udp_chat.py" >}}) (pt. 1)

3. Creating a minimal group chat is now straightforward:

    ```python
    import sys

    peer = AsyncPeer(
    port = int(sys.argv[1]), # port number from first command-line argument
    peers = [address(peer) for peer in sys.argv[2:]], # any other command-line argument is "ip:port"
        callback = lambda message, _: print(message) # print incoming messages on the console
    )

    print(f'Bound to: {peer.local_address}')
    print(f'Local IP addresses: {list(local_ips())}')
    username = input('Enter your username to start the chat:\n')
    print('Type your message and press Enter to send it. Messages from other peers will be displayed below.')
    while True:
        content = input()
        peer.send_all(message(content, username))
    ```

4. Let's now try the new version of the chat application
    1. run the first peer with `poetry run python -m snippets -l 2 -e 2 PORT_A`
    2. run the second peer with `poetry run python -m snippets -l 2 -e 2 PORT_B IP_A:PORT_A`
    3. make them chat!

---

## Example: UDP Group Chat

### Attempt 2 -- Remaining issues

1. Participants are __peers__ at runtime, but initially one acts as a __client__ and the other as a __server__
1. Lack of __graceful__ termination
    + let's focus on this one
1. Lack of __authentication__
1. UDP is __unreliable__: messages may get _lost_, _delayed_, delivered _out of order_, or _duplicated_

---

## Example: UDP Group Chat

### Attempt 3 -- [`example4_udp_chat_graceful`]({{< github-url repo="lab-snippets" path="snippets/lab2/example4_udp_chat_graceful.py" >}}) (pt. 1)

1. Let's address the __graceful termination__ issue by _catching exceptions_ and _communicating_ them accordingly

2. First, let's create a special kind of message to signal the _termination_ of a peer to other peers.
Upon receiving this message, a peer should _remove_ the sender from the local list of peers:
    ```python
    EXIT_MESSAGE = "<LEAVES THE CHAT>"


    class AsyncPeer(Peer):
        # other methods are unchanged

        def __handle_incoming_messages(self):
            while True:
                message, address = self.receive()
                if message.endswith(EXIT_MESSAGE):          # notice this
                    self.peers.remove(address)
                self.on_message_received(message, address)
    ```

3. Finally, let's _catch_ the user trying to terminate one peer, and _send_ the _termination message_ to the other peers:
    ```python
    # initialisation of the program is unchanged
    print('Type your message and press Enter to send it. Messages from other peers will be displayed below.')
    while True:
        try:
            content = input()
            peer.send_all(message(content, username))
        except (EOFError, KeyboardInterrupt):
            peer.send_all(message(EXIT_MESSAGE, username))
    peer.close()
    exit(0) # explicit termination of the program with success
    ```
    - `EOFError` is raised when the user _closes_ the terminal's input stream _politely_ (e.g. via `Ctrl+D`)
    - `KeyboardInterrupt` is raised when the user _interrupts_ the program (e.g. via `Ctrl+C`)

---

## Example: UDP Group Chat

### Attempt 3 -- [`example4_udp_chat_graceful`]({{< github-url repo="lab-snippets" path="snippets/lab2/example4_udp_chat_graceful.py" >}}) (pt. 2)

4. __Rationale__: no need to terminate the application when one peer leaves the chat
    - the chat should continue, and the leaving peer should be _forgotten_
    - other peers may _join_ the chat at any time

5. Let's now try the new version of the chat application
    1. run the first peer with `poetry run python -m snippets -l 2 -e 4 PORT_A`
    2. run the second peer with `poetry run python -m snippets -l 2 -e 4 PORT_B IP_A:PORT_A`
    3. make them chat!

6. What you should observe:
    - we still require the second peer to start the conversation
    - participants should be able to use the application without seeing _exceptions_ in their terminal
    - there could be situations where messages are _lost_ or _duplicated_
        * consider using [`example3_udp_streamer`]({{< github-url repo="lab-snippets" path="snippets/lab2/example3_udp_streamer.py" >}})
        to stress-test the chat with _many_ messages, and to observe the _reliability_ of the communication protocol

---

## Example: UDP Group Chat

### Attempt 2 -- Remaining issues

1. Participants are __peers__ at runtime, but initially one acts as a __client__ and the other as a __server__
1. Lack of __authentication__
1. UDP is __unreliable__: messages may get _lost_, _delayed_, delivered _out of order_, or _duplicated_
    + let's focus on this one

{{% /section %}}

---

{{% section %}}

{{< slide id="stream-sockets" >}}

## Stream sockets

{{< image src="./tcp-sockets.svg" alt="Stream sockets representation" width="80%" max-h="50vh" >}}

- Stream sockets aim at exchanging _streams_ of bytes among _endpoints_
    + __stream__ $\approx$ sequence of bytes with __no__ _length limitation_
        + thanks to the TCP protocol, the stream is _reliable_ and _ordered_
        + the stream is __directed__: either _from_ the client _to_ the server, or vice versa
- A __connection__ must be established between 2 (_and only 2_) endpoints
    + the connection is _full-duplex_, i.e. data may flow in both verses, simultaneously
    + each connection involves _2 streams_
- There is a clear distinction among _client_ and _server_ sockets
    + the two sorts of sockets have _different_ functionalities and API
- Stream sockets _only_ support __one-to-one__ communication
    + to communicate with multiple peers, multiple connections must be established

---

## Stream sockets in Python (pt. 1)

1. Python's `socket` _class_, from the `socket` _module_ works for _stream_ sockets too
    + simply initialize them with different _socket type_:

    ```python
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a new stream socket
    ```
    + `AF_INET` specifies the _address family_ (IPv4)
    + `SOCK_STREAM` specifies the _socket type_ (stream)

2. As for _datagram_ sockets, the _stream_ socket must be _bound_ to a local _address_ and _port_ before being used:
    ```python
    sock.bind(('W.X.Y.Z', 12345)) # bind the socket to the local address and port
    ```
    * the `bind` method is the same as for _datagram_ sockets
    * use `"0.0.0.0"` as the __IP address__ to bind to _all_ local addresses
    * use `0` as the __port__ to let the OS choose a free port
        + this is most commonly what _clients_ do

---

## Stream sockets in Python (pt. 2)

3. What happens next depends on whether we are on the _client_ or the _server_ side of the connection:

{{% multicol %}}
{{% col %}}
- __Server__:
    1. actively start **listen**ing for incoming _connections_
    2. actively wait to __accept__ an incoming connection
    3. __send__ and __receive__ data

- __Client__:
    1. actively __connect__ to a server socket (requires knowing the server's _IP address_ and _port_)
    2. __send__ and __receive__ data
{{% /col %}}
{{% col %}}
{{< image max-h="80vh" alt="Diagram showing the different API of client and server stream sockets" src="./stream-sockets.avif" >}}
{{% /col %}}
{{% /multicol %}}

---

## Stream sockets in Python (pt. 3)

### Client-side (connection)

4. To _connect_ to a server, the client must know the server's _IP address_ and _port_:
    ```python
    try:
        sock.connect(('A.B.C.D', 54321)) # connect to the server at address A.B.C.D:54321
    except ConnectionRefusedError:
        print("The server is reachable but not wlling to accept the connection")
    except TimeoutError:
        print("The server is not reachable")
        print("This may occur after a LONG while")
    ```
    + the `connect` method is used to establish a connection to a _remote_ endpoint (acting as _server_)
    + the argument is a _tuple_ with the _address_ and _port_ of the _server_
    + the operation is __blocking__, until the connection is established
    + when the timeout occurs can be regulated ([see doc](https://docs.python.org/3/library/socket.html#notes-on-socket-timeouts))
        + [`socket.setdefaulttimeout(SECONDS)`](https://docs.python.org/3/library/socket.html#socket.setdefaulttimeout) sets the default timeout for _all_ sockets (where `socket` is the module)
        + [`s.settimeout(SECONDS)`](https://docs.python.org/3/library/socket.html#socket.socket.settimeout) sets the timeout for _a single_ socket (where `s` is the socket instance)
        + `SECONDS` $\equiv$ `None` means _no timeout_

---

## Stream sockets in Python (pt. 4)

### Client-side (communication)

5. Once the connection is __established__, the client can _send_ and _receive_ data to/from the server:
    + this implies writing/reading _chuncks_ of _bytes_, on the socket's output/input _stream_

> __Golden rule__: always be aware of _how many bytes_ are being sent/received at a time
> <be> (i.e. _avoid_ __unilimited__ reads/writes: these may saturate the network, or the local memory)

{{% fragment %}}

6. How to __send__ data to remove via _buffered_ __write__:
    ```python
    data: bytes = b'My very important payload' # this is an array of bytes of knwon length
    sock.sendall(data) # send the data to the server
    # .. other sending operations ...
    sock.shutdown(socket.SHUT_WR) # signal to the remote that no more data will be sent
    ```
    + cf. documentation of [`sock.sendall`](https://docs.python.org/3/library/socket.html#socket.socket.sendall) and [`sock.shutdown`](https://docs.python.org/3/library/socket.html#socket.socket.shutdown)
    + the method is __blocking__, until all the data is sent
    + `data` is a _buffer_ of known size

{{% fragment %}}

7. How to __receive__ data from the server via _buffered_ __read__:
    ```python
    BUFFER_SIZE = 4096 # maximim amount of bytes to read at once, better to be constant
    data: bytes = sock.recv(BUFFER_SIZE) # receive up to 4096 bytes from the server
    if not data: # a.k.a. data == b''
        print("The remote is over with the data") # this may happen if the remoted does shutdown(socket.SHUT_WR)
    # .. other receiving operations ...
    sock.shutdown(socket.SHUT_RD) # signal to the remote that no more data will be received
    ```
    + cf. documentation of [`sock.recv`](https://docs.python.org/3/library/socket.html#socket.socket.recv)
    + the method is __blocking__, until _some_ data is received
    + here the buffer is a memory area ($\approx$ byte array) of 4KiB

{{% /fragment %}}

{{% /fragment %}}

---

## Stream sockets in Python (pt. 5)

### Client-side (closing)

8. Once the communication is over, the client must _close_ the connection:
    ```python
    sock.close() # close the connection with the server
    ```
    + the [`close`](https://docs.python.org/3/library/socket.html#socket.close) method is used to _close_ the connection
    + the method is __blocking__, until the connection is closed (usually very fast)
    + the _server_ will be notified of the _closing_ of the connection

---

## Stream sockets in Python (pt. 5)

### Server-side

4. Server sockets will start _listening_ for incoming connections, and will _accept_ them __one by one__:
    ```python
    sock.listen(5) # start listening for incoming connections, with a maximum of 5 pending connections
    while True:
        client_sock, client_address = sock.accept() # accept a new connection
        # client_sock is a new socket, connected to the client
        # client_address is the (ip, port) address of the client
        # .. other operations with the client ..
        client_sock.close() # close the connection with the client
    ```
    + the [`listen`(BACKLOG_LENGTH)](https://docs.python.org/3/library/socket.html#socket.socket.listen) method is used to start listening for incoming connections
        * this is __not blocking__: it simply sets the `BACKLOG_LENGTH`, i.e. the amount of pending (unaccepted) connections the OS will enqueue before _refusing_ new ones
            - refused connections will receive a `ConnectionRefusedError` on the remote side
    + the [`accept`](https://docs.python.org/3/library/socket.html#socket.socket.listen) method is used to accept a new connection
        * this dequeues the _first_ pending connection, or __blocks__ until a new connection arrives
    + the `client_sock` is a new _socket_ instance, connected to the _client_
    + the `client_address` is the _address tuple_ of the _client_

5. The new socket `client_sock` is used to _send_ and _receive_ data to/from the client
    + this works exactly as for the _client_ side...
    + ... except that it is already _connected_ to the client
    + the server socket `sock` is _only_ used to _accept_ new connections

6. Eventually, some event should _break_ the `while True` loop, and the server should _close_ the listening socket:
    ```python
    sock.close() # close the server socket (do not accept new connections)
    ```

---

## Stream sockets in Python (pt. 6)

### Connection-oriented message exchange

1. Streams are cool for sending data in _reliable_ and _ordered_ way, but what if one wants to send a sequence of _messages_?

2. Common use case of _stream_ sockets:
    1. _start_ a connection between any two peers...
    2. ... _keep_ the connection _alive_ for as long as possible...
    3. ... _send messages_ back and forth without the need to _reconnect_ every time

3. A common __pattern__ for _message exchange_ is to __prefix__ each message with its __length__:
    + this way, the _receiver_ knows _how many bytes_ to _read_ from the _stream_
    + the _sender_ must _send_ the _length_ of the message _before_ sending the _message_ itself
    + the _receiver_ must _read_ the _length_ of the message _before_ reading the _message_ itself

---

## Stream sockets in Python (pt. 6)

### Connection-oriented message exchange (example)

1. Suppose that one node wants to send the following messages (of different sizes) to another node:
    ```python
    messages = ["The user pressed UP and RIGHT", "The user released RIGHT, and pressed LEFT", "The user released LEFT"]
    ```

2. The _sender_ must _prefix_ each message with its _length_:
    ```python
    for message in messages:
        length = len(message)
        payload = length.to_bytes(4, 'big') + message.encode()
        sock.sendall(payload)
    sock.shutdown(socket.SHUT_WR) # no more data to send
    ```
    + `length.to_bytes(4, 'big')` converts the _length_ (an `int`) to a _4-byte_ _big-endian_ byte sequence (i.e. a _32-bit_ integer) representing the same value
    + `message.encode()` converts the _string_ to a _byte sequence_ (UTF-8 encoding is used by default)
    + `payload` is the _concatenation_ of the _length_ (fixed size) and the _message_ (variable size)
        - e.g. `b'\x00\x00\x00\x1dThe user pressed UP and RIGHT'` where `\x00\x00\x00\x1d` $\equiv$ `29` (in decimal)

3. The _receiver_ must _read_ the _length_ of the message _before_ reading the _message_ itself:
    ```python
    while True:
        length = sock.recv(4) # read the length of the message
        if not length: # no more data to read
            break
        length = int.from_bytes(length_bytes, 'big') # convert the length to an integer
        message = sock.recv(length) # read the exact amount of bytes to get the message
        message = message.decode() # convert the byte sequence to a string
        print(f"Use received message {message} to do something")
    sock.shutdown(socket.SHUT_RD) # no more data to read
    ```

{{% /section %}}

---

{{% section %}}

## Example: TCP Echo

- Let's implement a simple __echo__ application using _stream sockets_
    + the client will _forward_ it's _standard input stream_ to the server, which will send it back to the client, which will _print it_
    + essentially, just like the `cat` command in Unix-like systems, when no argument is passed
        * but with the _server_ acting as the intermediary

- Very didadical example, no real-world application
    + but it is a good way to understand the _stream_ sockets

- We will investigate what happens when the data stream is _too long_

- See <{{< github-url repo="lab-snippets" path="snippets/lab3/" >}}>

---

## Example: TCP Echo

### Server side

{{% multicol %}}
{{% col %}}
```python
import sys

BUFFER_SIZE = 1024
mode = sys.argv[1].lower().strip() # 'server' for server, 'client' for client
port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('0.0.0.0', port)) # bind to any local address, on the specified port
    server.listen(1) # only one connection at a time
    print(f"# echo server listening on port {port}")
    sock, addr = server.accept()
    print(f"# start echoing data from {addr}")
    while True:
        buffer = sock.recv(BUFFER_SIZE)
        if not buffer:
            break
        sock.sendall(buffer)
        print(f"# echoed {len(buffer)} bytes: {buffer}", flush=True)
    sock.close()
    print("# connection closed")
```
{{% /col %}}
{{% col %}}
<br>

1. The server _listens_ for incoming connections, and _accepts_ them one by one
2. Upon establishing a _connection_:
    1. the server _reads_ __chunks__ of data of _fixed size_ from the client
        * if _no byte_ is read, then the interaction is _over_
    2. the server _sends_ the chunk back to the client
    3. the server _logs_ which and how many bytes it has received

{{% /col %}}
{{% /multicol %}}

Launch the _server_ via the commnad `poetry run python -m snippets -l 3 -e 1 server PORT`
(cf. [source code]({{< github-url repo="lab-snippets" path="snippets/lab3/example1_tcp_echo_wrong.py" >}}))

---

## Example: TCP Echo

### Client Side, Attempt 1

{{% multicol %}}
{{% col %}}
```python
import sys

BUFFER_SIZE = 1024
mode = sys.argv[1].lower().strip() # 'server' for server, 'client' for client
remote_endpoint = address(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 0)) # any port on is fine
sock.connect(remote_endpoint)
print(f"# connected to {remote_endpoint}")
while True: # forward the whole standard input to the server
    buffer = sys.stdin.buffer.read(BUFFER_SIZE)
    if not buffer:
        break
    sock.sendall(buffer)
sock.shutdown(socket.SHUT_WR) # nothing more to send
while True: # receive the whole stream from the server
    buffer = sock.recv(BUFFER_SIZE)
    if not buffer:
        break
    sys.stdout.buffer.write(buffer)
    sys.stdout.buffer.flush()
sock.close()
print("# connection closed")
```
{{% /col %}}
{{% col %}}
<br>

1. The client _connects_ to the server
2. The client _forwards_ its _standard input stream_ to the server
    + `BUFFER_SIZE` bytes at a time
    + until the _end of the stream_ is reached
        - e.g. when the user presses `Ctrl+D` on Unix-like systems
        - or `Ctrl+Z` then `Enter` on Windows
3. The client _signals_ it has _no more data_ to send
    + by shutting down the _write_ part of the socket
4. The client _receives_ the _echoed_ data from the server, and _prints_ it to the _standard output_
    + `BUFFER_SIZE` bytes at a time
    + until the _end of the stream_ is reached
        - e.g. when the server _closes_ the connection
5. The client _closes_ the connection

{{% /col %}}
{{% /multicol %}}

Launch the _client_ via the commnad `poetry run python -m snippets -l 3 -e 1 client SERVER_IP:SERVER_PORT`
(cf. [source code]({{< github-url repo="lab-snippets" path="snippets/lab3/example1_tcp_echo_wrong.py" >}}))

---

## Example: TCP Echo

### Attempt 1 -- Manual Testing

1. Run the _server_ with `poetry run python -m snippets -l 3 -e 1 server PORT`
    * choose a _port_ number, e.g. `8080`

2. Run the _client_ with `poetry run python -m snippets -l 3 -e 1 client SERVER_IP:SERVER_PORT`
    * choose the _server's IP address_ and _port_, e.g. `localhost:8080`

3. Write some text in the _client_'s terminal, and press `Ctrl+D` (Unix-like) or `Ctrl+Z` then `Enter` (Windows)
    * the _server_ should _echo_ the text back to the _client_
    * you should see the text you worte _duplication_ in the _client_'s terminal
    * you can also see the _server_'s logs

{{% fragment %}}

###

4. Yay! It seems working, but let's try to send a _long_ message
    1. let's re-launch the server as before
    2. let's re-lanch the client as follows:
        `poetry run python rand.py | poetry run python -m snippets -l 3 -e 1 client SERVER_IP:SERVER_PORT`
        + where [the program `rand.py`]({{< github-url repo="lab-snippets" path="rand.py" >}}) aims at generating an _infinite_ sequence of random numbers
        + where `|` is the _pipe_ operator, which _redirects_ the _standard output_ of the _left_ command to the _standard input_ of the _right_ command

{{% /fragment %}}

---

## Example: TCP Echo

### Attempt 1 -- Issues

1. If the _client_'s input stream is too long...

2. ... and the _client_ only starts _receiving_ the _echoed_ data __after__ it has _sent_ _all_ the data...

3. ... even if the _server_ _echoes_ the data back to the _client_ one chunch at a time...

4. ... the _client_ ingoing _buffer_ may saturate, and the will eventually _slow down_ or _stop_ sending data
    + this is just how TCP works: recall [TCP's flow control](https://en.wikipedia.org/wiki/Transmission_Control_Protocol#Flow_control)

5. So, a very long stream + this particular client implementation = __deadlock__

6. Solution: __make the client *interleave* sending and receiving__

---

## Example: TCP Echo

### Attempt 2 -- Client Side

{{% multicol %}}
{{% col %}}
```python
# prologue of the script is unchanged w.r.t. attempt 1

print(f"# connected to {remote_endpoint}")
while True:
    buffer_local = sys.stdin.buffer.read(BUFFER_SIZE)
    if buffer_local:
        sock.sendall(buffer_local)
    buffer_remote = sock.recv(BUFFER_SIZE)
    if buffer_local != buffer_remote: # check if the echoed data is correct
        print(f"Wrong echoed data:", file=sys.stderr)
        print(f"     local: {buffer_local}", file=sys.stderr)
        print(f"    remote: {buffer_remote}", file=sys.stderr)
        break
    sys.stdout.buffer.write(buffer_remote)
    sys.stdout.buffer.flush()
sock.close()
print("# connection closed")
```
{{% /col %}}
{{% col %}}
<br>

1. The client _connects_ to the server
2. The client _forwards_ its _standard input stream_ to the server
    + `BUFFER_SIZE` bytes at a time
3. After _each_ chunck of data is _sent_
    + the client _receives_ the _echoed_ data from the server
    + if the sent and received data _differ_, the client _stops_ the communication, printing an error
4. When the _end of the input stream_ is reached and the last chuck of data is _received_
    - the client _closes_ the connection

{{% /col %}}
{{% /multicol %}}

---

## Example: TCP Echo

### Attempt 2 -- Manual Testing

1. Run the _server_ with `poetry run python -m snippets -l 3 -e 2 server PORT`
    * choose a _port_ number, e.g. `8080`

2. Run the _client_ with `poetry run python -m snippets -l 3 -e 2 client SERVER_IP:SERVER_PORT`
    * choose the _server's IP address_ and _port_, e.g. `localhost:8080`

3. Test it works as attempt 1 for short messages

4. Now, let's try to send a _long_ message
    1. let's re-launch the server as before
    2. let's re-lanch the client as follows:
        `poetry run python rand.py | poetry run python -m snippets -l 3 -e 2 client SERVER_IP:SERVER_PORT`
        + where [the program `rand.py`]({{< github-url repo="lab-snippets" path="rand.py" >}}) aims at generating an _infinite_ sequence of random numbers
        + where `|` is the _pipe_ operator, which _redirects_ the _standard output_ of the _left_ command to the _standard input_ of the _right_ command
    3. this time it should work

---

## Example: TCP Echo

### Attempt 2 -- Example output

#### Client

`poetry run python rand.py | poetry run python -m snippets -l 3 -e 2 client localhost:8080`

```text
502573549
-453960860
-381856593
-286722763
-211192745
-2134899619
-1711689099
-1503312253
-1701591573
-1205926153
...
...
...
```

#### Server

`poetry run python -m snippets -l 3 -e 2 server 8080`

```text
# echo server listening on port 8080
# start echoing data from ('127.0.0.1', 44267)
# echoed 1024 bytes: b'502573549\n-453960860\n-381856593\n-286722763\n-211192745\n-2134899619\n-1711689099\n-1503312253\n-1701591573\n-1205926153\n-50412914\n213710709\n-577009406\n219425615\n-252566774\n61565769\n1922001980\n-1873744585\n936906805\n2078720013\n1222654877\n-1289501938\n1395814954\n-1798177949\n-2041286581\n1932951426\n288129622\n803985826\n496679522\n-926425443\n14153399\n904025100\n-319222238\n734804897\n1102692378\n-262778378\n-377056832\n2082693948\n48281326\n-1760419856\n-956463672\n381424876\n1190469830\n-94801835\n-506278031\n-1861075783\n-321914757\n-151797661\n-974543774\n-676394188\n-1623558767\n-548408375\n-1997202209\n371955653\n-53265711\n974383730\n1230806274\n-1680300244\n-1878714490\n-674007318\n-1736582601\n1041815141\n-2046487010\n-1381702097\n-417225600\n-816967349\n1698648802\n-375787019\n-1796572572\n-1912254955\n657751568\n-792402858\n682694407\n-708204980\n1315814466\n1659654562\n1422679836\n1854502958\n-335151514\n1055416618\n-1791736404\n2127088482\n818796704\n-1398097789\n-1076649501\n-1950422542\n677576321\n1510589358\n886913109\n-1977200570\n-920062497\n-72348672\n-1656296063\n18'
# echoed 1024 bytes: b'60998094\n595222830\n-205208337\n834971633\n2084933832\n127694008\n211867414\n-1314672239\n329159798\n1239086726\n-65480338\n-1325348410\n78317563\n-147023906\n-718316757\n-1263506431\n877536631\n461893425\n-185087136\n-928284670\n-1686544446\n-468846558\n-1444844383\n414235162\n1774142424\n-1424176065\n264020445\n-2094294486\n-28058625\n-1391733741\n1039418086\n-1082553917\n1234585496\n-557844468\n-444121114\n-1868175869\n983621092\n1562181369\n-1130324982\n-1110872934\n-1563560497\n-1947233464\n219012865\n-1195987860\n-676060453\n-783549042\n583654808\n-277637291\n1885661158\n2014417331\n1596822218\n1965074998\n1664866272\n-574923596\n1247714696\n-1840435092\n-2005991425\n-718194566\n1902005952\n1032386525\n-1344433047\n448123247\n-1128830726\n1328377169\n1349144940\n898276016\n-313043102\n-143686687\n-401517594\n1885404533\n-381222101\n-459800837\n597736346\n1243757372\n1107668700\n741676479\n1902621581\n-1395444549\n1370602517\n1330286387\n1060817734\n-2046498769\n1390476769\n217760508\n-2008484501\n-1114114459\n22555323\n1070349670\n1366422557\n-1286331789\n1275922128\n-785260906\n-962938519\n17'
...
...
...
```

{{% /section %}}

---

{{% section %}}

{{< slide id="example-tcp-chat" >}}

## Example: TCP Chat

TL;DR: Let's redo the UDP chat, but with TCP, and with _no groups_

- Let's implement a simple __1-to-1 chat__ application using _stream sockets_

- __Client-server__ communication: each participant sends messages to _all_ the others

- Each participant is __identified__ by a _nickname_ and/or an _endpoint_

- Each __message__ contains
    1. the _nickname_ of the _sender_
    2. the _text_ of the message
    3. the _timestamp_ of the message

- __Command-line__ UI: each participant can type messages to send, and see incoming messages in the _console_

- See {{< github-url repo="lab-snippets" path="snippets/lab3/example3_tcp_chat.py" >}}

---

{{< slide id="utilities" >}}

## Example: TCP Chat

### [Utilities]({{< github-url repo="lab-snippets" path="snippets/lab3/__init__.py" >}}) (pt. 1)

![](https://www.plantuml.com/plantuml/svg/bPAnZjim38PtFmMHvH8qpWC8xLGKtRgqkw38J2oSGXgYSjVYUkzUMP9Z1u5nw1B554dz_FbPRqJWAnEXZOu9tXe0W1Qq5hRF61MKyr2EVFi9F5lZjUcwW28AudNmMAy2NZZYmrrjQZqBTWgEp7uE6k-FnZuhE5qfoxXT1RJeNZ3es0SqgR2SZiw7N_bVVLLhHovglIqozp3r_FA32NSrIv2wxGL5p1aLI0pJHNrckylH6Xorfj1DIs-eyvWUidn90dHj9Dkf2vF65wIupR-vrHu6yyUpwSfNLe2Xkh87387JrxVV5eTnxbtptZJ44S7ZAGAV5gjflYDXC145SdzHJGkRpLELyRJPA7ZjaS103O6JQRAkvEQHvipO8zXvzqxAp2KtQrjqfQ8MsDfha1HqVgo-NAxah8d9aGQfWr5zqrIkl4EAyFQm90pZJYiZ3yjwd-f_vhmRa-j4jk2THAIFG6bXXRM5k8730p-h3CpkVO31cAWMszn3dNwTXJiCPpA2E_SPZUBE6XR5aFjT5zz1eWbHgcLfYb9GHvah25-pR8iJ7PWgZwcidtYIoCFA4pmiNe3_G2fRFDRCtYx0cXs4pt_Rq5R65CZrs1Pg-7INTUWErIe5Dk3er3y0)

---

## Example: TCP Chat

### [Utilities]({{< github-url repo="lab-snippets" path="snippets/lab3/__init__.py" >}}) (pt. 2)

- `Connection`: a _communication channel_ among 2 endponts, for sending and _asynchrnously_ receiving messages _via TCP_
    + backed by a _stream socket_ for the communication
    + uses a _thread_ for the _asynchronous_ reception of messages
    + provides a _callback_ for handling _incoming_ messages
    + provides a _method_ for _sending_ messages

- `Client`: a particular case of `Connection` which _connects_ to a _server_ upon creation

- `Server`: a facility to _listen_ for incoming _connections_ and _accept_ them, creating a `Connection` for each of them
    + backed by a _stream socket_ for the listening
    + uses a _thread_ for the _asynchronous_ _acceptance_ of connections
    + provides a _callback_ for handling _incoming_ connections

---

## Example: TCP Chat

(cf. source code at <{{< github-url repo="lab-snippets" path="snippets/lab3/example3_tcp_chat.py" >}}>)

### Client Side

1. Prologue:
    ```python
    import sys

    mode = sys.argv[1].lower().strip() # 'server' for server, 'client' for client
    remote_endpoint = sys.argv[2]
    ```

2. A callback for handling _incoming_ messages:
    ```python
    def on_message_received(event, payload, connection, error):
        match event:
            case 'message':
                print(payload) # print any message received
            case 'close':
                print(f"Connection with peer {connection.remote_address} closed") # inform the user the connection is closed
                global remote_peer; remote_peer = None # forget about the disconnected peer
            case 'error':
                print(error) # inform the user about any error which occurs
    ```

3. _Establish_ the connection, _register_ the callback:
    ```python
    remote_peer = Client(server_address=address(remote_endpoint), callback=on_message_received)
    print(f"Connected to {remote_peer.remote_address}")
    ```

4. Get _outgoing_ messages from the console and _send_ them to the remote peer:
    ```python
    username = input('Enter your username to start the chat:\n')
    print('Type your message and press Enter to send it. Messages from other peers will be displayed below.')
    while True:
        try:
            content = input()
            send_message(content, username) # sends the message to the remote peer, if message is not empty and remote peer is connected
        except (EOFError, KeyboardInterrupt):
            if remote_peer:
                remote_peer.close()
            break
    ```

---

## Example: TCP Chat

(cf. source code at <{{< github-url repo="lab-snippets" path="snippets/lab3/example3_tcp_chat.py" >}}>)

### Server Side

1. Prologue:
    ```python
    import sys

    mode = sys.argv[1].lower().strip() # 'server' for server, 'client' for client
    port = int(sys.argv[2])
    remote_peer = None
    ```

2. Callback `on_message_received` is exactly as in the _client_ side

3. Server-specific callback for handling ingoing connections:
    ```python
    def on_new_connection(event, connection, address, error):
        match event:
            case 'listen':
                print(f"Server listening on port {address[0]} at {", ".join(local_ips())}")
            case 'connect':
                print(f"Open ingoing connection from: {address}")
                connection.callback = on_message_received # attach callback to the new connection
                global remote_peer; remote_peer = connection # assign the new connection to the global variable
            case 'stop':
                print(f"Stop listening for new connections")
            case 'error':
                print(error)
    ```

4. Actually start the server:
    ```python
    server = Server(port=port, callback=on_new_connection)
    print(f"Server started on port {port}")
    ```

5. Getting & sending messages is exactly as in the _client_ side

---

## Example: TCP Chat

### Manual Testing

1. Run the _server_ with `poetry run python -m snippets -l 3 -e 3 server PORT`
    * choose a _port_ number, e.g. `8080`

2. Run the _client_ with `poetry run python -m snippets -l 3 -e 3 client SERVER_IP:SERVER_PORT`
    * choose the _server's IP address_ and _port_, e.g. `localhost:8080`

3. This should work more or less like the UDP chat, but _no message-dispatching issues_
    * try to _gracefully_ close the connection by pressing `Ctrl+D` (Unix-like) or `Ctrl+Z` then `Enter` (Windows) on some peer: the other peer should notice it!
        - thanks to _connection-orientation_, peers can react to the _closing_ of the connection

{{% /section %}}

---

{{< slide id="exercise-tcp-group-chat" >}}

## Exercise: TCP Group Chat

- __Prerequisites__:
    1. understand [stream sockets](#/stream-sockets)
    2. understand the [UDP _group_ chat example](#/example-udp-chat)
    3. understand the [TCP chat example](#/example-tcp-chat)
    4. understand the provided Python code: [`snippets/lab3/__init__.py`]({{< github-url repo="lab-snippets" path="snippets/lab3/__init__.py" >}}), [`snippets/lab3/example3_tcp_chat.py`]({{< github-url repo="lab-snippets" path="snippets/lab3/example3_tcp_chat.py" >}})

- __Goal__: support group chats in TCP
    * where clients may appear and disappear at any time
    * similarly to what happens for the UDP _group_ chat example
    * in such a way _each peer **broadcasts** messages to all the other peers it has been contacted with so far_

- __Hints__:
    * you can and should reuse the provided code, possibly modifying it
    * there's no need anymore to distinguish among _servers_ and _clients_: all peers act simultaneously as both
    * peers may be informed about the _endpoints_ of other peers at _launch time_ (via _command-line_ arguments)

- __Deadline__: December 31st, 2025

- __Incentive__: +1 point on the final grade (if solution is satisfying)

- __Submission__:
    1. fork the [`lab-snippets` repository]({{< github-url repo="lab-snippets" >}})
    2. create a new branch named `exercise-lab3`
    3. commit your solution in the `snippets/lab3` directory (possibly in a new file named `exercise_tcp_group_chat.py`)
    4. push the branch to your fork & create a __pull request__ to the original repository, entitled `[{{<academic_year>}} Surname, Name] Exercise: TCP Group Chat`
        - in the pull request, describe your solution, motivate your choices, and explain how to test it

---

{{% import path="reusable/back.md" %}}
