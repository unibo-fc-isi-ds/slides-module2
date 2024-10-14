
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
    1. [About the course](./) (this page)
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

# Professors

### Giovanni Ciatto
  * email: [`giovanni.ciatto@unibo.it`](mailto:giovanni.ciatto@unibo.it)
  * homepage: [`https://www.unibo.it/sitoweb/giovanni.ciatto/en`](https://www.unibo.it/sitoweb/giovanni.ciatto/en)
  * office hours: by appointment (send me an email)

### \[Tutor\] Matteo Magnini
    * email: [`matteo.magnini@unibo.it`](mailto:matteo.magnini@unibo.it)
    * homepage: [`https://www.unibo.it/sitoweb/matteo.magnini/en`](https://www.unibo.it/sitoweb/matteo.magnini/en)
    * office hours: by appointment (send me an email)

---

#### Prioritize the {{< forum_general >}}

#### [`https://virtuale.unibo.it/mod/forum/view.php?id=1678931`](https://virtuale.unibo.it/mod/forum/view.php?id=1678931)
  * All technical question
  * Any other non-personal question

<p>

#### When using the email
  * Include *all* teachers, **always**, there including prof. [Omicini](mailto:andrea.omicini@unibo.it)
  * Clarify the _academic year_ and the _name of the course_ in the subject

---

## Pages of the course

- [Institutional Page of the Course](https://www.unibo.it/it/studiare/dottorati-master-specializzazioni-e-altra-formazione/insegnamenti/insegnamento/2024/493397)
- [Virtuale Page of the Course]({{< vle_url >}})
      + please enroll if you didn't already
- [APICe Page of the Course](https://apice.unibo.it/xwiki/bin/view/Course/Ds2425/)
- [These slides](https://unibo-fc-isi-ds.github.io/slides-module2/)
- [Examples and Exercises Repository](https://github.com/unibo-fc-isi-ds/lab-snippets)
- [Python Programming 101](https://matteomagnini.github.io/distributed-systems-python-101/#/)

---

# Organization of Module 2

- Lectures in lab with immediate hands-on
- Exercises and examples in Python
    * submission of exercises [via GitHub](https://github.com/) via grant you extra points
- Final project work in any language of your choice

## Time table

* **Wednesday 15:00--17:00** (2h) --- Lab 3.1
    - cf. [official timetable](https://www.unibo.it/en/study/phd-professional-masters-specialisation-schools-and-other-programmes/course-unit-catalogue/course-unit/2024/493397/orariolezioni) for any change

Changes will be published on the {{< forum_news >}}

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

---

## Prerequisites

- Basic knowledge of Python (see [Python Programming 101](https://matteomagnini.github.io/distributed-systems-python-101/#/) if missing)
- Basic knowledge of Git (see [these slides](https://unibo-dtm-se.github.io/course-slides/dvcs-basics/#/) if missing)
- Basic knowledge of Linux shell (see [these slides](https://unibo-dtm-se.github.io/course-slides/preliminaries/#/) if missing)
- Basic understanding of computer networks, ISO/OSI model, TCP/IP stack

---

## Software Requirements

### Required
* A working internet connection
* A working Python 3.10+ installation

### Recommended

* PyCharm
* Visual Studio Code
* A decent Unix terminal