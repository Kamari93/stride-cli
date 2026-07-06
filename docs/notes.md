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