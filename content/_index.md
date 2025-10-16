
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

1. General aspects
    1. [About the course](./) (this page)
        - [Useful links](./#/links)
        - [Project work rules](./#/rules)
    1. [Preliminaries](./preliminaries/)
    1. [Communication mechanisms](./communication/)
        - Exercise: [TCP Group Chat](./communication/#/exercise-tcp-group-chat)
    1. [Presentation](./presentation/)
        - Exercise: [RPC-based Authentication Service](./presentation/#/exercise-rpc-auth-service)
        - Exercise: [Secure RPC-based Authentication Service](./presentation/#/exercise-rpc-auth-service-secure)
    <!-- 1. \[No time for this in A.Y. 24-25\] Testing [Testing](./testing/) -->

    <!-- [Miscellanea](./misc/) -->

1. [PONG](./pong/) case study
    1. [Game Loop](./pong/#/game-loop)
    1. [Game Model](./pong/#/model)
    1. [I/O](./pong/#/io)
    1. [Architecture](./pong/#/architecture)
    1. [Protocols](./pong/#/protocols)
    1. [Analysis](./pong/#/analysis)
        + Exercise: [Available Distributed Pong](./pong/#/exercise-available-dpongpy)

---

## Teachers

### Prof. Giovanni Ciatto
* email: [`giovanni.ciatto@unibo.it`](mailto:giovanni.ciatto@unibo.it)
* homepage: <https://www.unibo.it/sitoweb/giovanni.ciatto/en>
* office hours: by appointment (send me an email)

### Tutor Matteo Magnini
* email: [`matteo.magnini@unibo.it`](mailto:matteo.magnini@unibo.it)
* homepage: <https://www.unibo.it/sitoweb/matteo.magnini/en>
* office hours: by appointment (send me an email)

---

## Prioritize the {{< forum_general >}}

* All technical question
* Any other non-personal question

<p>

## When using the email
* Include *all* teachers in CC, **always**, there including prof. [Omicini](mailto:andrea.omicini@unibo.it)
* Clarify the _academic year_ and the _name of the course_ in the subject

---

{{< slide id="links" >}}

## Pages of the course

- [Institutional Page of the Course]({{< institutional_page_url >}})
- [Virtuale Page of the Course]({{< vle_url >}})
    + please enroll if you didn't already
- [APICe Page of the Course]({{< apice_url >}})
- [These slides](./)
- [Examples and Exercises Repository]({{< github-url repo="lab-snippets" >}})
- [Python Programming 101](https://matteomagnini.github.io/distributed-systems-python-101/#/)

---

## Organization of Module 2

- Lectures in lab with immediate _hands-on_
- Exercises and examples in Python
    * submission of _exercises_ [via GitHub](https://github.com/) may grant you _extra points_
- Final project work in any programming language of your choice
    * report must be in English and follow [this LaTeX template]({{% final_report_template %}})

---

## Time—table

* **Friday 9:00--11:00** (2h) --- Lab 3.1
    - cf. [official timetable]({{< institutional_page_url >}}/orariolezioni) for any change

Changes will be published on the {{< forum_news >}}

---

{{< slide id="rules" >}}

## Workflow for the project work (pt. 1)

> Detailed rules here: <{{% apice_url %}}Projects/Rules>

1. **Propose** your project idea on the {{< forum_projects >}}
    + 1-3 students per _group_
    + open a discussion thread named `[Surname1, Surname2, ...] Project Proposal: <your project name>`
    + please indicate:
        1. names and __email-addresses__ of the members of the group;
        2. the project _vision_, i.e. what you want to realise, eliciting the _functionalities_ of the envisioned system;
        3. a _motivation_ of why/how the project is letting you _explore_ the __topics of the course__ (e.g. consistency, fault-tolerance, etc);
        4. _which technologies_ (programming langues, libraries, technologies) you intend to use and _why_;
        5. which _deliverable(s)_ you intend to produce (application, library, presentation, etc), __aside from the final report__;
        6. some strict _temporal constraint_, if any (e.g., someone in the group is going to graduate soon)

2. Any _subsequent communication_ on the project should be done on the __same thread__
    + use the thread as a _backlog_ of any official communication concerning the administration of your project work
    + if you want to talk _privately_ about your project work, _mention the URL_ of your project's thread in your email

3. __Wait__ for the teachers to _approve_ your proposal
    + most likely, we'll try to estimate the effort and ask for changes if too much or too little
    + we'll also check for overlaps with other groups

--- 

## Workflow for the project work (pt. 2)

4. Create a __GitHub repository__ where to develop your project and post the URL onto your project's thread
    + make all the _members_ of the group collaborators on the repository
    + give _full admin_ rights to the teachers:
        - Usernames: [`gciatto`](https://github.com/gciatto), [`matteomagnini`](https://github.com/MatteoMagnini)

5. __Work__ on your project:
    + _commit_ and _push_ your changes often
        - only the `master` or `main` branch will be considered for the evaluation
    + in parallel, or later, write a _report_ about your report following [this LaTeX template]({{% final_report_template %}})

6. Once done, post a _message_ on your _project's thread_ to signal the end of the work
    + we'll _clone_ your repository and evaluate the code

7. __Edits__ may be requested by the teachers, to either the code or the report (or both)

8. Once the teachers are satisfied, you'll be requested to __present__ your work to prof. Omicini
    + after setting up a meeting with him, in private
    + 12-15 minutes _presentation_ + 5-10 minutes _Q&A_

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

* PyCharm OR _Visual Studio Code_
* A decent Unix terminal
    * prefer _Git Bash_ on Windows

---

# Lecture is Over

<br>

Compiled on: {{< today >}} --- [<i class="fa fa-print" aria-hidden="true"></i> printable version](?print-pdf&pdfSeparateFragments=false)

[<i class="fa fa-undo" aria-hidden="true"></i> back to ToC](./#/toc)
