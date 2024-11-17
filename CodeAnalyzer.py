import ast
import sys
from typing import List, Dict, Tuple

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
        self.issues.sort(key=lambda x: x['line'])
        return self.issues, self.apply_optimizations()

def main():
    # Read input file
    with open("code.py", "r") as f:
        code = f.read()

    # Create analyzer and run analysis
    analyzer = CodeAnalyzer(code)
    issues, optimized_code = analyzer.analyze()

    # Sort issues by line number
    sorted_issues = sorted(issues, key=lambda x: x['line'])

    # Print issues
    print("Running static code analysis...")
    print("\nDetected Issues and Recommendations:")
    for issue in sorted_issues:
        print(f"Line {issue['line']}: {issue['issue']}")
        print(f"Recommendation: {issue['recommendation']}")

    # Save optimized code
    with open("optimized_code.py", "w") as f:
        f.write(optimized_code)

    print("\nOptimized code saved to optimized_code.py")

if __name__ == "__main__":
    main()