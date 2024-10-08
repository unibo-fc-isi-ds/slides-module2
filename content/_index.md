
+++

title = "About the course"
description = "Presentation of the course 'Distributed Systems — Module 2'"
outputs = ["Reveal"]
aliases = [
    "/about/"
]

+++

{{% import path="reusable/front.md" %}}

---

{{< slide id="toc" >}}

## Table of Contents

* General aspects
    1. [About the course](./about/)
    1. [Preliminaries](./preliminaries/)
    1. [Communication mechanisms](./communication/)
        - Exercise: [TCP Group Chat](./communication/#/exercise-tcp-group-chat)
    1. [Presentation](./presentation/)
        - Exercise: [RPC-based Authentication Service](./presentation/#/exercise-rpc-auth-service)
        - Exercise: [Secure RPC-based Authentication Service](./presentation/#/exercise-rpc-auth-service-secure)
    1. \[Tentative\] Testing <!-- [Testing](./testing/) -->

    <!-- [Miscellanea](./misc/) -->

* Case Studies
    - [PONG](./pong/)
        1. [Game Loop](./pong/#/game-loop)
        1. [Game Model](./pong/#/model)
        1. [I/O](./pong/#/io)
        1. [Architecture](./pong/#/architecture)
        1. [Protocols](./pong/#/protocols)
        1. [Analysis](./pong/#/analysis)

---

## Goals

- Teach you how to __design__ and __develop__ Distributed Systems, in practice...
- ... via a _running example_ (namely, distributed [Pong](https://en.wikipedia.org/wiki/Pong))
- Give you a _reference_ for developing your final __project work__

---

## Topics

- Distributed __architectures__ and __protocols__
- Communication __mechanisms__ (TCP / UDP _sockets_)
- _Presentation_ (__serialization__ and __deseralization__)
- __Issues__ of distributed systems programming
- \[Hopefully\] __Testing__ distributed systems
- \[Hopefully\] Overview on distributed programming __frameworks__ / __libraries__
