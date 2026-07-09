## Data classes @dataclass

## What is a @dataclass?

- A dataclass is a decorator (`@dataclass`) that automatically generates common methods for a class.
- It can create methods like `__init__()`, `__repr__()`, and `__eq__()` without having to write them manually.
- It is mainly used for classes whose primary purpose is storing data.

## What problem does it solve?

- Reduces boilerplate code.
- Makes classes shorter and easier to read.
- Prevents having to repeatedly write constructors and other common methods.
- Makes it easier to compare objects because equality methods can be generated automatically.

## What is `field()` used for?

- `field()` lets you customize how an individual attribute behaves.
- It can be used to:
  - Set default values in more advanced ways.
  - Use `default_factory`.
  - Exclude fields from comparisons or representations.
  - Control whether a field is included in the generated `__init__()`.

## `default` vs `default_factory`

### `default`
- Used when the default value is a simple immutable object.
- Example:
  ```python
  age: int = 18
  ```

### `default_factory`
- Used when the default value should be created each time a new object is instantiated.
- Commonly used with mutable types like lists, dictionaries, and sets.
- Example:
  ```python
  from dataclasses import field

  grades: list[int] = field(default_factory=list)
  ```
- This avoids multiple objects accidentally sharing the same list.

## What does `__post_init__()` do?

- Runs automatically after the generated `__init__()` finishes.
- Useful for:
  - Validating data.
  - Computing additional fields.
  - Performing setup that depends on initialized values.
- It lets you keep the benefits of the generated constructor while still running custom initialization code.

---

# Reflection

## What surprised me?

- I didn't realize dataclasses automatically generate several methods like `__init__()`, `__repr__()`, and `__eq__()`.
- I also learned that mutable defaults (like `[]`) should use `default_factory` instead of assigning them directly.
- `__post_init__()` was interesting because it allows custom initialization without replacing the automatically generated constructor.

## When do dataclasses seem useful?

- When creating classes that mainly hold data.
- Configuration objects.
- Records or models.
- Game objects with simple attributes.
- API responses or database records.
- Any time I find myself writing lots of constructors that simply assign values to attributes.

## How are they different from writing a normal class?

- A normal class usually requires writing the constructor and other methods manually.
- Dataclasses generate much of that code automatically.
- They require less boilerplate, making the code easier to read and maintain.
- You can still customize behavior with `field()` and `__post_init__()` when needed.

---------------------------------------------------------------------
# Notes on the Rich Library

## What is Rich?

Rich is a Python library that makes terminal applications look much more professional. Instead of plain `print()` statements, it provides components for formatting text, creating tables, displaying panels, showing progress bars, prompting users, and much more.

Instead of focusing on business logic, Rich helps improve the user experience.

---

# Console

## What problem does it solve?

The Console object is Rich's main interface.

Instead of using `print()`, almost everything is displayed through a `Console`.

It supports:
- Colored text
- Styled text
- Pretty printing
- Emojis
- Markdown
- Tables
- Panels

Almost every Rich application starts by creating a single Console object.

Example:

```python
console = Console()
```

## Where might I use it in Stride CLI?

- Display the application title
- Print success messages
- Print error messages
- Display activities
- Display statistics
- Show goodbye message when exiting

I think the CLI class should probably own one Console object since almost every screen will need it.

---

# Panel

## What problem does it solve?

A Panel places content inside a decorative box.

Instead of text floating around the terminal, related information can be grouped together.

Panels make applications feel more organized and easier to read.

## Where might I use it?

- Welcome screen
- Main menu
- Activity summary
- Statistics summary
- Goal progress
- Error messages
- Help screen

For example:

```
+----------------------------+
|        STRIDE CLI          |
+----------------------------+
```

could be a Rich Panel.

---

# Table

## What problem does it solve?

A Table displays structured information in rows and columns.

Instead of manually spacing text, Rich aligns everything automatically.

## Where might I use it?

Viewing activities.

Example:

Date | Type | Distance | Duration | Pace
------------------------------------------
6/12 | Run  | 3.1 mi   | 28 min   | 9:02
6/13 | Walk | 2.0 mi   | 35 min   | 17:30

It would also work well for:
- Weekly statistics
- Monthly summaries
- Goals
- Personal records

---

# Prompt

## What problem does it solve?

Prompt provides a cleaner way to collect user input than using `input()`.

It also supports validation and default values.

Instead of writing validation logic everywhere, Prompt can help ensure users enter valid data.

## Where might I use it?

- Main menu selection
- Activity type
- Distance
- Duration
- Notes
- Route
- Goal settings

Eventually Prompt could replace almost every call to `input()`.

---

# Reflection

## What surprised me?

Rich isn't just about colors. It provides reusable UI components for terminal applications.

It almost feels like a GUI framework, except everything stays inside the terminal.

## When would Rich be useful?

Any CLI application where users spend more than a few minutes.

Examples:
- Task managers
- Budget trackers
- Habit trackers
- Fitness apps like Stride CLI
- Developer tools

## Biggest takeaway

Rich separates *what* I want to display from *how* it looks.

Instead of worrying about spacing text manually, I can use components like Panels and Tables.