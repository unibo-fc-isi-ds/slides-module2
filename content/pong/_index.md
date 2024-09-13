
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

{{< slide id="game-loop" >}}

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

{{% code path="content/pong/example1_game_loop.py" %}}

full example [on GitHub]({{<github-url repo="lab-snippets" path="snippets/lab1/example1_game_loop.py">}})

---

#### Aspects to notice (cf. [PyGame documentation](https://www.pygame.org/docs/ref/event.html)):

- PyGame comes with a notion of _events_ and __event queue__ 
    * this is good for handling user _inputs_

- each event had a _type_ (e.g., `pygame.KEYDOWN` and `pygame.KEYUP`) and _attributes_ (e.g., `event.key`)
    * there is a _class_ for events, namely `pygame.event.Event`
    * event _types_ are indeed `int`egers

- events can be _retrieved_ from the queue (e.g., `pygame.event.get([RELEVANT_TYPES])`)...
    * where `RELEVANT_TYPES` is a _list_ of event _types_ to be retrieved

- ... and possibly _provoked_ (i.e. appended to the queue) by the programmer (e.g., `pygame.event.post(event)`)
    * where `event` is an instance of `pygame.event.Event`

---

## Clean Code Recommendations

1. Better to explicitly represent _game objects_ in the code
    - __Game Object__ $\approx$ any entity that may appear in the game world (e.g. the circle)
        + interesting aspects: _size_, _position_ , _speed_, _name_, etc.
        + may have methods to _update_ its state
    - the _overall_ **game state** consists of _all_ game objects therein contained
        + $\Rightarrow$ update the game $\equiv$ update _each_ game objects
    - cf. [PyGame documentation](https://www.pygame.org/docs/)

{{% multicol %}}
{{% col class="col-9" %}}
{{% code path="content/pong/example2_game_object.py" %}}
{{% /col %}}
{{% col %}}
{{<plantuml>}}

class GameObject {
    + name: str
    + position: Vector2
    + size: Vector2
    + speed: Vector2
    + bounding_box: Rect
    + update(dt: float)
}

package "pygame" {
    class Vector2 {
        + x: float
        + y: float
    }
    class Rect {
        + left: float
        + top: float
        + width: float
        + height: float
    }
}

GameObject *-d- Vector2
GameObject *-- Rect

{{</plantuml>}}
{{% /col %}}
{{% /multicol %}}


full example [on GitHub]({{<github-url repo="lab-snippets" path="snippets/lab1/example2_game_object.py">}})

---


## Clean Code Recommendations

2. Better to explicitly represent _input handlers_ and _controllers_ in the code
    - __Input Handler__ $\approx$ any entity that may _interpret_ user inputs and map them to _game events_
        + supports plugging in different _key maps_
    - __Game Events__ $\approx$ represent _actions_ that make sense for game objects
        + e.g., `MOVE_UP`, `MOVE_DOWN`, `STOP`, etc.
        + custom event _types_ can be defined via [`pygame.event.custom_type()`](https://www.pygame.org/docs/ref/event.html#pygame.event.custom_type)
    - __Controller__ $\approx$ any entity that may _interpret_ game events and _update_ the game state accordingly

{{% multicol %}}
{{% col class="col-9" %}}
{{% code path="content/pong/example3_controller.py" %}}
{{% /col %}}
{{% col %}}
{{<plantuml>}}

top to bottom direction

enum GameEvent {
    + MOVE_UP
    + MOVE_DOWN
    + MOVE_LEFT
    + MOVE_RIGHT
    + STOP
    + create_event(**kwargs): Event
    + {static} all(): set[GameEvent]
    + {static} types(): list[int]
}

package "pygame" {
    package "event" {
        class Event {
            + type: int
            + data: dict
        }
    }
}

class InputHandler {
    + keymap: Dict[int, int]
    + handle_inputs() -> List[int]
    + post_event(event: Event)
}

class Controller {
    - _game_object: GameObject
    - _speed: float
    + update(dt: float)
    - _update_object_according_to_event(game_object, event)
}

InputHandler <|-d- Controller

InputHandler .u.> GameEvent: uses
InputHandler .u.> Event: uses

{{</plantuml>}}
{{% /col %}}
{{% /multicol %}}

full example [on GitHub]({{<github-url repo="lab-snippets" path="snippets/lab1/example3_controller.py">}})

---

## Clean Code Recommendations

3. Better to delegate _rendering_ to a dedicated class taking care of the _view_ of the game
    - __View__ $\approx$ any entity that may _draw_ game objects on the screen
        + may have methods to _render_ the game (objects) on the screen
    - cf. [PyGame documentation](https://www.pygame.org/docs/ref/display.html)

{{% multicol %}}
{{% col class="col-9" %}}
{{% code path="content/pong/example4_view.py" %}}
{{% /col %}}
{{% col %}}
{{<plantuml>}}

top to bottom direction

class View {
    - _size: tuple[int, int]
    - _screen: Surface
    + background_color: Color
    + foreground_color: Color
    - _game_object: GameObject
    + render()
    - _reset_screen(screen, color)
    - _draw_game_object(game_object, color)
}

package "pygame" {
    class Surface {
        + fill(color: Color)
        + flip()
    }
    class Color {
        + r: int
        + g: int
        + b: int
        + a: int
    }
}

View .d.> Surface: uses
View ..> Color: uses

{{</plantuml>}}
{{% /col %}}
{{% /multicol %}}

full example [on GitHub]({{<github-url repo="lab-snippets" path="snippets/lab1/example4_view.py">}})

---

## Clean Code Recommendations

4. Wrap up
    - game loop is now much simplified
    - changes in _input handling_ $\rightarrow$ implement new `InputHandler`
    - changes in _game logic_ $\rightarrow$ implement new `Controller`
    - changes in _visualization_ $\rightarrow$ implement new `View`

{{% code path="content/pong/example5_game_loop_cleancode.py" %}}

full example [on GitHub]({{<github-url repo="lab-snippets" path="snippets/lab1/example5_game_loop_cleancode.py">}})

{{%/section%}}

---

{{%section%}}

{{< slide id="model" >}}

## Pong Model

{{%/section%}}

---

{{%section%}}

{{< slide id="io" >}}

## Pong I/O

### Input handling and Rendering

{{%/section%}}

---

{{%section%}}

{{< slide id="architecture" >}}

## Distributed Pong Architecture


{{%/section%}}

---

{{%section%}}

{{< slide id="protocols" >}}

## Distributed Pong Protocols


{{%/section%}}

---

{{%section%}}

{{< slide id="analysis" >}}

## Distributed Pong Analysis



{{%/section%}}