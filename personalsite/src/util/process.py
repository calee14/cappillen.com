
def strip_parentheses(string):
    if string.startswith('(') and string.endswith(')'):
        return '-' + string.strip('()')
    return string

def rm_commas_parentheses(string):
    return strip_parentheses(rm_commas(string))

def rm_commas(string):
    return string.replace(',', '')

def rev_to_int(num_str):
    num_str = rm_commas(strip_parentheses(num_str))
    multipliers = {
        'M': 1_000_000, 
        'B': 1_000_000_000, 
        'T': 1_000_000_000_000
    
    }
    suffix = num_str[-1]
    num = float(num_str[:-1])

    if suffix in multipliers:
        num *= multipliers[suffix]

    return int(num)

def eps_to_float(num_str):
    num_str = rm_commas(strip_parentheses(num_str))
    return float(num_str)