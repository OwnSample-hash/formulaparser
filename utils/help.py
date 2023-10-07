def help():
    print(
        """q to quit
re to resize table
w to save the last expr.
r to reevaluate last expression
p to print out the table
m to toggle more info about the expr.
let <expr. ref. name> <expr.> to add new expr
list [r|p] to list stored expr. [raw or parsed] form
del <expr. ref. name> to delete stored expr.
eval to evalute the stored expr.
q or eof to quit
? to help"""
    )
