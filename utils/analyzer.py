import re

def analyze_code(code):
    lines = code.strip().split("\n")
    num_lines = len(lines)

    num_loops = len(re.findall(r"\b(for|while)\b", code))
    num_conditions = len(re.findall(r"\b(if|elif|else)\b", code))

    indentation_levels = [
        len(line) - len(line.lstrip())
        for line in lines if line.strip()
    ]

    max_depth = max(indentation_levels) // 4 if indentation_levels else 0

    return {
        "lines": num_lines,
        "loops": num_loops,
        "conditions": num_conditions,
        "depth": max_depth
    }