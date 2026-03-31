"""Top-level orchestration service for mechanic generation."""

from __future__ import annotations

from .balancing import BalancingConsistencyEngine
from .error_handling import ErrorHandlingLayer
from .generation import MechanicGenerationEngine
from .input_layer import InputLayer
from .logging_utils import EventLogger
from .models import GenerationContext, GenerationResult
from .novelty import NoveltyAnalysisEngine
from .output import OutputFormattingLayer
from .rationale import DesignRationaleEngine
from .simulation import SimulationEngine
from .utils import make_seed, stable_trace_id
from .validation import ValidationLayer


class MechanicGeneratorService:
    """Facade that coordinates all modules into a single deterministic pipeline."""

    def __init__(self) -> None:
        self.input_layer = InputLayer()
        self.validation_layer = ValidationLayer()
        self.generation_engine = MechanicGenerationEngine()
        self.simulation_engine = SimulationEngine()
        self.balancing_engine = BalancingConsistencyEngine()
        self.novelty_engine = NoveltyAnalysisEngine()
        self.rationale_engine = DesignRationaleEngine()
        self.output_layer = OutputFormattingLayer()
        self.error_handler = ErrorHandlingLayer()

    def generate(self, payload: dict) -> GenerationResult:
        bootstrap_logger = EventLogger(trace_id="pending", debug=bool(payload.get("debug", False)) if isinstance(payload, dict) else False)
        normalized_input, input_report = self.input_layer.normalize(payload, bootstrap_logger)
        seed = make_seed(normalized_input)
        logger = EventLogger(trace_id=stable_trace_id(seed), debug=normalized_input.debug)
        logger.log("input", "Received normalized input.", normalized=normalized_input.__dict__)

        if not input_report.is_valid:
            for error in input_report.errors:
                logger.log("validation_error", error.message, code=error.code, field=error.field)
            return GenerationResult(success=False, errors=self.error_handler.format_errors(input_report.errors), logs=logger.dump())

        context = GenerationContext(normalized_input=normalized_input, seed=seed, trace_id=logger.trace_id)
        context_report = self.validation_layer.validate_context(context)
        if not context_report.is_valid:
            for error in context_report.errors:
                logger.log("validation_error", error.message, code=error.code, field=error.field)
            return GenerationResult(success=False, errors=self.error_handler.format_errors(context_report.errors), logs=logger.dump())

        blueprint = self.generation_engine.generate(context)
        logger.log("generation", "Generated mechanic blueprint.", mechanic_name=blueprint.mechanic_name, tags=blueprint.tags)

        simulation = self.simulation_engine.simulate(context, blueprint)
        logger.log("simulation", "Completed deterministic simulation.", steps=len(simulation))

        balancing_notes = self.balancing_engine.analyze(blueprint)
        logger.log("balancing", "Completed balancing pass.", notes=len(balancing_notes))

        novelty_analysis = self.novelty_engine.analyze(context, blueprint)
        logger.log("novelty", "Computed novelty score.", novelty_score=novelty_analysis["novelty_score"])

        rationale = self.rationale_engine.analyze(context, blueprint)
        logger.log("rationale", "Generated design rationale.")

        output = self.output_layer.format(context, blueprint, simulation, balancing_notes, novelty_analysis, rationale)
        schema_report = self.output_layer.validate_schema(output)
        if not schema_report.is_valid:
            for error in schema_report.errors:
                logger.log("validation_error", error.message, code=error.code, field=error.field)
            return GenerationResult(success=False, errors=self.error_handler.format_errors(schema_report.errors), logs=logger.dump())

        logger.log("output", "Generated schema-compliant output.", export_version=output["export_version"])
        return GenerationResult(success=True, output=output, logs=logger.dump())
