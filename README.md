# Stride CLI

A command-line application for tracking walks and runs.

## Why I Built Stride

Stride CLI started as a Boot.dev personal project. I wanted to create something that I could use in my daily life.

I enjoy light cardio, so I wanted a simple way to stay consistent and track my progress from my computer.

What started as a simple activity tracker grew into a larger project where I could practice real software concepts including SQLite persistence, service-layer architecture, testing, data visualization, API integration, and Python packaging.

## Features

- Log walking and running activities
- Store activities with SQLite
- Update and delete activities
- Track distance, duration, pace, and notes
- View activity statistics
- Track fitness goals
- Search, filter, and sort activities
- Export activities to CSV
- View distance history and charts
- Check current weather by city
- Rich terminal interface

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/Kamari93/stride-cli.git
cd stride-cli
python3 -m venv .venv
source .venv/bin/activate
```

Install Stride:

```bash
pip install .
```

Run the application:

```bash
stride
```
## Architecture
Stride follows a layered architecture designed to keep responsibilities separated and reduce coupling between components.
```text
CLI
 ↓
Services
 ↓
Repository
 ↓
SQLite
```

Additional components handle statistics, data export, visualization, and external weather services.

**Main Components**

- **Models** — Define the application’s core data structures, including activities, goals, and weather data.
- **CLI** — Handles user interaction and Rich terminal presentation.
- **Services** — Contains application and business logic while coordinating between the CLI and data layers.
- **Repository** — Handles SQLite persistence and database operations.
- **Statistics** — Performs calculations such as distance totals, pace, streaks, and distance history.
- **Export** — Handles CSV generation.
- **Weather Provider** — Separates weather API integration from the rest of the application through a provider interface.
- **Charts** — Uses Plotext to visualize activity and distance history.

The application uses dependency injection for services and external providers, allowing components to be tested independently and reducing direct dependencies between layers.

## Testing

Stride uses pytest for automated testing.

The test suite covers core application behavior including:

* Activity and goal models
* SQLite repository operations
* Service-layer business logic
* Statistics and streak calculations
* Activity sorting, filtering, and searching
* CSV export
* Weather services and API error handling
* Distance history and visualization data

Run the full test suite with:
```bash
python3 -m pytest -v 
```
All tests should pass before making changes to the project.

## Tech Stack

* **Python 3.14** — Application development
* **SQLite** — Local data persistence
* **pytest** — Automated testing
* **Rich** — Terminal UI and formatted output
* **Plotext** — Terminal-based data visualization
* **Requests** — HTTP requests for weather API integration
* **Open-Meteo** — Weather and geocoding data
* **setuptools** — Python package building and installation
* **uv* — Optional development and dependency management