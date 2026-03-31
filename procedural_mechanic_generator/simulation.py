"""Deterministic gameplay loop simulation."""

from __future__ import annotations

from copy import deepcopy

from .models import GenerationContext, MechanicBlueprint, SimulationStep


class SimulationEngine:
    """Produces a reproducible simulation trace for the generated mechanic."""

    def simulate(self, context: GenerationContext, blueprint: MechanicBlueprint) -> list[SimulationStep]:
        key = (
            context.normalized_input.theme,
            context.normalized_input.genre,
            context.normalized_input.mechanic_type,
        )
        state = deepcopy(blueprint.resource_state)
        if key == ("cyberpunk", "roguelike", "combat"):
            return self._simulate_cyberpunk_combat(state)
        if key == ("high fantasy", "mmo", "crafting"):
            return self._simulate_fantasy_crafting(state)
        if key == ("space horror", "survival", "traversal"):
            return self._simulate_space_traversal(state)
        return self._simulate_generic(state, blueprint)

    def _simulate_cyberpunk_combat(self, state: dict[str, int | float]) -> list[SimulationStep]:
        steps = []
        steps.append(self._step(1, "setup", "Mark a patrolling sentinel from cover.", "Breach marker planted; trace remains low.", state, {"Breach Markers": -1}, "success"))
        steps.append(self._step(2, "engage", "Slide into line-of-sight and trigger the mark with a pistol burst.", "Optics subsystem opens; turret feed becomes hijackable.", state, {"Focus": -1, "Trace": 18}, "success"))
        steps.append(self._step(3, "gamble", "Overclock the hijack to reroute turret fire into nearby drones.", "Enemy scan lattice accelerates and forces a reposition.", state, {"Trace": 24, "Intel Fragments": 1}, "high_reward"))
        steps.append(self._step(4, "failure_branch", "Ignore a purge window and tag a second elite target.", "Elite counter-hack reflects a branch, jamming one weapon slot.", state, {"Trace": 22, "Focus": -1}, "setback"))
        steps.append(self._step(5, "recovery", "Perform an isolated takedown to purge trace before full detection.", "Trace partially resets and one breach marker is refunded.", state, {"Trace": -30, "Breach Markers": 1}, "recovery"))
        steps.append(self._step(6, "finish", "Cash out the remaining breach for intel instead of damage.", "Encounter ends with moderate trace and persistent run knowledge.", state, {"Intel Fragments": 2, "Trace": 8}, "success"))
        return steps

    def _simulate_fantasy_crafting(self, state: dict[str, int | float]) -> list[SimulationStep]:
        steps = []
        steps.append(self._step(1, "refine", "Refine rare ore and herb ash into a tier-two essence blend.", "Material quality rises but stability tightens.", state, {"Base Matter": -2, "Essence Tier": 1, "Stability": -8}, "success"))
        steps.append(self._step(2, "bind", "Bind a guardian frame for a plate gauntlet order.", "Recipe locks defensive trait weights into the result tree.", state, {"Stability": -10}, "success"))
        steps.append(self._step(3, "infuse", "Insert a guild technique during the resonance beat.", "A unique branch opens for shield pulse utility.", state, {"Guild Favor": -1, "Stability": -12}, "high_reward"))
        steps.append(self._step(4, "gamble", "Overcharge the forge to chase a lineage affix.", "Volatility spikes; the item risks fracture if pushed again.", state, {"Lineage Sigils": -1, "Stability": -28}, "high_risk"))
        steps.append(self._step(5, "recover", "Choose temper rather than another overcharge.", "Stability loss slows and a cursed branch is pruned.", state, {"Stability": 6}, "recovery"))
        steps.append(self._step(6, "finalize", "Finalize at narrow positive stability.", "The gauntlet resolves with a defensive pulse and one lineage perk.", state, {"Stability": -12}, "success"))
        return steps

    def _simulate_space_traversal(self, state: dict[str, int | float]) -> list[SimulationStep]:
        steps = []
        steps.append(self._step(1, "survey", "Scan the corridor and identify two safe anchor rings beyond a hull tear.", "Hazard pressure map updates with debris rhythm.", state, {}, "success"))
        steps.append(self._step(2, "route_commit", "Place the first tether to control a long drift segment.", "Travel speed drops slightly but collision risk falls.", state, {"Tether Charges": -1, "Oxygen": -6}, "success"))
        steps.append(self._step(3, "risk_window", "Cut the line early to slingshot past an electrified bulkhead.", "Momentum gain saves time but spikes oxygen debt.", state, {"Oxygen": -18, "Suit Integrity": -9}, "high_risk"))
        steps.append(self._step(4, "failure_branch", "Miss the next anchor and deploy emergency foam mid-drift.", "A temporary air pocket forms, but nearby hostiles begin converging.", state, {"Emergency Foam": -1, "Oxygen": 12}, "recovery"))
        steps.append(self._step(5, "decision", "Use the air pocket only briefly and sprint the final lane.", "The player preserves foam duration for future cover at the cost of suit strain.", state, {"Oxygen": -14, "Suit Integrity": -6}, "tense_success"))
        steps.append(self._step(6, "safe_zone", "Reach the maintenance chamber and reclaim the first tether.", "Oxygen debt stabilizes and route efficiency grants salvage.", state, {"Tether Charges": 1, "Oxygen": 8}, "success"))
        return steps

    def _simulate_generic(self, state: dict[str, int | float], blueprint: MechanicBlueprint) -> list[SimulationStep]:
        return [
            self._step(
                1,
                "bootstrap",
                f"Start the first loop of {blueprint.mechanic_name}.",
                "The system initializes its primary state machine.",
                state,
                {},
                "success",
            )
        ]

    def _step(
        self,
        tick: int,
        phase: str,
        decision: str,
        response: str,
        state: dict[str, int | float],
        delta: dict[str, int | float],
        outcome: str,
    ) -> SimulationStep:
        for key, value in delta.items():
            state[key] = state.get(key, 0) + value
        return SimulationStep(
            tick=tick,
            phase=phase,
            player_decision=decision,
            system_response=response,
            resource_delta=dict(delta),
            outcome=f"{outcome}; resulting_state={state}",
        )
