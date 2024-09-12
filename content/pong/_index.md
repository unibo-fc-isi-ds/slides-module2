
+++

title = "Distributed Pong"
description = "A running example for 'Distributed Systems — Module 2', based on the classic game Pong"
outputs = ["Reveal"]
aliases = [
    "/pong/"
]

+++

# Distributed Pong

{{% import path="reusable/footer.md" %}}

---

## What's Pong?

<https://en.wikipedia.org/wiki/Pong>

![Pong screenshot](https://upload.wikimedia.org/wikipedia/commons/6/62/Pong_Game_Test2.gif)

---

## Goal

In this running example we are going to

- implement a __distributed__ version of the classic game Pong
- in [Python](https://www.python.org)
- using [PyGame](https://www.pygame.org)

in order to exemplify the _development_ of a distributed system _project_.

---

## What is PyGame?

- **PyGame** is a popular Python library for writing simple games

- It handles many game development tasks, such as _graphics_, _sound_, _time_, and _input management_.

- Simple to use, yet powerful enough to create non-trivial games

- Lightweight, portable, and easy to install
    + `pip install pygame` (better to use a virtual environment)


---

{{%section%}}

## Preliminaries

# The Game Loop

---

## What is a Game Loop?

- A **game loop** is the main logic cycle of most video-games

- It continuously runs while the game is active, managing the following aspects:
    1. **Processing user input** (e.g., keyboard, mouse, gamepad)
    2. **Updating the game state** (e.g., moving objects in the virtual space)
    3. **Rendering the game** (e.g., drawing the game world on the screen)
    4. **Simulating the passage of time** in the game (e.g., moving objects even in absence of inputs)

- Most commonly, some _wait_ is introduced at the end of each cycle 
    + to control the game's frame rate

---

## The Game Loop in PyGame

{{<code path="content/pong/example1_game_loop.py">}}

full example [on GitHub]({{<github-url repo="lab-snippets" path="snippets/lab1/example1_game_loop.py">}})

{{%/section%}}

---

## Clean Code Recommendations

1. Better to explicitly represent _game objects_ in the code
    - __Game Object__ $\approx$ any entity that may appear in the game world (e.g. the circle)
        + interesting aspects: _size_, _position_ , _speed_, _name_, etc.
        + may have methods to _update_ its state
    - the _overall_ **game state** consists of _all_ game objects therein contained
        + $\Rightarrow$ update the game $\equiv$ update _each_ game objects

{{%code path="content/pong/example2_game_object.py"%}}

full example [on GitHub]({{<github-url repo="lab-snippets" path="snippets/lab1/example2_game_object.py">}})


---

