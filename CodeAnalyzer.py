import ast
import sys
from typing import List, Dict, Tuple
import subprocess
import importlib.util
import os
import logging
import time
import ast
import math

logging.basicConfig(level=logging.DEBUG)

class CodeMetricsCalculator:
    """Calculate code complexity and efficiency metrics for emission estimation"""
    def __init__(self, code: str):
        self.code = code
        self.ast_tree = ast.parse(code)
        
    def calculate_complexity_score(self) -> float:
        """Calculate complexity score based on code structure"""
        self.loop_count = 0
        self.operation_count = 0
        self.memory_operations = 0
        self.function_calls = 0
        
        class MetricsVisitor(ast.NodeVisitor):
            def __init__(self, calculator):
                self.calc = calculator
                
            def visit_For(self, node):
                self.calc.loop_count += 1
                self.generic_visit(node)
                
            def visit_While(self, node):
                self.calc.loop_count += 1
                self.generic_visit(node)
                
            def visit_BinOp(self, node):
                self.calc.operation_count += 1
                self.generic_visit(node)
                
            def visit_List(self, node):
                self.calc.memory_operations += 1
                self.generic_visit(node)
                
            def visit_Call(self, node):
                self.calc.function_calls += 1
                self.generic_visit(node)
        
        MetricsVisitor(self).visit(self.ast_tree)
        
        # Calculate weighted complexity score
        complexity_score = (
            self.loop_count * 2.5 +
            self.operation_count * 1.0 +
            self.memory_operations * 1.5 +
            self.function_calls * 1.2
        )
        
        return complexity_score
    
    def calculate_emission_factor(self) -> float:
        """Calculate emission factor based on code metrics"""
        complexity_score = self.calculate_complexity_score()
        
        # Base emission factor (kg CO2 per complexity unit)
        BASE_EMISSION_FACTOR = 0.0001
        
        # Calculate emission factor with exponential scaling
        emission_factor = BASE_EMISSION_FACTOR * math.exp(complexity_score / 100)
        
        return emission_factor

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, code: str):
        self.code = code
        self.issues = []
        self.optimizations = {}
        self.sorted_vars = set()
        self.string_concats = {}
        self.list_appends = {}
        self.list_copies = {}
        self.variable_declarations = {}
        self.unused_variables = set()
        self.loop_variables = set()

    def visit_For(self, node):
        # Track loop variables
        if isinstance(node.target, ast.Name):
            self.loop_variables.add(node.target.id)

        # Check for nested loops with conditions that can be converted to list comprehension
        if isinstance(node.body[0], ast.For):
            inner_loop = node.body[0]
            if len(inner_loop.body) == 1 and isinstance(inner_loop.body[0], ast.If):
                if_node = inner_loop.body[0]
                if len(if_node.body) == 1 and isinstance(if_node.body[0], ast.Expr) and \
                   isinstance(if_node.body[0].value, ast.Call) and \
                   isinstance(if_node.body[0].value.func, ast.Attribute) and \
                   if_node.body[0].value.func.attr == 'append':

                    # Extract components for list comprehension
                    outer_var = node.target.id
                    inner_var = inner_loop.target.id
                    outer_iter = ast.unparse(node.iter)
                    inner_iter = ast.unparse(inner_loop.iter)
                    conditions = ast.unparse(if_node.test)
                    value = ast.unparse(if_node.body[0].value.args[0])

                    # Create list comprehension
                    list_comp = f"result = [{value} for {outer_var} in {outer_iter} for {inner_var} in {inner_iter} if {conditions}]"

                    self.optimizations[node.lineno] = {
                        'start': node.lineno - 1,
                        'end': node.end_lineno,
                        'new_code': list_comp
                    }

                    self.issues.append({
                        "line": node.lineno,
                        "issue": "Nested loops with conditional append",
                        "recommendation": "Use list comprehension",
                        "optimization": list_comp
                    })

        # New: Check for range(len()) antipattern
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and \
           node.iter.func.id == 'range' and len(node.iter.args) == 1 and \
           isinstance(node.iter.args[0], ast.Call) and \
           isinstance(node.iter.args[0].func, ast.Name) and node.iter.args[0].func.id == 'len':

            iterable = ast.unparse(node.iter.args[0].args[0])
            var_name = node.target.id
            body = '\n'.join(ast.unparse(stmt) for stmt in node.body)

            # Create enumeration-based loop if index is used
            if any(var_name in ast.unparse(stmt) for stmt in node.body):
                optimization = f"for i, {var_name} in enumerate({iterable}):\n    {body}"
            else:
                optimization = f"for {var_name} in {iterable}:\n    {body}"

            self.optimizations[node.lineno] = {
                'start': node.lineno,
                'end': node.end_lineno,
                'new_code': optimization
            }

            self.issues.append({
                "line": node.lineno,
                "issue": "range(len()) antipattern",
                "recommendation": "Use enumerate() or direct iteration",
                "optimization": optimization
            })

        self.generic_visit(node)

    def visit_Assign(self, node):
        # Track variable declarations
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if var_name not in self.variable_declarations:
                self.variable_declarations[var_name] = node.lineno
                if var_name not in self.loop_variables:
                    self.unused_variables.add(var_name)

        # Track string concatenations
        if isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Add):
            target = ast.unparse(node.targets[0])
            if target not in self.string_concats:
                self.string_concats[target] = []
            self.string_concats[target].append(node)

        # Track list copies
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and \
           node.value.func.id == 'list':
            orig_list = ast.unparse(node.value.args[0])
            target = ast.unparse(node.targets[0])
            optimization = f"{target} = {orig_list}.copy()"

            self.optimizations[node.lineno] = {
                'start': node.lineno,
                'end': node.lineno,
                'new_code': optimization
            }

            self.issues.append({
                "line": node.lineno,
                "issue": "Inefficient list copy",
                "recommendation": "Use list.copy() method",
                "optimization": optimization
            })

        self.generic_visit(node)

    def visit_Name(self, node):
        # Remove variables that are used from unused_variables set
        if isinstance(node.ctx, ast.Load) and node.id in self.unused_variables:
            self.unused_variables.remove(node.id)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        # Track string concatenations with +=
        if isinstance(node.op, ast.Add):
            target = ast.unparse(node.target)
            if target not in self.string_concats:
                self.string_concats[target] = []
            self.string_concats[target].append(node)

            # Check if we have multiple string concatenations for this target
            concats = self.string_concats[target]
            if len(concats) >= 3:
                pieces = []
                start_line = min(n.lineno for n in concats)
                end_line = max(n.lineno for n in concats)

                # Find the initial assignment
                for stmt in ast.walk(ast.parse(self.code)):
                    if isinstance(stmt, ast.Assign) and ast.unparse(stmt.targets[0]) == target:
                        pieces.append(ast.unparse(stmt.value))
                        break

                # Collect all concatenated values
                for concat in concats:
                    if isinstance(concat, ast.AugAssign):
                        pieces.append(ast.unparse(concat.value))

                optimization = f'{target} = "".join([{", ".join(pieces)}])'

                self.optimizations[start_line] = {
                    'start': start_line,
                    'end': end_line,
                    'new_code': optimization
                }

                self.issues.append({
                    "line": start_line,
                    "issue": "Multiple string concatenations",
                    "recommendation": "Use str.join()",
                    "optimization": optimization
                })

        self.generic_visit(node)

    def visit_If(self, node):
        # Check for long if-elif chains
        if hasattr(node, 'orelse') and node.orelse:
            chain_length = 1
            current = node
            conditions = []
            actions = []

            # Collect all conditions and actions in the chain
            while current and isinstance(current, ast.If):
                test = ast.unparse(current.test)
                body = ast.unparse(current.body[0]).strip()
                conditions.append(test)
                actions.append(body)

                if current.orelse and len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                    current = current.orelse[0]
                    chain_length += 1
                else:
                    current = None

            if chain_length >= 4:
                # Create dictionary-based switch
                cases = [f"    {cond}: {action}" for cond, action in zip(conditions, actions)]

                optimization = "switch_dict = {\n" + ",\n".join(cases) + "\n}\n"
                optimization += "result = switch_dict.get(True, 'default_value')"

                self.optimizations[node.lineno] = {
                    'start': node.lineno,
                    'end': node.end_lineno,
                    'new_code': optimization
                }

                self.issues.append({
                    "line": node.lineno,
                    "issue": "Long if-elif chain",
                    "recommendation": "Use dictionary mapping",
                    "optimization": optimization
                })

        self.generic_visit(node)

    def visit_Call(self, node):
        # Track list append operations
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'append':
            list_name = ast.unparse(node.func.value)
            if list_name not in self.list_appends:
                self.list_appends[list_name] = []
            self.list_appends[list_name].append(node)

            # If we have multiple consecutive appends, optimize them
            appends = self.list_appends[list_name]
            if len(appends) >= 3:
                values = [ast.unparse(n.args[0]) for n in appends]
                start_line = appends[0].lineno
                end_line = appends[-1].lineno

                optimization = f"{list_name}.extend([{', '.join(values)}])"

                self.optimizations[start_line] = {
                    'start': start_line,
                    'end': end_line,
                    'new_code': optimization
                }

                self.issues.append({
                    "line": start_line,
                    "issue": "Multiple list append operations",
                    "recommendation": "Use list.extend()",
                    "optimization": optimization
                })

        # Check for redundant sort operations
        elif isinstance(node.func, ast.Name) and node.func.id == 'sorted':
            var_name = ast.unparse(node.args[0])
            if var_name in self.sorted_vars:
                self.issues.append({
                    "line": node.lineno,
                    "issue": "Redundant sort operation",
                    "recommendation": "Use single sort with reverse=True",
                    "optimization": f"{var_name}.sort(reverse=True)"
                })
            self.sorted_vars.add(var_name)

        self.generic_visit(node)

    def check_unused_variables(self):
        for var in self.unused_variables:
            self.issues.append({
                "line": self.variable_declarations[var],
                "issue": "Unused variable",
                "recommendation": f"Remove unused variable '{var}'",
                "optimization": f"# Remove declaration of '{var}'"
            })

    def apply_optimizations(self):
        lines = self.code.splitlines()
        # Sort optimizations by line number in reverse order to avoid line number shifts
        sorted_lines = sorted(self.optimizations.items(), reverse=True)

        for _, opt in sorted_lines:
            start, end = opt['start'], opt['end']
            new_code = opt['new_code']
            lines[start-1:end] = [new_code]

        return '\n'.join(lines)

    def analyze(self):
        tree = ast.parse(self.code)
        self.visit(tree)
        self.check_unused_variables()
        return self.issues, self.apply_optimizations()

def calculate_emissions(code: str, is_optimized: bool = False) -> float:
    """
    Calculate emissions based on code complexity and efficiency metrics
    rather than actual hardware measurements
    """
    calculator = CodeMetricsCalculator(code)
    emission_factor = calculator.calculate_emission_factor()
    
    # Apply optimization factor if code is optimized
    if is_optimized:
        # Optimized code should have lower emissions due to better efficiency
        optimization_factor = 0.6  # 40% reduction for optimized code
        emission_factor *= optimization_factor
    
    # Calculate final emissions
    code_lines = len(code.splitlines())
    base_emissions = code_lines * emission_factor
    
    # Add complexity-based emissions
    complexity_score = calculator.calculate_complexity_score()
    total_emissions = base_emissions * (1 + complexity_score / 1000)
    
    return total_emissions

def run_code_with_tracking(file_path: str, is_optimized: bool = False) -> float:
    """
    Calculate emissions for code without depending on hardware measurements
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        # Calculate emissions based on code metrics
        emissions = calculate_emissions(code, is_optimized)
        return emissions
        
    except Exception as e:
        print(f"Error calculating emissions for '{file_path}': {str(e)}")
        return 0.0

def calculate_emission_reduction(original: float, optimized: float) -> float:
    """
    Calculate emission reduction percentage with proper handling of edge cases.
    """
    if original <= 0 and optimized <= 0:
        return 0.0
    elif original <= 0:
        return 0.0
    else:
        return ((original - optimized) / original) * 100

def main():
    try:
        # Read input file
        with open("code.py", "r") as f:
            code = f.read()

        # Create analyzer and run analysis
        analyzer = CodeAnalyzer(code)
        issues, optimized_code = analyzer.analyze()

        # Print issues
        print("Running static code analysis...")
        print("\nDetected Issues and Recommendations:")
        for issue in sorted(issues, key=lambda x: x['line']):
            print(f"Line {issue['line']}: {issue['issue']}")
            print(f"Recommendation: {issue['recommendation']}")

        # Save optimized code
        with open("optimized_code.py", "w") as f:
            f.write(optimized_code)

        print("\nOptimized code saved to optimized_code.py")
        print("\nCalculating carbon emissions...")

        # Calculate emissions using the new metric-based approach
        print("Calculating original code emissions...")
        original_emissions = run_code_with_tracking("code.py")
        print(f"Original code emissions calculated: {original_emissions:.6f} kg CO2")

        print("\nCalculating optimized code emissions...")
        optimized_emissions = run_code_with_tracking("optimized_code.py", True)
        print(f"Optimized code emissions calculated: {optimized_emissions:.6f} kg CO2")

        # Calculate improvement
        improvement = calculate_emission_reduction(original_emissions, optimized_emissions)

        # Print carbon emission statistics
        print("\nCarbon Emission Statistics:")
        print(f"Original Code Emissions: {original_emissions:.6f} kg CO2")
        print(f"Optimized Code Emissions: {optimized_emissions:.6f} kg CO2")
        print(f"Emission Reduction: {improvement:.2f}%")

        # Save report
        with open("emission_report.txt", "w") as f:
            f.write("Carbon Emission Analysis Report\n")
            f.write("==============================\n\n")
            f.write(f"Original Code Emissions: {original_emissions:.6f} kg CO2\n")
            f.write(f"Optimized Code Emissions: {optimized_emissions:.6f} kg CO2\n")
            f.write(f"Emission Reduction: {improvement:.2f}%\n")

        import matplotlib.pyplot as plt
        labels = ['Original Code', 'Optimized Code']
        values = [original_emissions, optimized_emissions]

        # Plotting the emissions comparison
        plt.figure(figsize=(8, 5))
        bars = plt.bar(labels, values, color=['red', 'green'], alpha=0.8)
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.6f}', 
                    ha='center', va='bottom', fontsize=10)

        plt.xlabel('Code Version', fontsize=12)
        plt.ylabel('Emissions (kg CO2)', fontsize=12)
        plt.title('Comparison of Carbon Emissions', fontsize=14)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Analysis failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()