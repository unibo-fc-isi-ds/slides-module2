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

## Useful resources

- [Python `socket` module](https://docs.python.org/3/library/socket.html)
- [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)

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
        + the peer is _stuck_ waiting for a message, and cannot send messages...
        + ... nor gather local user's inputs

    * __blocking__ `input`: gathering user's input is a blocking operation too
        + the peer is _stuck_ waiting for the user to type a message...
        + ... and cannot receive messages

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

## Stream sockets

{{< image src="./tcp-sockets.svg" alt="Stream sockets representation" height="50vh" >}}

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

### Stream sockets in Python (pt. 1)

1. Python's `socket` _class_, from the `socket` _module_ works for _stream_ sockets too
    + simply initialize them with different _socket type_:

    ```python
    import socket

    # create a new stream socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ```
    + `AF_INET` specifies the _address family_ (IPv4)
    + `SOCK_STREAM` specifies the _socket type_ (stream)


{{% /section %}}

---

{{% import path="reusable/back.md" %}}
