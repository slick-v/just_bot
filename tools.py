def caluculator(expression:str):
    try:
        return str(eval(expression))
    except:
        return "invalid expression"