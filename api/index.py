from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from pydantic import BaseModel, Field

from procedural_mechanic_generator.service import MechanicGeneratorService


class GenerateRequest(BaseModel):
    theme: str | None = None
    genre: str | None = None
    complexity: str | None = None
    mechanic_type: str | None = None
    constraints: list[str] = Field(default_factory=list)
    demo_mode: bool = False
    debug: bool = False


app = FastAPI(title="Game Mechanic API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate")
@app.post("/api/generate")
def generate_mechanic(request: GenerateRequest):
    payload = request.model_dump()
    try:
        result = MechanicGeneratorService().generate(payload)
        return {
            "success": result.success,
            "output": result.output,
            "errors": result.errors,
            "logs": result.logs,
        }
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "output": None,
                "errors": [
                    {
                        "code": "internal_error",
                        "message": "Mechanic generation failed.",
                        "field": None,
                        "severity": "error",
                        "details": str(exc),
                    }
                ],
                "logs": [],
            },
        )


handler = Mangum(app)
