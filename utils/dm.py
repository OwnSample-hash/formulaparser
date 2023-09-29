import re

def check_dm1(input_:str):
    pattern = r"(not) \((\w) (and|or) (\w)\)"
    subst = "\\g<1> \\g<2> \\g<3> \\g<1> \\g<4>"
    res = re.sub(pattern, subst, input_, 1)
    if res == input_:
        return input_

    if "and" in input_:
        res = res.replace('and', 'or')
    elif "or" in input_:
        res = res.replace('or', 'and')
    return f"{input_} => {res}"

def check_dm2(input_:str):
    pattern = r"(not) (\w) (and|or) not (\w)"
    subst = "\\g<1> (\\g<2> \\g<3> \\g<4>)"
    res = re.sub(pattern, subst, input_, 1)
    if res == input_:
        return input_   
 
    if "and" in input_:
        res = res.replace('and', 'or')
    elif "or" in input_:
        res = res.replace('or', 'and')
    return f"{input_} => {res}"

def check_dm(input_:str):
    _1 = check_dm1(input_)
    _2 = check_dm2(input_)
    
    if _1 != input_ and _2 != input_:
        # Both _1 and _2 are different from input_
        # You can choose which one to return here; in this example, we return _1
        return _1
    elif _1 != input_:
        # Only _1 is different from input_
        return _1
    elif _2 != input_:
        # Only _2 is different from input_
        return _2
    else:
        # Both _1 and _2 are the same as input_
        return input_

