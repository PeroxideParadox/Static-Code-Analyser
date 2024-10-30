# utils/labelling_helper.py
import ast

def detect_code_smells_ast(code):
    """
    Detect specific code smells using AST for better accuracy in Python code analysis.
    """
    smells = {
        "nested_loops": 0,
        "repetitive_code": 0,
        "inefficient_algorithms": 0,
        "redundant_computations": 0
    }
    
    # Parse code into an AST
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # If code can't be parsed, skip this file
        return smells

    # Helper function to detect nested loops
    def count_nested_loops(node, depth=0):
        if isinstance(node, (ast.For, ast.While)):
            if depth > 0:
                smells["nested_loops"] += 1
            depth += 1
        for child in ast.iter_child_nodes(node):
            count_nested_loops(child, depth)

    # Helper function to detect repetitive code (functions with similar names and structure)
    def count_repetitive_code(node):
        functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        func_names = [f.name for f in functions]
        smells["repetitive_code"] = len(func_names) - len(set(func_names))

    # Helper function to detect long functions (as inefficient algorithms proxy)
    def count_long_functions(node):
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                func_length = len(n.body)
                if func_length > 15:  # Arbitrary threshold for "long" function
                    smells["inefficient_algorithms"] += 1

    # Helper function to detect redundant computations (like returns of None)
    def count_redundant_computations(node):
        for n in ast.walk(node):
            if isinstance(n, ast.Return) and isinstance(n.value, ast.Constant) and n.value.value is None:
                smells["redundant_computations"] += 1

    # Perform analysis
    count_nested_loops(tree)
    count_repetitive_code(tree)
    count_long_functions(tree)
    count_redundant_computations(tree)

    return smells
