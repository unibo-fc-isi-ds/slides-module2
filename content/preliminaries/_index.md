+++

title = "[DS] Preliminaries"
description = "Preliminaries about Distributed Systems Engineering"
outputs = ["Reveal"]
aliases = [
    "/preliminaries/"
]

+++

# Preliminaries about Distributed Systems Engineering

{{% import path="reusable/footer.md" %}}

---

{{%section%}}

# What is a Distributed System?

---

### Leslie Lamport (1987)

> A distributed system is one in which the failure of a computer you didn’t even know existed can render your own computer unusable

### __Interpretation__

This humorous yet insightful definition highlights one of the main challenges in distributed systems—hidden interdependencies between machines and how a failure in one part of the system can have unforeseen consequences elsewhere.

---

### Andrew S. Tanenbaum (2002)

> A distributed system is a collection of independent computers that appears to its users as a single coherent system

### __Interpretation__

This definition emphasizes the illusion of a unified system despite the fact that it is made up of multiple independent machines.

The key idea is that users should not be aware that the system is distributed.

---

### Coulouris, Dollimore, and Kindberg (2005)

> A distributed system is one in which components located at networked computers communicate and coordinate their actions only by passing messages.

### __Interpretation__

This definition focuses on the communication and coordination aspect of distributed systems, particularly the reliance on message passing across a network to achieve collaboration among independent components.

---

### George Coulouris (2001)

> A distributed system is a system in which hardware or software components located at networked computers communicate and coordinate their actions by passing messages.

### __Interpretation__

This expands the idea of distributed systems to both hardware and software components, emphasizing the key role of communication over a network.

---

### Peter Van Roy (2009)

> A distributed system is a system that consists of a collection of independent computers that appear to the users of the system as a single coherent system.

### __Interpretation__

This builds on Tanenbaum’s definition, stressing the coherence and illusion of a single system, despite its distributed nature across many independent computers.

{{%/section%}}

---

## What is a Distributed System?

### Wrap up

These definitions cover the essential characteristics of distributed systems:
- independent components,
- communication via messages, and the
- challenge of presenting a unified system to the user,
- despite failures or complexities within the system.

---

{{%section%}}

## Why would you make your system distributed?

- __Scalability__: Handling large-scale systems efficiently
- __Fault Tolerance__ and __Availability__: Ensuring reliability despite failures
- __Low Latency__ and __Geographical Distribution__: Providing better user experience across the globe
- __Resource Sharing__: Efficiently using computing power and storage
- __Handling Big Data__: Processing data locally rather than moving it
- __Parallelism__: Speeding up tasks through concurrent execution
- __Cost Efficiency__: Reducing infrastructure costs through resource pooling
- __Collaboration__: Enabling real-time updates and interactions across distances
- _The functionality to be provided_ by the system simply **implies** _distribution_

---

## Example: Google Search

- __Scalability__: Google handles billions of searches every day
- __Fault Tolerance__ and __Availability__: A single server cannot handle such a massive amount of data
- __Low Latency__ and __Geographical Distribution__: By distributing the search process across thousands of servers worldwide, Google can deliver search results quickly and reliably
- __Parallelism__: Processing multiple search queries concurrently

---

## Example: Social Networks (e.g., Instagram) or Messaging Apps (e.g., WhatsApp)

- __Scalability__: Millions of users are active at the same time
- __Fault Tolerance__ and __Availability__: A single server cannot handle such a massive amount of data
- __Low Latency__ : By distributing the service across multiple servers worldwide, the app can deliver messages quickly and reliably
- __Geographical Distribution__: Users can communicate across the globe
- __Handling Big Data__: Store users' data within that user's region (as per GDPR)
- __Parallelism__: Processing multiple messages concurrently
- __Collaboration__: Enabling real-time updates and interactions across distances
- The functionality is __inherently distributed__

---

## Example: Online Shopping (e.g., Amazon)

- __Scalability__: Millions of users are active at the same time
- __Fault Tolerance__ and __Availability__: A single server cannot handle such a massive amount of data
- __Low Latency__: By distributing the service across multiple servers worldwide, the app can deliver messages quickly and reliably
- __Geographical Distribution__: Comply to local regulations and regional preferences, e.g., language, currency, etc.
- __Parallelism__: Processing multiple orders concurrently
- _The functionality to be provided_ by the system simply **implies** _distribution_

---

## Example: Online Gaming (e.g., LoL, Fortnite)

- __Scalability__: Millions of users are active at the same time
- __Fault Tolerance__ and __Availability__: A single server cannot handle such a massive amount of data
- __Low Latency__: By distributing the service across multiple servers worldwide, the app can deliver messages quickly and reliably
- __Geographical Distribution__: Users can play with others across the globe
- __Parallelism__: Processing multiple games concurrently
- __Collaboration__: Enabling real-time updates and interactions across distances
- _The functionality to be provided_ by the system simply **implies** _distribution_

---

## Example: Google Docs (et. similia)

- __Scalability__: allows for different business models, e.g., subscription-based
- __Fault Tolerance__ and __Availability__: Allows for automatic, implicit updates / file saves / backups
- __Geographical Distribution__: Simplified sharing and collaboration across the globe
- __Parallelism__ and __Collaboration__: Multiple users can edit the same document concurrently

---

## Example: Federated Learning (e.g. [Google's Gboard](https://support.google.com/gboard/answer/12373137?hl=en))

- __Scalability__: Improve learning for all users (while keeping their data private)
- __Geo-Distribution__: Improve the functionality based on the data from different regions
- __Handling Big Data__: Process data locally rather than moving it
- __Parallelism__: Learning occurs on the user's device, anywhere, at any time
- __Cost Efficiency__: A single device would not be sufficient to process all the data
- __Resource Sharing__: Efficiently using computing power and storage, while preserving privacy

{{%/section%}}

---

{{%section%}}

# How does the SE workflow change for distributed systems?

---

## Recap: Software Engineering Workflow

1. __Use case collection__: _negotiate_ expectations with customer(s) or stakeholders

1. __Requirements analysis__: produce a list of _requirements_ the final product should satisfy
    + with _acceptance criteria_ for each requirement

1. __Design__: produce a _blueprint_ of the software
    + __modelling__: what entities from the _real world_ are represented in the software?
        * how do they _behave_? how do they _interact_?

1. __Implementation__: write the _code_ that reifies the _design_ into software

1. __Verification__: verify that the software _meets_ the _requirements_
    + __automated__ _testing_: write more code to check whether the aforementioned implementation code works
    + __acceptance__ _testing_: test the system with _real_ data and _real_ users

1. __Release__: make one particular _version_ of the software _available_ to the _customers_

1. __Deployment__: install and activate the software for the software

1. __Documentation__: produce _manuals_ and _guides_ for the software

1. __Maintenance__: fix _bugs_, _improve_ the software, _adapt_ it to _new_ requirements

---

## Software Engineering Workflow for _Distributed Systems_

(only additional steps are listed)

1. __Use case collection__:
    - _where_ are the users?
    - _when_ and _how frequently_ do they interact with the system?
    - _how_ do they _interact_ with the system? which _devices_ are they using?
    - does the system need to _store_ user's __data__? _which_? _where_?
    - most likely, there will be _multiple_ __roles__

---

## Software Engineering Workflow for _Distributed Systems_

2. __Requirements analysis__:
    - most likely, answers to the questions above imply __technical constrains__ on the system
        * e.g. where to store data?
            + in case of multiple data centers, how to keep them consistent?
    - will the system need to _scale_? how to handle _faults_? _how_ will it _recover_?
    - _acceptance criteria_ will for all such additional requirements/constraints

---

## Software Engineering Workflow for _Distributed Systems_

3. __Design__:
    - are there _infrastructural components_ that need to be introduced? _how many_?
        * e.g. _clients_, _servers_, _load balancers_, _caches_, _databases_, _message brokers_, _queues_, _workers_, _proxies_, _firewalls_, _CDNs_, _etc._
    - how do components	_distribute_ over the network? _where_?
        * e.g. what are the IP addresses of the servers / brokers / databases / etc.?
    - how do _domain entities_ __map to__ _infrastructural components_?
        * e.g. state of a video game on central server, while inputs/representations on clients
        * e.g. where to store messages in an IM app? for how long?
    - how do components _communicate_? _what_? _which_ __interaction patterns__ do they enact?
    - do components need to store data? _what data_? _where_? _when_? _how many **copies**_?
        * in case of network partition, should the system be _available_ or _consistent_?
    - how do components _find_ each other?
        * how to _name_ components?
        * e.g. _service discovery_, _load balancing_, _etc._
    - _how_ do components _recognize_ each other?
        * e.g. _authentication_, _authorization_, _etc._
    - what should happen when a component _fails_? is it _really_ a failure?
        * e.g. _retries_, _back-off_, _graceful degradation_, _etc._

---

## Software Engineering Workflow for _Distributed Systems_

4. __Implementation__:
    - which __network protocols__ to use?
        * e.g. UDP, TCP, HTTP, WebSockets, gRPC, XMPP, AMQP, MQTT, etc.
    - how should _in-transit data_ be __represented__?
        * e.g. JSON, XML, YAML, Protocol Buffers, etc.
    - how should _persistent data_ be __stored__?
        * e.g. relations, documents, key-value, graph, etc.
    - how should _databases_ be __queried__?
        * e.g. SQL, NoSQL, etc.
    - how should components be _authenticated_?
        * e.g. OAuth, JWT, etc.
    - how should components be _authorized_?
        * e.g. RBAC, ABAC, etc.

---

## Software Engineering Workflow for _Distributed Systems_

5. __Verification__:
    - how to **_unit_-test** distributed components?
    - testing the _integration_ among components is _paramount_
    - how to **_end-to-end_-test** the system?
        * e.g. production vs. test environment
    - _deployment_ __automation__ is commonly used to _test_ the system in _production-like_ environment

---

## Software Engineering Workflow for _Distributed Systems_

6. __Release__:
    - components may (and should) have their __own__ _release cycles_ and _versions_
    - components should be _resilient_ to the __coexistence__ of _multiple_ versions
    - _rolling_ __updates__ are _preferred_ over _big bang_ updates

---

## Software Engineering Workflow for _Distributed Systems_

7. __Deployment__:
    - _where_ to deploy components?
        * e.g. _cloud_, _on-premises_, _hybrid_?
    - _how_ to deploy components?
        * e.g. _containers_, _VMs_, _bare metal_?
    - _how_ to _scale_ components?
        * e.g. _horizontally_, _vertically_, _auto-scaling_?
    - _how_ to _monitor_ components?
        * e.g. _logs_, _metrics_, _traces_?
    - _how_ to _secure_ components?
        * e.g. _firewalls_, _encryption_, _certificates_, _etc._
    - all such aspects should be _automated_
        * tools and companies exist just for this!

---

## Software Engineering Workflow for _Distributed Systems_

8. __Documentation__:
    - protocols and data formats should be _well-documented_
        * allowing for third-parties to create _compatible_ components
    - e.g. _Web API_ specification is public for most Web services

---

## Software Engineering Workflow for _Distributed Systems_

9. __Maintenance__:
    - continuous __monitoring__ of _performance_ and _availability_
        * tools and companies exist just for this!
    - _issues tracking_ is non-trivial (may require ad-hoc sub-systems)
    - _sunsetting_ old versions is _crucial_ $\rightarrow$ _coexistence_ of multiple versions
        * __End-of-Life__ should be _scheduled_, not _abrupt_

{{%/section%}}

---

# Nomenclature

---

## Infrastructure

- Andrew S. Tanenbaum and Maarten Van Steen - “Distributed Systems: Principles and Paradigms” (2007):
> The infrastructure of a distributed system comprises the communication mechanisms, middleware, and platforms that allow components, located on different networked computers, to communicate and coordinate their actions.

- Coulouris, Dollimore, Kindberg - “Distributed Systems: Concepts and Design” (2011):
> Infrastructure in a distributed system refers to the underlying hardware, software services, and networks that facilitate the integration, execution, and management of distributed components.

- Peter Van Roy - “Concepts, Techniques, and Models of Computer Programming” (2004):
> In distributed systems, infrastructure is the ensemble of hardware and software that provides the necessary support for computation and communication across a network of independent, interacting components.

---

{{%section%}}

## Infrastructural Components

> An infrastructural component consists of a software unit — most commonly a process — playing a precise role in the distributed system.
> The role depends on the purpose of the component in the system, and/or how it interacts.

### Examples

clients, servers, brokers, load balancers, caches, databases, queues, masters, workers, proxies, etc.

---

## Synonyms

- __Node__ $\equiv$ an infrastructural component for which the _role_ is __not__ relevant

- __Peer__ $\equiv$ an infrastructural component for which the _role_ is __not__ specified
    * because all components play the same role(s)

---

## Clients and servers

![Clients and server concept](./client-server.png)

- __Server__ $\equiv$ a component with a _well-known name_/address _responding_ to _requests_ coming from clients
    * it's the components that _listens_ (waits) for remote requests
    * commonly it exposes an _interface_ ($\approx$ the requests it can answer to) to _clients_

- __Client__ $\equiv$ a component that sends _requests_ to servers, waiting for _responses_
    * it's the components that _initiates_ the interaction
    * it may expose an _interface_ to _users_ on how to _interact_ with the server

---

## Proxy

{{< image src="./proxy.png" height="50vh" >}}

<br>

- __Proxy__ $\equiv$ a server acting as a _gateway_ towards another server
    * it _intercepts_ requests from clients and forwards them to the actual server
    * it _intercepts_ responses from the actual server and forwards them to the client
    * it may _cache_ responses to _reduce_ the _load_ on the server

- A _proxy_ performing _caching_ is called a _cache server_ (or just _cache_)

---

## Load Balancer

{{< image src="./load-balancer.png" height="60vh" alt="Load Balancer concept" >}}

- __Load Balancer__ $\equiv$ a proxy _distributing_ incoming requests among multiple servers
    * according to some _distribution policy_:
        + _round-robin_,
        + _least connections_,
        + _least response time_,
        + etc.

---

## Broker

![Broker concept](./broker.png)

- __Broker__ $\equiv$ a server _mediating_ the _communication_ between _producers_ and _consumers_ of data (a.k.a. messages)
    * it _receives_ messages from producers and _forwards_ them to (1 or more) consumers
    * common assumption: consumers _declare_ their interest in receiving messages

- __Producer__ $\equiv$ the component _sending_ messages to _producer(s)_ (via the broker)

- __Consumer__ $\equiv$ the component _receiving_ messages from _consumer(s)_ (via the broker)

- The same component can be simultaneously a _producer_ and a _consumer_

---

## \[Broker with\] Queues

![Queue concept](./queue.jpg)

- __Queue__ $\approx$ a data structure where messages are _stored_ in a _FIFO_ manner
    * FIFO storage $\rightarrow$ messages are consumed in the order they were produced
    * storage $\rightarrow$ messages are _not_ lost if consumers are _unavailable_

---

## Message oriented middleware (MOM)

![MOM concept](./mom.png)

- __MOM__ $\approx$ a sort of broker having multiple channels for messages
    * messages involving the same _topic_ are sent to the same _channel_
    * consumers subscribe to _channels_

- __Topic__ $\equiv$ a _label_ for messages, allowing
    * producers to control which _consumers_ receive the message
    * consumers to _filter_ messages they are interested in
    * the broker to _route_ messages to the correct consumers

- Yes, most MOM technologies use queues to implement channels

---

## Database

![Database concept](./three-tier.webp)

- __Database__ $\equiv$ a server specialized in _storing_ and _retrieving_ data
    * in three-tier architectures, the database is the _third_ tier
        + acting as a server for the server (which acts as a client w.r.t the database)

---

## Master—Worker (a.k.a. Master—Slave, or Leader—Follower)

![Master—Worker concept](./master-worker.png)

- __Master__ $\equiv$ a server _coordinating_ the _work_ of multiple workers
    * it _distributes_ the work among workers
    * it _collects_ the results from workers

- __Worker__ $\equiv$ a server _executing_ the _work_ assigned by the master

- Common use cases:
    - \[master—worker\] _parallel_ computation
    - \[master—slave\] _replication_ of data

{{%/section%}}

---

{{%section%}}

## Interaction Patterns

> An __interaction pattern__ describes how different _components_ (nodes, processes, etc.) _communicate_ and _coordinate_ their actions to achieve a common goal.
> These patterns define the _flow of messages_, _responsibilities_ of __participants__, and the _timing_ and _sequencing_ of __communications__.

e.g. _request-response_, _publish-subscribe_, _auction_, _etc.

### Key points

- __Participants__: we assume that there are _$N \geq 2$_ participants
- __Roles__: participants play _well-defined_ roles, most commonly:
    * __initiator__: the participant _initiating_ the interaction
    * __responder__: the participant _waiting_ for _some other participant_ to initiate the interaction
- __Messages__: information _exchanged_ among participants, most commonly containing at least:
    * __payload__: the actual content of the message
    * __metadata__: information _about_ the message, e.g. _source_, _destination_, _timestamp_, _conversation id_, etc.

---

## How to represent Interaction Patterns?

1. __Sequence diagrams__: _visual_ representation of the _flow_ of messages between participants
    * _time_ is _vertical_, _participants_ are _horizontal_
    * _arrows_ represent _messages_ sent from one participant to another
    * _lifelines_ represent the _lifetime_ of a participant

![Example of a Sequence Diagram](./diagram-sequence.png)

### Hints

- see explanation at <https://www.uml-diagrams.org/sequence-diagrams.html>
- use [PlantUML](https://plantuml.com/sequence-diagram) to _automatically_ generate sequence diagrams from textual descriptions
    + many Web-based picture generators, e.g. [http://www.plantuml.com/plantuml](http://www.plantuml.com/plantuml/uml/SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd9vt98pKi1IW80)

---

## How to represent Interaction Patterns?

2. __Message flow graphs__: _visual_ representation of the _flow_ of messages
    * each _node_ represents a __type__ of _message_ (e.g. _request_, _response_, _notification_, etc.)
    * each _directed edge_ represents an admissible _reply_ to a _message_
    * the graph may contain _cycles_, if the pattern allows for _repeated_ interactions, or _resets_
    * nodes may be represented in different colours/shapes depending on which _role_ sends/receives the message

{{< image src="./user-agent-protocol.svg" width="65vw" link="https://link.springer.com/chapter/10.1007/978-3-031-40878-6_3" >}}

### Hints

- in _OO programming languages_, each message type can be represented as a _class_
- you may use class diagrams (e.g. in [PlantUML](https://plantuml.com/class-diagram)) to represent them
- you may also depict the graph otherwise, via graph-drawing tools (e.g. [Graphviz](https://graphviz.org/) or [yEd](https://www.yworks.com/products/yed))

---

## How to represent Interaction Patterns?

3. __State diagrams (a.k.a. state machines)__: _visual_ representation of the _internal state transitions_ of a participant
    * each _state_ represents a _condition_ of the participant (e.g. before/after a message is sent/received)
    * each _transition_ represents an _event_ that _changes_ the _state_ of the participant
        + most commonly, a message _reception_ or _sending_
    * _initial_ and _final_ states are _special_ states representing the _start_ and _end_ of the interaction
    * most commonly, there's _one state diagram per participant_

{{% multicol %}}
{{% col %}}
{{< image src="./user-state-diagram.svg" width="40vw" link="https://link.springer.com/chapter/10.1007/978-3-031-40878-6_3" >}}
{{% /col %}}
{{% col %}}
{{< image src="./agent-state-diagram.svg" width="40vw" link="https://link.springer.com/chapter/10.1007/978-3-031-40878-6_3" >}}
{{% /col %}}
{{% /multicol %}}

### Hints

- use [PlantUML](https://plantuml.com/state-diagram) to _automatically_ generate state diagrams from textual descriptions

---

## Which representation to use?

- The three representations are _complementary_
- So you should use them _together_ to _fully_ describe an interaction pattern

<br>

### Further representations may be welcome

1. FIPA's _AUML_ (Agent UML) for agent-based systems
    * see <http://www.fipa.org/docs/input/f-in-00077/f-in-00077.pdf>
1. _BPMN_ (Business Process Model and Notation) for _business_ processes
    * see <https://en.wikipedia.org/wiki/Business_Process_Model_and_Notation>
1. UML's _Activity Diagrams_
    * see <https://www.uml-diagrams.org/activity-diagrams.html>

---

## Common Interaction Protocols (pt. 1)

### Request—Response

The most common and basic pattern for communication between two components

{{% multicol %}}
{{% col %}}
{{% plantuml %}}
hide footbox
participant Client
participant Server


Client -> Server: Request
Server -> Client: Response
{{% /plantuml %}}
{{% /col %}}
{{% col %}}
- 2 roles: __client__ and __server__
- 2 sorts of messages: __request__ and __response__
- __each__ _request_ is _followed_ by __one__ _response_
- _client_ is the __initiator__, _server_ is the __responder__
- _client_ __sends__ the _request_, _server_ __sends__ the _response_
- _client_ __waits__ for the _response_, _server_ __waits__ for the _request_
- often used to realise:
    + _remote procedure calls_ (RPC)
    + _remote method invocations_ (RMI)
    + (web) _services_

{{% /col %}}
{{% /multicol %}}

---

## Common Interaction Protocols (pt. 2)

### Publish—Subscribe

A simple pattern to spread information among multiple recipients

{{% multicol %}}
{{% col %}}
{{% plantuml %}}
hide footbox
actor User
participant Publisher
participant Subscriber1
participant Subscriber2

== Subscription Phase ==
Subscriber1 -> Publisher: subscribe
activate Publisher
Publisher --> Subscriber1: confirmation
deactivate Publisher

Subscriber2 -> Publisher: subscribe
activate Publisher
Publisher --> Subscriber2: confirmation
deactivate Publisher

== Notification Phase ==
User --> Publisher: Event
activate Publisher
Publisher -> Subscriber1: notify Message
Publisher -> Subscriber2: notify Message
deactivate Publisher
{{% /plantuml %}}
{{% /col %}}
{{% col %}}
- 2 roles: __publisher__ and __subscriber__
- 2 sorts of messages: __subscribe__ and __notify__
- 2 _phases_ of interaction: __subscription__ and __notification__
    1. __Subscription__ phase: _subscribers_ __declare__ their _interest_ in _receiving_ message
        * subscribers are _initiators_ here
    2. __Notification__ phase: _publishers_ __send__ messages to _subscribers_
        * messages are _broadcasted_ or _multicasted_ depending on the implementation
- messages of type _notify_ carry __messages__, commonly representing events
- messages of type _subscribe_ may carry __topics__, commonly representing the topic of interest (for the subscriber)
- notice that subscription is, essentially, a _request-response_ pattern
{{% /col %}}
{{% /multicol %}}

---

## Common Interaction Protocols (pt. 2)

### Publish—Subscribe with Broker

Notice that the publisher here is acting as a __broker__
* one may re-design the pattern with _explicit_ broker
* this is commonly useful to _decouple_ the _publisher_ from the _subscribers_
* most commonly, brokers _store_ messages until they are _consumed_

{{% plantuml height="50vh" %}}
hide footbox
actor User
participant Publisher
participant Broker
participant Subscriber1
participant Subscriber2
participant Subscriber3

== Subscription Phase ==
Subscriber1 -> Broker: subscribe TopicA
activate Broker
Broker --> Subscriber1: confirmation
deactivate Broker

Subscriber2 -> Broker: subscribe TopicA
activate Broker
Broker --> Subscriber2: confirmation
deactivate Broker

Subscriber3 -> Broker: subscribe TopicB
activate Broker
Broker --> Subscriber3: confirmation
deactivate Broker

== Notification Phase ==
User --> Publisher: Event
activate Publisher
Publisher -> Broker: publish Message\non TopicA
deactivate Publisher
activate Broker
Broker -> Subscriber1: notify Message
Broker -> Subscriber2: notify Message
deactivate Broker
{{% /plantuml %}}

---

## Common Interaction Protocols (pt. 2)

### Unicast vs. Broadcast vs. Multicast

{{< image src="./cast.png" width="60vw" alt="Depiction of the three types of communication" >}}

<br/>

- __Unicast__: _one-to-one_ communication
- __Broadcast__: _one-to-all_ communication
- __Multicast__: _one-to-many_ communication
    * implies a _selection criterion_ for the _many_

---

## Common Interaction Protocols (pt. 3)

### ContractNet Protocol

A simple protocol for _auctions_ and _negotiations_

{{% multicol %}}
{{% col %}}
{{% plantuml %}}
hide footbox
participant Initiator
participant Contractor1
participant Contractor2

== Call for Proposals ==
Initiator -> Contractor1: Call for Proposal (CFP)
activate Initiator
Initiator -> Contractor2: Call for Proposal (CFP)

== Proposal Submission ==
Contractor1 -> Initiator: Submit Proposal
Contractor2 -> Initiator: Submit Proposal

== Proposal Evaluation ==
Initiator -> Initiator: Evaluate Proposals, choosing the best one

== Award Contract ==
Initiator -> Contractor1: Award Contract
activate Contractor1
Contractor1 -> Initiator: Accept Contract

== Contract Execution ==
Contractor1 -> Initiator: Return Result
deactivate Contractor1
deactivate Initiator
{{% /plantuml %}}
{{% /col %}}
{{% col %}}
- 2 roles: __initiator__ and __contractor__
- 5 sorts of messages: __CFP__, __proposal__, __award__, __accept__, __result__
- 4 _phases_ of interaction:
    1. __Call for Proposals__: _initiator_ broad- or multi-casts a _request_ a CFP
        + commonly defining a _deadline_ + _task request_
    2. __Proposal Submission__: _contractors_ __submit__ proposals to _initiator_
        + commonly containing _estimated cost_
    3. __Proposal Evaluation__: _initiator_ __evaluates__ proposals and __chooses__ the best one
    4. __Award Contract__: _initiator_ __awards__ the contract to the chosen contractor
        + the chosen contractor __accepts__ the contract
    5. __Contract Execution__: _contractor_ __executes__ the contract and __returns__ the result

- not shown in the picture:
    1. lack of proposals (i.e. no contractor)
    2. no proposal chosen
    3. _contractor_ may _reject_ the contract

{{% /col %}}
{{% /multicol %}}

---

## Common Interaction Protocols (pt. 4)

### Foundation for Intelligent Physical Agents (FIPA)

- FIPA is a _standardization_ body for _agent-based_ systems
- **Very** rough analogy: _agent_ $\approx$ distributed _component_ in a distributed system
- FIPA has _standardized_ many _interaction protocols_ for agents
    * e.g. _contract net_, _request-response_, _subscription_, _auction_, _etc.
- See <http://www.fipa.org/repository/ips.php3>

{{%/section%}}

---

{{% section %}}

# Architecture and Architectural Styles

(recall theory from Module 1's {{< module1-m6 >}})

---

## Recap: Software Architecture vs. Architectural Style

- Roy Fielding (2000):
> A __software architecture__ is an abstraction of the run-time elements of a software system during some phase of its operation.
> [...]
> It is defined by a _configuration_ of __architectural elements__ constrained in their relationships in order to achieve a desired set of _architectural properties_.


- Very roughly:
> __Architectural style__ $\approx$ _patterns_ of architectures which are known to work in practice

### Main architectural styles for distributed systems

* _layered_ architectures
* _object-based_ architectures
* _event-based_ architectures
* _shared data-space_ architectures

---

## Architectural Styles in Practice (pt. 1)

### Layered Architecture (concept)

{{% multicol %}}
{{% col %}}
{{< image src="./architecture-layered.png" alt="Layered Architecture" >}}
{{% /col %}}
{{% col %}}
+ Which __infrastructural components__?
    - Each layer is a __server__ (or a _proxy_) for the layer(s) _above_ it
    - Each layer is a __client__ for the layer(s) _below_ it

+ Which __interaction patterns__?
    - _Request—Response_: (a.k.a. remote procedure call, RPC)
        * _upper_ layers issue __requests__ to _lower_ layers
        * _lower_ layers issue __responses__ to _upper_ layers
    - sometimes, _Publish—Subscribe_:
        * _upper_ layers _subscribe_ to _lower_ layers
        * _lower_ layers _notify_ _upper_ layers

+ Constraints:
    - _no cycles_ among layers
        * i.e. _lower_ layers_ should not contact _upper_ layers

+ Example: (Web Services)
    - [Skyscanner](https://www.skyscanner.net) (looks for flights / hotels)
        * relying on the Web services of airlines / hotels
        * relying on the [Booking](https://www.booking.com) portal
            + all of which have their own _layered_ architecture
{{% /col %}}
{{% /multicol %}}

---

## Architectural Styles in Practice (pt. 1)

### Layered Architecture (particular cases)

#### Three-Tier Architecture

{{< image src="./three-tier.webp" alt="Classic three-tier application architecture" >}}

- __Presentation Tier__: responsible for _presenting_ information to the _user_, and _accepting_ user _input_
- __Application Tier__: responsible for _processing_ user _requests_, and _executing_ business _logic_, __updating system state__
- __Data Tier__: responsible for _storing_ and _retrieving_ data, and _managing_ data _access_, __persisting system state__

---

## Architectural Styles in Practice (pt. 1)

### Layered Architecture (particular cases)

#### Hexagoal Architecture

{{< image src="./architecture-hexagonal.png" alt="Hexagonal Architecture" >}}

cf. <https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)>

---

## Architectural Styles in Practice (pt. 1)

### Layered Architecture (analysis)

#### Pros

1. **Separation of Concerns**: each layer handles a specific responsibility, making the system easier to understand and maintain.

2. **Modularity**: layers are independent, allowing easier updates, testing, and replacement without affecting the entire system.

3. **Reusability**: common functionality in layers can be reused across different systems or projects.

4. **Scalability**: the system can scale by modifying or optimizing individual layers (e.g., scaling the database or network layer independently).

5. **Maintainability**: bugs or issues can be isolated to specific layers, making troubleshooting simpler.

6. **Abstraction**: layers provide clear abstractions, allowing higher layers to interact with the system without needing to know the internal details of lower layers.

7. **Interoperability**: a well-defined interface between layers promotes compatibility and enables the use of different technologies in each layer.

---

## Architectural Styles in Practice (pt. 1)

### Layered Architecture (analysis)

#### Cons

1. **Performance Overhead**: multiple layers can introduce latency, especially if there are excessive data transformations or processing between layers.

2. **Complexity in Design**: designing and managing multiple layers can increase overall system complexity, particularly in very large systems.

3. **Rigid Structure**: strict layer separation can limit flexibility, making it harder to implement cross-cutting concerns (e.g., logging, security) efficiently.

4. **Duplication of Functionality**: if layers are not carefully defined, functionality can be duplicated across layers, leading to inefficiencies.

5. **Potential for Over-Engineering**: in smaller or simpler systems, using a layered architecture might introduce unnecessary complexity when simpler architectures would suffice.

6. **Difficulty in Layer Communication**: strict adherence to layer boundaries might make certain interactions cumbersome, requiring unnecessary intermediate steps.

---

## Architectural Styles in Practice (pt. 1)

### Layered Architecture (analysis)

#### Personal Opinion of the Teacher

- _Layered_ architectures are _simple_ and _easy_ to _understand_
- It works well in most cases, you can consider it the _default_ choice
- Prefer:
    1. _two-tier_ (3-tier with no real DBMS) architectures for _quick and dirty_ systems
    2. _three-tier_ architectures for if _flexibility_ is not a primary concern
    3. _hexagonal_ architectures for systems that may need to _scale_ in _complexity_

---

## Architectural Styles in Practice (pt. 2)

### Object-Based Architecture (concept)

{{% multicol %}}
{{% col %}}
{{< image src="./architecture-objectbased.png" alt="Object-Based Architecture" >}}
{{% /col %}}
{{% col %}}
+ Which __infrastructural components__?
    - each is object simultaneously a __client__ and a __server__ for other objects

+ Which __interaction patterns__?
    - _Request—Response_: (a.k.a. remote method invocation, RMI)
        * _objects_ issue __requests__ to _other objects_
        * _other objects_ __respond__

+ Constraints:
    - basically none

+ Examples:
    - [Microsoft Component Object Model](https://en.wikipedia.org/wiki/Component_Object_Model) COM
    - [Java RMI](https://docs.oracle.com/javase/8/docs/technotes/guides/rmi/hello/hello-world.html)
    - [Common Object Request Broker Architecture](https://en.wikipedia.org/wiki/Common_Object_Request_Broker_Architecture) (CORBA)

{{% /col %}}
{{% /multicol %}}

---

## Architectural Styles in Practice (pt. 2)

### Object-Based Architecture (analysis)

#### Pros

1. **Encapsulation**: objects encapsulate data and behaviour, making the system more modular and easier to maintain.

2. **Reusability**: objects can be reused across different parts of the system or in different applications, reducing duplication of code.

3. **Modularity**: components are independent and self-contained, allowing easier upgrades, testing, and maintenance.

4. **Clear Interface Definition**: objects interact through well-defined interfaces, making it easier to manage dependencies and interactions between components.

5. **Flexibility**: objects can be distributed across different nodes, enabling flexibility in deployment and scalability in a distributed system.

6. **Language Agnosticism** (e.g., CORBA): some object-based systems (like CORBA) support multi-language environments, allowing developers to use the best language for each component while maintaining system integration.

7. **Dynamic Behaviour**: objects can be created, modified, or destroyed dynamically, allowing more flexible and adaptive systems.

---

## Architectural Styles in Practice (pt. 2)

### Object-Based Architecture (analysis)

#### Cons

1. **Performance Overhead**: the communication between distributed objects, especially over a network, can introduce significant latency and performance overhead.

2. **Complexity in Management**: managing the lifecycle and communication of distributed objects can add complexity, particularly in handling object references, synchronization, and failure recovery.

3. **Difficulty in Debugging**: debugging distributed objects is more complex due to the separation between client and server objects, especially when communication spans across different networks or systems.

4. **Scalability Limitations**: while object-based systems are modular, they may not scale efficiently in very large systems due to the overhead of managing object communication and state.

5. **Security Concerns**: distributed objects expose interfaces that can be exploited if not secured properly, making security management more challenging.

6. **Tight Coupling through Interfaces**: objects often rely on specific interfaces, which can lead to tight coupling between components, reducing flexibility in modifying or replacing objects.

7. **State Management**: maintaining the state of distributed objects can be complex, especially in cases of network failures or when objects need to be synchronized across multiple nodes.

---

## Architectural Styles in Practice (pt. 2)

### Object-Based Architecture (analysis)

#### Personal Opinion of the Teacher

- _Object-based_ architectures were a thing in the 90s and early 2000s
- They never really took off, and are now mostly _legacy_
- OOP is good for developing individual _components_, where objects share the same _address space_
- Inter-object _interactions_ are so _fine-grained_ and _intertwined_ in OOP that adding network in between makes it __unmanageable__
- Just __don't__ use this when designing a new system

---

## Architectural Styles in Practice (pt. 3)

### Event Based Architecture (concept)

{{% multicol %}}
{{% col %}}
{{< image src="./architecture-eventbased.png" alt="Event-Based Architecture" >}}
{{% /col %}}
{{% col %}}
+ Which __infrastructural components__?
    - ???

+ Which __interaction patterns__?
    - ???

+ Constraints:
    - ???

+ Examples:
    - ???
{{% /col %}}
{{% /multicol %}}

---

## Architectural Styles in Practice (pt. 4)

### Shared Dataspace Architecture (concept)

{{% multicol %}}
{{% col %}}
{{< image src="./architecture-shareddataspace.png" width="40vw" alt="Shared Dataspace Architecture" >}}
{{% /col %}}
{{% col %}}
+ Which __infrastructural components__?
    - ???

+ Which __interaction patterns__?
    - ???

+ Constraints:
    - ???

+ Examples:
    - ???
{{% /col %}}
{{% /multicol %}}

{{%/section%}}

---

## Other features you may want to consider

1. Replication
    - why? fault tolarance, load balancing, consistency, etc.

2. Federation

3. Partitioning

4. Sharding
