import unittest
from unittest.mock import patch
from CodeAnalyzer import CodeMetricsCalculator, CodeAnalyzer, calculate_emissions

# Assuming the provided code is saved in a file named `code_analyzer.py` and imported here
# from code_analyzer import CodeMetricsCalculator, CodeAnalyzer, calculate_emissions

class TestCodeMetricsCalculator(unittest.TestCase):
    def test_calculate_complexity_score(self):
        code = """
for i in range(10):
    print(i)
"""
        calculator = CodeMetricsCalculator(code)
        complexity_score = calculator.calculate_complexity_score()
        self.assertEqual(complexity_score, 2.5)  # One loop with weight 2.5

    def test_calculate_emission_factor(self):
        code = """
for i in range(10):
    print(i)
"""
        calculator = CodeMetricsCalculator(code)
        emission_factor = calculator.calculate_emission_factor()
        self.assertAlmostEqual(emission_factor, 0.000101, places=6)  # Verify emission factor

class TestCodeAnalyzer(unittest.TestCase):
    def test_detect_issues(self):
        code = """
for i in range(len(my_list)):
    print(i)
"""
        analyzer = CodeAnalyzer(code)
        issues, _ = analyzer.analyze()
        self.assertTrue(any(issue["issue"] == "range(len()) antipattern" for issue in issues))

    def test_apply_optimizations(self):
        code = """
for i in range(len(my_list)):
    print(my_list[i])
"""
        analyzer = CodeAnalyzer(code)
        _, optimized_code = analyzer.analyze()
        self.assertIn("enumerate", optimized_code)  # Check if `enumerate` is used in optimized code

class TestEmissions(unittest.TestCase):
    def test_calculate_emissions(self):
        code = """
for i in range(10):
    print(i)
"""
        emissions = calculate_emissions(code)
        self.assertGreater(emissions, 0)  # Emissions should be a positive value

    def test_calculate_emissions_with_optimization(self):
        code = """
for i in range(10):
    print(i)
"""
        emissions_optimized = calculate_emissions(code, is_optimized=True)
        emissions_non_optimized = calculate_emissions(code, is_optimized=False)
        self.assertLess(emissions_optimized, emissions_non_optimized)  # Optimized emissions should be lower

if __name__ == "__main__":
    unittest.main()
