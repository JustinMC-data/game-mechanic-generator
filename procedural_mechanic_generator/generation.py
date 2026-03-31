"""Mechanic generation engine."""

from __future__ import annotations

from .models import GenerationContext, MechanicBlueprint
from .utils import hash_pick, title_case


class MechanicGenerationEngine:
    """Builds deterministic, structured mechanics from normalized inputs."""

    def generate(self, context: GenerationContext) -> MechanicBlueprint:
        profile = self._select_profile(context)
        theme = title_case(context.normalized_input.theme)
        genre = title_case(context.normalized_input.genre)
        mechanic_type = title_case(context.normalized_input.mechanic_type)
        constraint_suffix = (
            f" with {' / '.join(title_case(c) for c in context.normalized_input.constraints[:2])}"
            if context.normalized_input.constraints
            else ""
        )
        mechanic_name = f"{profile['name_prefix']} {theme} {mechanic_type}{constraint_suffix}".strip()

        description = profile["description_template"].format(
            theme=theme,
            genre=genre,
            mechanic_type=mechanic_type,
            constraints=", ".join(title_case(c) for c in context.normalized_input.constraints) or "no extra constraints",
        )

        ue5_stub = {
            "components": profile["ue5_components"],
            "events": profile["ue5_events"],
            "variables": profile["ue5_variables"],
            "pseudo_logic": profile["ue5_logic"],
        }

        return MechanicBlueprint(
            mechanic_name=mechanic_name,
            description=description,
            core_loop=profile["core_loop"],
            player_actions=profile["player_actions"],
            system_rules=profile["system_rules"],
            resources=profile["resources"],
            progression_hooks=profile["progression_hooks"],
            risk_reward_structure=profile["risk_reward_structure"],
            edge_cases=profile["edge_cases"],
            ue5_blueprint_stub=ue5_stub,
            resource_state=profile["resource_state"],
            tags=profile["tags"],
            tuning=profile["tuning"],
        )

    def _select_profile(self, context: GenerationContext) -> dict:
        key = (
            context.normalized_input.theme,
            context.normalized_input.genre,
            context.normalized_input.mechanic_type,
        )
        profiles = self._profiles()
        if key in profiles:
            return profiles[key]
        return hash_pick(list(profiles.values()), context.seed)

    def _profiles(self) -> dict[tuple[str, str, str], dict]:
        return {
            ("cyberpunk", "roguelike", "combat"): {
                "name_prefix": "Ghostline Breach",
                "description_template": (
                    "A {theme} {genre} combat mechanic where every engagement alternates between exposure and infiltration. "
                    "The player seeds intrusions into enemy implants, cashes them out during line-of-sight windows, and rides escalating counter-hacks under {constraints}."
                ),
                "core_loop": [
                    "Tag a target through stealth positioning to plant a dormant breach marker.",
                    "Trigger a visible combat action to wake the breach and expose enemy subsystems.",
                    "Exploit the opened subsystem for bonus damage, intel, or rerouted defenses.",
                    "Decide whether to overclock the intrusion for a bigger payout before the counter-hack lands.",
                ],
                "player_actions": [
                    "Shadow-mark enemies from cover to queue breach markers.",
                    "Fire, slide, or melee to activate marked targets and collapse their defense state.",
                    "Hijack a revealed subsystem such as optics, ammo feed, or ally IFF routing.",
                    "Purge trace buildup at terminals or by performing takedowns on isolated targets.",
                ],
                "system_rules": [
                    "Only marked targets can be breached, and marks decay if the player remains fully exposed for two turns.",
                    "Each successful breach adds Trace, increasing enemy scan speed and turret hostility.",
                    "Subsystem hijacks have mutually exclusive branches, preventing a single breach from granting every reward.",
                    "Elite enemies can invert one hijack effect once per encounter, forcing the player to vary breach timing.",
                ],
                "resources": ["Trace", "Focus", "Breach Markers", "Intel Fragments"],
                "progression_hooks": [
                    "Unlock new breach branches that trade raw damage for information warfare.",
                    "Earn persistent ghostware upgrades that let one mark survive between rooms.",
                    "Introduce faction-specific implants so later runs reshape breach priorities.",
                ],
                "risk_reward_structure": [
                    "Holding breaches longer increases subsystem payout but multiplies scan pressure.",
                    "Fast activation is safer but yields only shallow hijacks and less intel.",
                    "Purging Trace resets threat but costs combat tempo and positional advantage.",
                ],
                "edge_cases": [
                    "If a room contains only drones, breach markers reroute through their controller rather than failing.",
                    "Bosses convert excess Trace into arena hazards instead of instant detection spikes.",
                    "When no cover exists, movement abilities can count as temporary stealth windows for marking.",
                ],
                "ue5_components": ["BP_BreachComponent", "BP_TraceMeterComponent", "BP_SubsystemHijackInterface"],
                "ue5_events": ["OnTargetMarked", "OnBreachActivated", "OnTraceThresholdReached", "OnHijackResolved"],
                "ue5_variables": ["TraceValue", "FocusValue", "ActiveMarks", "HijackCooldown", "SubsystemStateMap"],
                "ue5_logic": [
                    "OnTargetMarked: add mark entry with decay timer keyed by actor ID.",
                    "OnBreachActivated: validate mark, consume focus, reveal subsystem branch set.",
                    "OnHijackResolved: apply branch effect, add trace, broadcast AI alert delta.",
                    "OnTraceThresholdReached: escalate enemy scan cones and enable counter-hack behaviors.",
                ],
                "resource_state": {"Trace": 0, "Focus": 5, "Breach Markers": 2, "Intel Fragments": 0},
                "tags": ["stealth", "hacking", "burst windows", "counterplay"],
                "tuning": {"risk_index": 0.68, "reward_index": 0.74, "failure_penalty": 1.9, "progression_velocity": 1.1},
            },
            ("high fantasy", "mmo", "crafting"): {
                "name_prefix": "Aetherforge Concord",
                "description_template": (
                    "A {theme} {genre} crafting mechanic centered on collaborative resonance forging. "
                    "Crafters weave base matter, lineage sigils, and timed guild techniques into gear whose final qualities depend on synchronized choices under {constraints}."
                ),
                "core_loop": [
                    "Refine raw materials into tiered essences with identifiable temper traits.",
                    "Bind a recipe frame that sets the item class and resonance tolerances.",
                    "Layer catalyst actions during timed forge windows to steer the final property spread.",
                    "Stabilize or intentionally overload the item to choose reliability versus rare affixes.",
                ],
                "player_actions": [
                    "Survey node quality to source common, rare, and lineage-bound reagents.",
                    "Prime a forge frame with one school focus such as guardian, storm, or ember.",
                    "Spend crafting beats on refine, bind, infuse, temper, or overcharge actions.",
                    "Invite a specialist to add a guild technique that can only be inserted during a live forge step.",
                ],
                "system_rules": [
                    "Every recipe has a stability budget that drops as rare traits are infused.",
                    "Material tiers interact multiplicatively, so high-tier catalysts amplify the best and worst traits of the base.",
                    "Guild techniques are unique per craft and lock one branch of the result tree to avoid stacking exploits.",
                    "Items can be finalized early for safe output or pushed into volatility for a chance at lineage traits.",
                ],
                "resources": ["Base Matter", "Essence Tier", "Stability", "Lineage Sigils", "Guild Favor"],
                "progression_hooks": [
                    "Unlock new forge schools that expand recipe frames rather than just raising item level.",
                    "Master temper patterns that reveal hidden material interactions and reduce waste.",
                    "Attach guild contracts that create social demand for specialized outputs.",
                ],
                "risk_reward_structure": [
                    "Overcharging yields access to lineage traits but can fracture ingredients or produce cursed outputs.",
                    "Safe crafting protects expensive reagents but caps affix depth and market value.",
                    "Bringing in a second crafter increases peak potential while adding coordination risk and guild taxation.",
                ],
                "edge_cases": [
                    "If a player disconnects mid-craft, the forge enters stasis instead of consuming partner-only actions.",
                    "Recipes missing rare reagents can still resolve by creating utilitarian lower-tier variants.",
                    "If stability reaches zero exactly on finalization, the item resolves as volatile but bind-on-use to prevent market abuse.",
                ],
                "ue5_components": ["BP_ForgeSessionComponent", "BP_ResonanceRecipeData", "BP_GuildTechniqueInterface"],
                "ue5_events": ["OnCraftBeatCommitted", "OnStabilityChanged", "OnTechniqueInserted", "OnItemFinalized"],
                "ue5_variables": ["CurrentStability", "EssenceTier", "RecipeFrame", "TechniqueSlots", "VolatilityScore"],
                "ue5_logic": [
                    "OnCraftBeatCommitted: resolve selected action against recipe frame and material traits.",
                    "OnStabilityChanged: update forge state visuals and unlock or close volatility branches.",
                    "OnTechniqueInserted: consume guild technique token and reserve one result branch.",
                    "OnItemFinalized: roll deterministic property weights from accumulated resonance state.",
                ],
                "resource_state": {"Base Matter": 6, "Essence Tier": 1, "Stability": 100, "Lineage Sigils": 1, "Guild Favor": 2},
                "tags": ["crafting", "social", "timing", "resource tiers"],
                "tuning": {"risk_index": 0.52, "reward_index": 0.79, "failure_penalty": 2.4, "progression_velocity": 0.9},
            },
            ("space horror", "survival", "traversal"): {
                "name_prefix": "Vacuum Tether",
                "description_template": (
                    "A {theme} {genre} traversal mechanic where movement is planned around oxygen debt and anchor discipline. "
                    "The player advances by placing temporary tethers, slingshotting through compromised corridors, and trading route speed against survivability under {constraints}."
                ),
                "core_loop": [
                    "Survey the environment for anchor points, hull breaches, and air pockets.",
                    "Commit oxygen to a movement route by placing or reclaiming tether anchors.",
                    "Traverse using controlled pulls, wall catches, and burst vents to bypass hazards.",
                    "Reach a safe chamber to rebalance oxygen debt before the route collapses.",
                ],
                "player_actions": [
                    "Deploy tether anchors onto stable surfaces or intact maintenance rings.",
                    "Reel in or release line tension to steer momentum through zero-G spaces.",
                    "Seal micro-breaches with emergency foam to create a temporary breathable pocket.",
                    "Cut a tether early to dodge debris at the cost of uncontrolled drift.",
                ],
                "system_rules": [
                    "Every anchor extends traversal safety but adds setup time and tool wear.",
                    "Oxygen drains faster while drifting untethered or crossing contaminated zones.",
                    "Emergency foam creates short-lived refuges that also attract blind hostile life.",
                    "Momentum carries through turns, so poor line angles can force collision or overshoot penalties.",
                ],
                "resources": ["Oxygen", "Tether Charges", "Suit Integrity", "Emergency Foam"],
                "progression_hooks": [
                    "Upgrade tether heads for magnetic recall and longer safe arcs.",
                    "Unlock suit mods that convert skillful wall catches into small oxygen refunds.",
                    "Discover route schematics that reveal stable anchor chains in derelict sectors.",
                ],
                "risk_reward_structure": [
                    "Fast untethered movement preserves tool charges but sharply increases oxygen and collision risk.",
                    "Dense anchor placement is safer yet may leave the player underprepared for later zones.",
                    "Temporary air pockets save runs but can trigger hostile migrations into future routes.",
                ],
                "edge_cases": [
                    "If no valid anchor exists, emergency foam can form a one-use soft anchor on debris.",
                    "When oxygen reaches zero during a successful room transition, the player arrives incapacitated instead of dying instantly.",
                    "Large creatures can snap lines, but only if the line has already exceeded safe tension once.",
                ],
                "ue5_components": ["BP_TetherTraversalComponent", "BP_OxygenComponent", "BP_AnchorPointActor"],
                "ue5_events": ["OnAnchorPlaced", "OnTensionChanged", "OnAirPocketCreated", "OnSafeZoneReached"],
                "ue5_variables": ["CurrentOxygen", "ActiveTethers", "SuitIntegrity", "MomentumVector", "HazardPressure"],
                "ue5_logic": [
                    "OnAnchorPlaced: validate surface class, spend tether charge, create tension spline.",
                    "OnTensionChanged: modify movement assist and collision risk thresholds.",
                    "OnAirPocketCreated: spawn timed oxygen refuge and register hostile attraction pulse.",
                    "OnSafeZoneReached: settle oxygen debt and convert route efficiency into minor rewards.",
                ],
                "resource_state": {"Oxygen": 100, "Tether Charges": 3, "Suit Integrity": 100, "Emergency Foam": 2},
                "tags": ["oxygen", "routing", "hazards", "momentum"],
                "tuning": {"risk_index": 0.61, "reward_index": 0.66, "failure_penalty": 2.1, "progression_velocity": 0.95},
            },
        }
