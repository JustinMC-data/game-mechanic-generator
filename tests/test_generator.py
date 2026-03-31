from __future__ import annotations

import unittest

from procedural_mechanic_generator.service import MechanicGeneratorService


class MechanicGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = MechanicGeneratorService()

    def test_schema_validation_for_cyberpunk_combat_case(self) -> None:
        result = self.service.generate(
            {
                "theme": "Cyberpunk",
                "genre": "Roguelike",
                "complexity": "Medium",
                "mechanic_type": "Combat",
            }
        )
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        output = result.output or {}
        self.assertEqual(output["theme"], "Cyberpunk")
        self.assertEqual(output["genre"], "Roguelike")
        self.assertIn("simulation_output", output)
        self.assertGreaterEqual(output["novelty_analysis"]["novelty_score"], 0)
        self.assertIn("BP_BreachComponent", output["ue5_blueprint_stub"]["components"])

    def test_deterministic_output(self) -> None:
        payload = {
            "theme": "High Fantasy",
            "genre": "MMO",
            "complexity": "Advanced",
            "mechanic_type": "Crafting",
            "constraints": ["No Magic Resistance"],
        }
        first = self.service.generate(payload)
        second = self.service.generate(payload)
        self.assertTrue(first.success)
        self.assertTrue(second.success)
        self.assertEqual(first.output, second.output)

    def test_contradictory_constraints_are_rejected(self) -> None:
        result = self.service.generate(
            {
                "theme": "Cyberpunk",
                "genre": "Roguelike",
                "complexity": "Medium",
                "mechanic_type": "Combat",
                "constraints": ["low gravity", "fall damage multiplier 3x"],
            }
        )
        self.assertFalse(result.success)
        self.assertTrue(any(error["code"] == "contradictory_constraints" for error in result.errors))

    def test_demo_mode_ignores_inputs(self) -> None:
        result = self.service.generate(
            {
                "theme": "invalid",
                "genre": "invalid",
                "complexity": "invalid",
                "mechanic_type": "invalid",
                "demo_mode": True,
            }
        )
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertEqual((result.output or {})["theme"], "Mythic Sci-fi")

    def test_space_horror_traversal_contains_oxygen_management(self) -> None:
        result = self.service.generate(
            {
                "theme": "Space Horror",
                "genre": "Survival",
                "complexity": "Simple",
                "mechanic_type": "Traversal",
            }
        )
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        output = result.output or {}
        self.assertIn("Oxygen", output["resources"])
        self.assertTrue(
            any(
                "oxygen" in step["player_decision"].lower() or "oxygen" in step["outcome"].lower()
                for step in output["simulation_output"]
            )
        )

    def test_balancing_notes_include_exploit_detection(self) -> None:
        result = self.service.generate(
            {
                "theme": "High Fantasy",
                "genre": "MMO",
                "complexity": "Advanced",
                "mechanic_type": "Crafting",
            }
        )
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertTrue(any("Exploit check" in note for note in (result.output or {})["balancing_notes"]))

    def test_missing_theme_returns_structured_error(self) -> None:
        result = self.service.generate(
            {
                "genre": "Roguelike",
                "complexity": "Medium",
                "mechanic_type": "Combat",
            }
        )
        self.assertFalse(result.success)
        self.assertEqual(result.errors[0]["field"], "theme")

    def test_unsupported_genre_returns_error(self) -> None:
        result = self.service.generate(
            {
                "theme": "Cyberpunk",
                "genre": "Metroidvania",
                "complexity": "Medium",
                "mechanic_type": "Combat",
            }
        )
        self.assertFalse(result.success)
        self.assertTrue(any(error["code"] == "invalid_genre" for error in result.errors))

    def test_malformed_input_returns_structured_error(self) -> None:
        result = self.service.generate("bad input")  # type: ignore[arg-type]
        self.assertFalse(result.success)
        self.assertEqual(result.errors[0]["code"], "malformed_input")


if __name__ == "__main__":
    unittest.main()
