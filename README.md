[![Live Demo](https://img.shields.io/badge/Live%20Demo-Add%20URL%20after%20deploy-blue)](PASTE_VERCEL_URL_HERE)

# Game Mechanic

Game Mechanic is a deterministic procedural generator for structured game design ideas. It accepts a constrained set of themes, genres, complexity levels, and mechanic types, then runs them through normalization, validation, generation, simulation, balancing, novelty analysis, and rationale layers before returning a schema-compliant JSON payload through the FastAPI endpoint in `api/index.py`.

## How it works

The `procedural_mechanic_generator/` package is organized as a procedural pipeline:

- `__init__.py`: Exposes `MechanicGeneratorService` as the package entry point.
- `__main__.py`: Runs the CLI when you execute the package with `python -m procedural_mechanic_generator`.
- `balancing.py`: Produces balancing notes, exploit checks, and tuning guidance from generated mechanic data.
- `cli.py`: Defines the command-line interface and prints JSON results.
- `config.py`: Stores allowed inputs, contradiction rules, numeric safety ranges, genre conventions, and the demo profile.
- `error_handling.py`: Converts internal validation issues into stable API/CLI error payloads.
- `generation.py`: Builds the deterministic mechanic blueprint from normalized inputs.
- `input_layer.py`: Normalizes raw inputs, applies demo mode, and performs early input validation.
- `logging_utils.py`: Captures structured trace events for debugging and monitoring.
- `models.py`: Defines the dataclasses shared across the full pipeline.
- `novelty.py`: Scores the generated mechanic against genre conventions and explains the novelty result.
- `output.py`: Formats the final JSON payload and validates its schema.
- `rationale.py`: Generates designer-facing reasoning for why the mechanic works.
- `service.py`: Orchestrates the full generation pipeline end to end.
- `simulation.py`: Produces a deterministic simulation trace for the generated mechanic.
- `utils.py`: Provides normalization, hashing, seeding, formatting, and bounded-value helpers.
- `validation.py`: Applies contradiction and feasibility checks before generation completes.

## Running locally

```bash
cd Game-Mechanic
pip install -r requirements.txt
uvicorn api.index:app --reload
# then open public/index.html in a browser or serve it with a static server
```

## Deploying to Vercel

1. Push the repository to GitHub.
2. Import the GitHub repository on [vercel.com](https://vercel.com/).
3. Leave the build settings at their defaults; this repo already includes `vercel.json`, so no build command or output directory is required.
4. Deploy.

## Allowed inputs

- Themes: `cosmic horror`, `cyberpunk`, `dieselpunk`, `fantasy`, `high fantasy`, `mythic sci-fi`, `post-apocalypse`, `space horror`
- Genres: `action rpg`, `deck-builder`, `immersive sim`, `mmo`, `roguelike`, `rts`, `survival`
- Complexities: `advanced`, `medium`, `simple`
- Mechanic types: `ai behavior`, `combat`, `crafting`, `economy`, `traversal`
