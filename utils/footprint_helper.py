# utils/footprint_helper.py
def calculate_cpu_cycles(smell_count):
    return smell_count * 1000

def calculate_carbon_footprint(cpu_cycles):
    return cpu_cycles * 0.000001 
