#define custom exception to call
class Parser_Error(Exception):
    '''This class creates the custom exception'''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
#token class
class Token():
    def __init__(self, token, token_type):
        self.token = token
        self.token_type = token_type
        self.type = 'token'
    def print_vars(self):
        print(self.token, self.token_type, self.location)
#class to make if cache work better
class If_Block():
    def __init__(self):
        self.type = 'if_block'
#classes for output elements
class If_statement():
    def __init__(self, comparison, statement):
        self.comparison = comparison 
        self.statement = statement
        self.true = False
        self.type = 'if'
class Elif_statement():
    def __init__(self, comparison, statement, parent):
        self.comparison = comparison 
        self.statement = statement
        self.parent = parent
        self.true = False
        self.type = 'elif'
class Then_statement():
    def __init__ (self, statement):
        self.statement = statement
        self.type = 'then'
class Else_statement():
    def __init__ (self, statement, parent):
        self.statement = statement
        self.parent = parent
        self.type = 'else'
class Function():
    def __init__(self, name, args, statement, return_type):
        self.name = name
        self.args = args
        self.statement = statement
        self.return_type = return_type
        self.type = 'function'
class Class():
    def __init__(self, name, parents, functions):
        self.name = name
        self.parents = parents
        self.functions = functions
        self.type = 'class'
class Make_Class_Instance():
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.type = 'make_class_instance'
class While_Loop():
    def __init__(self, comparison, statement):
        self.comparison = comparison
        self.statement = statement
        self.type = 'while'
class For_Loop():
    def __init__(self, var, for_type, values, statement):
        self.var = var
        self.for_type = for_type
        self.values = values
        self.statement = statement
        self.type = 'for'
class Free_statement():
    def __init__ (self, var):
        self.var = var
        self.type = 'free'
class Make_statement():
    def __init__ (self, var_type, var, value):
        self.var_type = var_type
        self.var = var
        self.value = value
        self.type = 'make'
class Changer():
    def __init__(self, value, output):
        self.value = value
        self.output = output
        self.type = 'changer'
class Run_Func():
    '''Functions on variable objects'''
    def __init__(self, value, output):
        self.value = value
        self.output = output
        self.type = 'run_func'
class Custom_Func():
    '''For running lone functions'''
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.type = 'custom_func'
class Class_Func():
    '''For running functions that are part of a class'''
    def __init__(self, instance, name, args):
        self.instance = instance
        self.name = name
        self.args = args
class Return():
    def __init__(self, value):
        self.value = value
        self.type = 'return'
class Comparison():
    def __init__(self, left, comp, right):
        self.left = left
        self.comp_op = comp 
        self.right = right
        self.type = 'comp'
class Equation():
    def __init__(self, postfix):
        self.postfix = postfix
        self.type = 'equation'
    def print_postfix(self):
        for token in self.postfix:
            print(token.token)
class Display():
    def __init__(self, value):
        self.value = value
        self.type = 'display'
class Input():
    def __init__(self, string=Token('', 'str')):
        self.type = 'input'
        self.string = string
#main parser function
def parser(tokens, console_index, input_string):
    #line will be contained in a list
    syntax_tree = []
    current_index = 0
    def braketed_expression():
        '''Checks what type of brackated expression it is'''
        #first check if there is just a float next 
        if len(tokens) <= current_index + 2:
            return 'float'
        elif (tokens[current_index + 1].token_type == 'flt' or tokens[current_index + 1].token_type == 'var') and tokens[current_index + 2].token_type == 'op':
            return 'equation'
        else:
            return 'comparison'
    #return boolean if next token is the same as inputed token
    def accept_token(token):
        '''returns boolean if next token is given token'''
        nonlocal current_index
        if token == tokens[current_index].token:
            current_index += 1
            return True
        else:
            return False
    #return boolean if next token has the same type as the inputted type
    def accept_type(token_type):
        '''returns boolen if next token is the given token type'''
        nonlocal current_index
        if token_type == tokens[current_index].token_type:
            current_index += 1
            return True
        else:
            return False
    #error if next token is not the same as input
    def expect(token, console_index, error_type='Syntax'):
        '''raises error if expected token is not next token'''
        nonlocal current_index
        #check if equal, else raise error
        if token == tokens[current_index].token:
            current_index += 1
            return tokens[current_index - 1]
        else:
            error_token = tokens[current_index]
            out_length = len(f'[Out_{console_index}]: ')
            #allows for diffferent errors to occur
            match error_type:
                case 'Syntax':
                    print(f'[Out_{console_index}]: Syntax Error: Expected {token}')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (error_token.location - len(error_token.token)) + '^' * len(error_token.token))
            raise Parser_Error('')
    #error if next token is not the same as input
    def expect_type(token_types, console_index, error_type='Type'):
        '''Raises error if expected type isn't next token'''
        nonlocal current_index
        #check if types are equal, else raise error
        if tokens[current_index].token_type in token_types:
            current_index += 1
            return tokens[current_index - 1]
        else:
            error_token = tokens[current_index]
            out_length = len(f'[Out_{console_index}]: ')
            #allows for diffferent errors to occur
            match error_type:
                case 'Type':
                    print(f'[Out_{console_index}]: Type Error: {tokens[current_index].token} is not a {token_types}')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (error_token.location - len(error_token.token)) + '^' * len(error_token.token))
            raise Parser_Error('')
    #function to create statements
    def statement():
        '''Makes Statement Objects'''
        if len(tokens) == current_index:
            return
        #create if statement
        if accept_token('if'):
            comp = arrange_comps()
            #check if then is the next token
            expect('then', console_index)
            st = statement()
            return If_statement(comp, st)
        elif accept_token('elif'):
            comp = arrange_comps()
            #check if then is the next token
            expect('then', console_index)
            st = statement()
            return Elif_statement(comp, st)
        #create then statement
        elif accept_token('then'):
            st = statement()
            return Then_statement(st)
        #create else statement
        elif accept_token('else'):
            st = statement()
            return Else_statement(st)
        #create make statement
        elif accept_token('make'):
            var_type, var, value = create_make()
            return Make_statement(var_type, var, value)
        #display statements
        elif accept_token('display'):
            value = create_display()
            return Display(value)
    def create_display():
        '''Creates Display Objects'''
        nonlocal current_index
        if accept_type('var'):
            value = tokens[current_index - 1]
        elif accept_type('flt'):
            current_index -= 1
            if braketed_expression() == 'equation':
                value = equation()
            else:
                value = expect_type('flt', console_index)
        elif accept_token('('):
            current_index -= 1
            if braketed_expression == 'equation':
                value = equation()
            else:
                current_index += 1
                value = tokens[current_index - 1]
        elif accept_type('str'):
            value = tokens[current_index - 1]
        elif accept_type('bool'):
            value = tokens[current_index - 1]
        elif accept_token('{'):
            value = create_array()
        elif accept_token('['):
            value = create_changer()
        else:
            print(f'[Out_{console_index}]: Syntax Error: {tokens[current_index].token} is not able to be displayed')
            out_length = len(f'[Out_{console_index}]: ')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (tokens[current_index].location - len(tokens[current_index].token)) + '^' * len(tokens[current_index].token))
            raise Parser_Error('')
        return value
    def create_make():
        '''Makes Make Statement Objects'''
        nonlocal current_index
        var_type = expect_type('type', console_index)
        var_name = expect_type('var', console_index)
        expect('=', console_index)
        #arrays need to be parsed
        if var_type.token == 'array':
            #check for {
            expect('{', console_index)
            value = create_array()
        #check if changer is being used. Interpreter will do type check
        elif accept_token('['):
            value = create_changer()
        #allow setting variables to equal comparisons
        elif var_type.token == 'bool':
            if accept_token('('):
                current_index -= 1
                if braketed_expression() == 'comparison':
                    #current_index += 1
                    value = arrange_comps()
                else:
                    current_index += 1
                    #this will throw an error because there is no comparison
                    value = expect_type(var_type.token, console_index)
            else:
                current_index -= 1
                if braketed_expression() == 'comparison':
                    #current_index += 1
                    value = arrange_comps()
                else:
                    #checking for bracketed comparison doesn't push up index but should
                    current_index += 1
                    value = expect_type(var_type.token, console_index)
        #allows equations to be used as input
        elif var_type.token == 'flt':
            if accept_token('('):
                current_index -= 1
                if braketed_expression() == 'equation':
                    #current_index += 1
                    value = equation()
                else:
                    current_index += 1
                    #this will throw an error because there is no equation
                    value = expect_type(var_type.token, console_index)
            else:
                current_index -= 1
                if braketed_expression() == 'equation':
                    current_index += 1
                    value = equation()
                else:
                    #checking for bracketed equation doesn't push up index but should
                    current_index += 1
                    value = expect_type(var_type.token, console_index)
        else:
            #check for right type if not array or equation
            value = expect_type(var_type.token, console_index)
        return var_type, var_name, value
    def create_changer():
        '''Create Changer Object'''
        nonlocal current_index
        #look for input 
        if accept_type('var'):
            value = tokens[current_index - 1]
        elif accept_type('flt'):
            value = tokens[current_index - 1]
        elif accept_type('str'):
            value = tokens[current_index - 1]
        elif accept_token('{'):
            value = create_array()
        elif accept_token('['):
            value = create_changer()
        else:
            print(f'[Out_{console_index}]: Type Error: {tokens[current_index].token} is not a valid type to be converted')
            out_length = len(f'[Out_{console_index}]: ')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (tokens[current_index].location - len(tokens[current_index].token)) + '^' * len(tokens[current_index].token))
            raise Parser_Error('')
        #check for seperator comma
        expect(',', console_index)
        #get what output should be
        #check for flt for string splicing/getting value from array
        if accept_type('flt'):
            output = tokens[current_index - 1]
        elif accept_type('keyword'):
            current_index -= 1
            #only get or len keywords are allowed
            if accept_token('get'):
                output = tokens[current_index - 1]
            elif accept_token('len'):
                output = tokens[current_index - 1]
            else:
                print(f'[Out_{console_index}]: Syntax Error: Expected get or len')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (tokens[current_index].location - len(tokens[current_index].token)) + '^' * len(tokens[current_index].token))
                raise Parser_Error('')
        else:
            output = expect_type('type', console_index)
            #make sure output is not var type - can't convert to variable type 
            if output.token == 'var':
                print(f'[Out_{console_index}]: Type Error: {tokens[current_index].token} is not a valid type to be converted to')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (tokens[current_index].location - len(tokens[current_index].token)) + '^' * len(tokens[current_index].token))
                raise Parser_Error('')
        expect(']', console_index)
        return Changer(value, output)
    def create_array():
        '''Creates Arrays'''
        array = []
        while True:
            if accept_type('var'):
                array.append(tokens[current_index - 1])
            elif accept_type('flt'):
                array.append(tokens[current_index - 1])
            elif accept_type('str'):
                array.append(tokens[current_index - 1])
            elif accept_type('bool'):
                array.append(tokens[current_index - 1])
            elif accept_token('{'):
                array.append(create_array())
            else:
                print(f'[Out_{console_index}]: Type Error: {tokens[current_index].token} is not a valid type ({tokens[current_index].token_type}) for array')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (tokens[current_index].location - len(tokens[current_index].token)) + '^' * len(tokens[current_index].token))
                raise Parser_Error('')
            #getout clause
            if accept_token('}'):
                break
            #check for comma seperator
            expect(',', console_index)
        return Token(array, 'array')
    #function to create comparisons
    def comparison():
        nonlocal current_index
        '''Creates Comparison Objects'''
        if len(tokens) == current_index:
            return
        left = expect_type(['var', 'flt', 'str', 'bool'], console_index)
        comp = expect_type(['comp'], console_index)
        right = expect_type(['var', 'flt', 'str', 'bool', 'orderer'], console_index)
        #makeing sure that right is not a bracketed equation
        if right.token == '(':
            current_index -= 1
            #check comparison or equation
            if braketed_expression() == 'comparison':
                current_index += 1
                right = bracket_comps()
            elif braketed_expression() == 'equation':
                right = equation()
        #make sure valid comparison operator is used
        if comp.token != '==' and comp.token != '!=':
            #check if they are both floats
            if (left.token_type != 'flt' or right.token_type != 'flt'):
                #check if they are both variables
                if (left.token_type != 'var' or right.token_type != 'var'):
                    #raise error if wrong comparison is used for a number
                    print(f'[Out_{console_index}]: Type Error: {comp.token} is not supported for non number instances')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (comp.location - len(comp.token)) + '^' * len(comp.token_type))
                    raise Parser_Error('')
        return Comparison(left, comp, right)
    def bracket_comps():
        '''Create Comparison Object For Bracketed Comparisons'''
        nonlocal current_index
        comps = []
        while not accept_token(')'):
            if len(tokens) == current_index:
                print('error')
                break
            #check for bracket
            if accept_token('('):
                current_index -= 1
                #check comparison or equation
                if braketed_expression() == 'comparison':
                    current_index += 2
                    comps.append(bracket_comps())
                elif braketed_expression() == 'equation':
                    comps.append(equation())
            else:
                comps.append(comparison())
            #combined comparison if 'and' or 'or' is found
            if accept_token('and'):
                #create new token for or
                comp = Token('and', 'keyword')
                #check for bracket
                if accept_token('('):
                    #check comparison or equation
                    if braketed_expression() == 'comparison':
                        current_index += 1
                        comps.append(bracket_comps())
                    elif braketed_expression() == 'equation':
                        comps.append(equation())
                else:
                    comps.append(comparison())
                #combined curent comparisons
                complex_comp = Comparison(comps[0], comp, comps[1])
                comps = [complex_comp]
            elif accept_token('or'):
                #create new token for or
                comp = Token('or', 'keyword')
                #check for bracket
                if accept_token('('):
                    #check comparison or equation
                    if braketed_expression() == 'comparison':
                        current_index += 1
                        comps.append(bracket_comps())
                    elif braketed_expression() == 'equation':
                        comps.append(equation())
                else:
                    comps.append(comparison())
                #combined curent comparisons
                complex_comp = Comparison(comps[0], comp, comps[1])
                comps = [complex_comp]
            elif accept_type('comp'):
                    #get token for the compairson
                    comp = tokens[current_index -1]
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            #current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        #check if there is only 1 charachter after (i.e (3 + 1) == 4)
                        if tokens[current_index + 1].token == 'then' or tokens[current_index + 1].token == ')':
                            comps.append(tokens[current_index])
                            current_index += 1
                        elif braketed_expression() == 'comparison':
                            comps.append(comparison())
                        else:
                            comps.append(tokens[current_index])
                            current_index += 1
            elif accept_token(')'):
                break
            else:
                print('error')
        #return the single comparison object
        return comps[0]
    def arrange_comps():
        '''Makes full comparison objects'''
        nonlocal current_index
        comps = []
        #loop until comparison statement is finished
        while True:
            if accept_token('('):
                #loop until no tokens or closing bracket is found
                #check comparison or equation
                current_index -= 1
                if braketed_expression() == 'comparison':
                    current_index += 1
                    comps.append(bracket_comps())
                elif braketed_expression() == 'equation':
                    comps.append(equation())
                #combined comparison if 'and' or 'or' or comparison is found
                if accept_type('comp'):
                    #get token for the compairson
                    comp = tokens[current_index - 1]
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1 
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        #check if there is only 1 charachter after (i.e (3 + 1) == 4)
                        if tokens[current_index + 1].token == 'then':
                            comps.append(tokens[current_index])
                            current_index += 1
                        elif braketed_expression() == 'comparison':
                            comps.append(comparison())
                        else:
                            comps.append(tokens[current_index])
                            current_index += 1
                    #create complex comparison
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                elif accept_token('and'):
                    #create new token for and
                    comp = Token('and', 'keyword')
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            #current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        comps.append(comparison())
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                elif accept_token('or'):
                    #create new token for or
                    comp = Token('or', 'keyword')
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                           # current_index += 2
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        comps.append(comparison())
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                elif accept_token('then'):
                    current_index -= 1
                    break
                elif accept_token(')'):
                    pass
                else:
                    break
            #if no bracket check for type
            else:
                #break loop if then is found
                if accept_token('then'):
                    current_index -= 1
                    break
                #combined comparison if 'and' or 'or' or comparison operator is found
                if accept_type('comp'):
                    #get token for the compairson
                    comp = tokens[current_index -1]
                    #check for bracket
                    if accept_token('('):
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        if braketed_expression() == 'comparison':
                            comps.append(comparison())
                        else:
                            comps.append(tokens[current_index - 1])
                    #create complex comparison
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                else:
                    comps.append(comparison())
                if accept_token('and'):
                    #create new token for and
                    comp = Token('and', 'keyword')
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            #current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        comps.append(comparison())
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                elif accept_token('or'):
                    #create new token for or
                    comp = Token('or', 'keyword')
                    #check for bracket
                    if accept_token('('):
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        comps.append(comparison())
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                else:
                    break
        return comps[0]
    def equation():
        '''Uses Shunting Yard Algorithm'''
        output = []
        operator_stack = []
        #define presedence for operators
        presedence = {
                    '+': 1,
                    '-': 1,
                    '*': 2,
                    '/': 2,
                    '**': 3,
                    '(': 0, #not an operator, but required so the code doesn't break
                    }
        while True:
            #check if all charachters have been used
            if len(tokens) == current_index:
                break
            else:
                current_token = tokens[current_index]
                if accept_type('flt'):
                    #add token (previous due to accept type increseing counter) to output
                    output.append(current_token)
                elif accept_type('var'):
                    #add token (previous due to accept type increseing counter) to output
                    output.append(current_token)
                elif accept_type('op'):
                    while True:
                        if len(operator_stack) == 0:
                            operator_stack.append(current_token)
                            break
                        #check if presedence is greater
                        elif presedence[current_token.token] > presedence[operator_stack[-1].token]:
                            operator_stack.append(current_token)
                            break
                        #check if equal and right associative -> only ** is right associative in this console
                        elif current_token.token == '**' and operator_stack[-1].token == '**':
                            operator_stack.append(current_token)
                            break
                        else:
                            output.append(operator_stack.pop())
                elif accept_token('('):
                    operator_stack.append(current_token)
                elif accept_token(')'):
                    while True:
                        #break if left paren is found
                        if operator_stack[-1].token == '(':
                            operator_stack.pop()
                            break
                        #otherwise push to output
                        else:
                            output.append(operator_stack.pop())
                else:
                    #end loop if a non math charachter is found
                    break
        #add all remaining operators to output
        while len(operator_stack) > 0:
            output.append(operator_stack.pop())
        return Equation(output)
    #loop until all tokens are used
    while len(tokens) > current_index:
        #check what next group of tokens will be
        if len(tokens) == 1:
            syntax_tree.append(Display(tokens[current_index]))
            current_index += 1 
        elif accept_type('keyword'):
            current_index -= 1
            syntax_tree.append(statement())
        elif accept_type('flt'):
            current_index -= 1 
            syntax_tree.append(equation())
        elif accept_type('var'):
            current_index -= 1 
            syntax_tree.append(equation())
        elif accept_token('('):
            current_index -= 1 
            syntax_tree.append(equation())
        elif braketed_expression() == 'equation':
            current_index -= 1 
            syntax_tree.append(equation())
        #error if there are no matches
        else:
            print(f'[Out_{console_index}]: Syntax Error: Unexpected Token')
            out_length = len(f'[Out_{console_index}]: ')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (tokens[current_index].location - len(tokens[current_index].token)) + '^' * len(tokens[current_index].token))
            raise Parser_Error('')
    #return final syntax tree
    return syntax_tree
#main parser function for files
def file_parser(tokens, console_index, input_string):
    def braketed_expression():
        '''Checks what type of brackated expression it is'''
        #first check if there is just a float next 
        if len(tokens[line]) <= current_index + 2:
            return 'float'
        elif (tokens[line][current_index + 1].token_type == 'flt' or tokens[line][current_index + 1].token_type == 'var') and tokens[line][current_index + 2].token_type == 'op':
            return 'equation'
        else:
            return 'comparison'
    def equation():
        '''Uses Shunting Yard Algorithm'''
        nonlocal current_index
        output = []
        operator_stack = []
        #define presedence for operators
        presedence = {
                    '+': 1,
                    '-': 1,
                    '*': 2,
                    '/': 2,
                    '%': 2,
                    '**': 3,
                    '(': 0, #not an operator, but required so the code doesn't break
                    }
        while True:
            #check if all charachters have been used
            if len(tokens[line]) == current_index:
                break
            else:
                current_token = tokens[line][current_index]
                if accept_type('flt'):
                    #add token (previous due to accept type increseing counter) to output
                    output.append(current_token)
                elif accept_type('var'):
                    #add token (previous due to accept type increseing counter) to output
                    output.append(current_token)
                elif accept_type('op'):
                    while True:
                        if len(operator_stack) == 0:
                            operator_stack.append(current_token)
                            break
                        #check if presedence is greater
                        elif presedence[current_token.token] > presedence[operator_stack[-1].token]:
                            operator_stack.append(current_token)
                            break
                        #check if equal and right associative -> only ** is right associative in this console
                        elif current_token.token == '**' and operator_stack[-1].token == '**':
                            operator_stack.append(current_token)
                            break
                        else:
                            output.append(operator_stack.pop())
                elif accept_token('('):
                    #accept_token increases current index
                    current_index -= 1
                    operator_stack.append(current_token)
                elif accept_token(')'):
                    current_index -= 1
                    while True:
                        #break if left paren is found
                        if operator_stack[-1].token == '(':
                            operator_stack.pop()
                            break
                        #otherwise push to output
                        else:
                            output.append(operator_stack.pop())
                else:
                    #end loop if a non math charachter is found
                    break
                current_index += 1
        #add all remaining operators to output
        while len(operator_stack) > 0:
            output.append(operator_stack.pop())
        return Equation(output)
    #function to create comparisons
    def comparison():
        nonlocal current_index
        '''Creates Comparison Objects'''
        if len(tokens[line]) == current_index:
            return
        left = expect_type(['var', 'flt', 'str', 'bool'], console_index)
        comp = expect_type(['comp'], console_index)
        right = expect_type(['var', 'flt', 'str', 'bool', 'orderer'], console_index)
        #makeing sure that right is not a bracketed equation. Left will have been grabbed before this by arrange_comps()
        if right.token == '(':
            current_index -= 1
            #check comparison or equation
            if braketed_expression() == 'comparison':
                current_index += 1
                right = bracket_comps()
            elif braketed_expression() == 'equation':
                right = equation()
        #make sure valid comparison operator is used
        if comp.token != '==' and comp.token != '!=':
            #check if they are both floats or variables
            if (not left.token_type in {'var', 'flt'}) or (not right.token_type in {'var', 'flt'}):
                #raise error if wrong comparison is used for a number
                print(f'[Out_{console_index}]: Type Error: {comp.token} is not supported for non number instances')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (comp.location - len(comp.token)) + '^' * len(comp.token_type))
                raise Parser_Error('')
        return Comparison(left, comp, right)
    def bracket_comps():
        '''Create Comparison Object For Bracketed Comparisons'''
        nonlocal current_index
        comps = []
        while not accept_token(')'):
            if len(tokens) == current_index:
                print('error')
                break
            #check for bracket
            if accept_token('('):
                current_index -= 1
                #check comparison or equation
                if braketed_expression() == 'comparison':
                    current_index += 2
                    comps.append(bracket_comps())
                elif braketed_expression() == 'equation':
                    comps.append(equation())
            else:
                comps.append(comparison())
            #combined comparison if 'and' or 'or' is found
            if accept_token('and'):
                #create new token for or
                comp = Token('and', 'keyword')
                #check for bracket
                if accept_token('('):
                    #check comparison or equation
                    if braketed_expression() == 'comparison':
                        current_index += 1
                        comps.append(bracket_comps())
                    elif braketed_expression() == 'equation':
                        comps.append(equation())
                else:
                    comps.append(comparison())
                #combined curent comparisons
                complex_comp = Comparison(comps[0], comp, comps[1])
                comps = [complex_comp]
            elif accept_token('or'):
                #create new token for or
                comp = Token('or', 'keyword')
                #check for bracket
                if accept_token('('):
                    #check comparison or equation
                    if braketed_expression() == 'comparison':
                        current_index += 1
                        comps.append(bracket_comps())
                    elif braketed_expression() == 'equation':
                        comps.append(equation())
                else:
                    comps.append(comparison())
                #combined curent comparisons
                complex_comp = Comparison(comps[0], comp, comps[1])
                comps = [complex_comp]
            elif accept_type('comp'):
                    #get token for the compairson
                    comp = tokens[current_index -1]
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            #current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        #check if there is only 1 charachter after (i.e (3 + 1) == 4)
                        if tokens[current_index + 1].token == 'then' or tokens[current_index + 1].token == ')':
                            comps.append(tokens[current_index])
                            current_index += 1
                        elif braketed_expression() == 'comparison':
                            comps.append(comparison())
                        else:
                            comps.append(tokens[current_index])
                            current_index += 1
            elif accept_token(')'):
                break
            else:
                print('error')
        #return the single comparison object
        return comps[0]
    def arrange_comps():
        '''Makes full comparison objects'''
        nonlocal current_index
        comps = []
        #loop until comparison statement is finished
        while True:
            if accept_token('('):
                #loop until no tokens or closing bracket is found
                #check comparison or equation
                current_index -= 1
                if braketed_expression() == 'comparison':
                    current_index += 1
                    comps.append(bracket_comps())
                elif braketed_expression() == 'equation':
                    comps.append(equation())
                #combined comparison if 'and' or 'or' or comparison is found
                if accept_type('comp'):
                    #get token for the compairson
                    comp = tokens[current_index - 1]
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1 
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        #check if there is only 1 charachter after (i.e (3 + 1) == 4)
                        if tokens[current_index + 1].token == 'then':
                            comps.append(tokens[current_index])
                            current_index += 1
                        elif braketed_expression() == 'comparison':
                            comps.append(comparison())
                        else:
                            comps.append(tokens[current_index])
                            current_index += 1
                    #create complex comparison
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                elif accept_token('and'):
                    #create new token for and
                    comp = Token('and', 'keyword')
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            #current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        comps.append(comparison())
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                elif accept_token('or'):
                    #create new token for or
                    comp = Token('or', 'keyword')
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                           # current_index += 2
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        comps.append(comparison())
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                elif accept_token('then') or accept_token('do'):
                    current_index -= 1
                    break
                elif accept_token(')'):
                    pass
                else:
                    break
            #if no bracket check for type
            else:
                #break loop if then is found
                if accept_token('then') or accept_token('do'):
                    current_index -= 1
                    break
                #combined comparison if 'and' or 'or' or comparison operator is found
                if accept_type('comp'):
                    #get token for the compairson
                    comp = tokens[current_index -1]
                    #check for bracket
                    if accept_token('('):
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        if braketed_expression() == 'comparison':
                            comps.append(comparison())
                        else:
                            comps.append(tokens[current_index - 1])
                    #create complex comparison
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                else:
                    comps.append(comparison())
                #check if comparison is 'and'ed or 'or'ed
                if accept_token('and'):
                    #create new token for and
                    comp = Token('and', 'keyword')
                    #check for bracket
                    if accept_token('('):
                        current_index -= 1
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            #current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        comps.append(comparison())
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                elif accept_token('or'):
                    #create new token for or
                    comp = Token('or', 'keyword')
                    #check for bracket
                    if accept_token('('):
                        #check comparison or equation
                        if braketed_expression() == 'comparison':
                            current_index += 1
                            comps.append(bracket_comps())
                        elif braketed_expression() == 'equation':
                            comps.append(equation())
                    else:
                        comps.append(comparison())
                    complex_comp = Comparison(comps[0], comp, comps[1])
                    comps = [complex_comp]
                else:
                    break
        return comps[0]
    def create_display():
        '''Creates Display Objects'''
        nonlocal current_index
        nonlocal line
        if accept_type('var'):
            value = tokens[line][current_index]
        elif accept_type('flt'):
            #current_index -= 1
            if braketed_expression() == 'equation':
                current_index += 1
                value = equation()
            else:
                value = expect_type('flt', console_index)
        elif accept_token('('):
            current_index -= 1
            if braketed_expression == 'equation':
                value = equation()
            else:
                current_index += 1
                value = tokens[line][current_index]
        elif accept_type('str'):
            value = tokens[line][current_index]
        elif accept_type('bool'):
            value = tokens[line][current_index]
        elif accept_token('{'):
            value = create_array()
        elif accept_token('['):
            value = create_changer()
        else:
            print(f'[Out_{console_index}]: Syntax Error: {tokens[line][current_index].token} is not able to be displayed')
            out_length = len(f'[Out_{console_index}]: ')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (tokens[line][current_index].location - len(tokens[line][current_index].token)) + '^' * len(tokens[line][current_index].token))
            raise Parser_Error('')
        return value
    def create_make():
        '''Makes Make Statement Objects'''
        nonlocal current_index
        used = False
        var_type = expect_type('type', console_index)
        var_name = expect_type('var', console_index)
        expect('=', console_index)
        #allow to get user input set to a variable. This will always be a string, and should be set as so
        if accept_token('input') and var_type.token == 'str':
            if not check_line_end():
                if accept_type('str'):
                    value = Input(string=expect_type('str', console_index))
                else:
                    value = Input()
            else:
                value = Input()
        #check if running function/setting to variable
        elif accept_type('var'):
            current_index += 1
            #check if the line ends after the variable
            if not check_line_end():
                if accept_token('['):
                    #decrement current_index, it was increased to run the checks
                    current_index -= 2
                    name, args = create_func(check_type=False)
                    value = Custom_Func(name, args)
                    #tell next chain of if statements not to run
                    used = True
                #for runnign instances of classes
                elif accept_token('.'):
                    #decrement current_index, it was increased to run checks
                    current_index -= 2
                    #get class instance
                    instance = expect_type('var', console_index)
                    #pass over period
                    expect('.', console_index)
                    name, args = create_func(check_type=False)
                    value = Class_Func(instance, name, args)
                    #tell next chain of if statements to not run
                    used = True
                else:
                    #decrease current index so next options work properly
                    current_index -= 1
            else:
                current_index -= 1
                value = expect_type('var', console_index)
                used = True
        if used == True:
            pass
        #check if instance of class is being made
        elif accept_token('new'):
            #hijacking create_func to get class definition
            name, args = create_func(check_type=False)
            value = Make_Class_Instance(name, args)
        #check if a variable function is being run
        elif accept_type('type') or accept_type('keyword'):
            value = create_run_func()
        #arrays need to be parsed
        elif var_type.token == 'array':
            #check for {
            expect('{', console_index)
            value = create_array()
        #allows equations to be used as input
        elif var_type.token == 'flt':
            if accept_token('('):
                current_index -= 1
                if braketed_expression() == 'equation':
                    value = equation()
                else:
                    current_index += 1
                    #this will throw an error because there is no equation
                    value = expect_type(var_type.token, console_index)
            else:
                current_index -= 1
                if braketed_expression() == 'equation':
                    current_index += 1
                    value = equation()
                else:
                    #checking for bracketed equation doesn't push up index but should
                    current_index += 1
                    value = expect_type(var_type.token, console_index)
        else:
            #check for right type if not array or equation
            value = expect_type(var_type.token, console_index)
        return var_type, var_name, value
    def create_array():
        '''Creates Arrays'''
        nonlocal current_index
        array = []
        while True:
            if accept_type('var'):
                array.append(tokens[line][current_index])
            elif accept_type('flt'):
                array.append(tokens[line][current_index])
            elif accept_type('str'):
                array.append(tokens[line][current_index])
            elif accept_type('bool'):
                array.append(tokens[line][current_index])
            elif accept_token('{'):
                array.append(create_array())
                current_index -= 1
            else:
                print(f'[Out_{console_index}]: Type Error: {tokens[current_index].token} is not a valid type ({tokens[current_index].token_type}) for array')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (tokens[current_index].location - len(tokens[current_index].token)) + '^' * len(tokens[current_index].token))
                raise Parser_Error('')
            #increase current index
            current_index += 1
            #getout clause
            if accept_token('}'):
                break
            #check for comma seperator
            expect(',', console_index)
        return Token(array, 'array')
    def create_run_func():
        '''Create Changer Object'''
        nonlocal current_index
        #custom function
        if accept_type('var'):
            pass
        #change type of variable
        elif accept_type('type'):
            output = expect_type('type', console_index)
        #functions on variables
        elif accept_token('len'):
            output = tokens[line][current_index - 1]
        #get type of variable
        elif accept_token('type'):
            output = tokens[line][current_index - 1]
        else:
            print(f'[Out_{console_index}]: Type Error: {tokens[line][current_index].token} is not a valid type to be converted')
            out_length = len(f'[Out_{console_index}]: ')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (tokens[line][current_index].location - len(tokens[current_index].token)) + '^' * len(tokens[line][current_index].token))
            raise Parser_Error('')
        #check for [
        expect('[', console_index)
        #get what output should be
        if accept_type('var'):
            value = expect_type('var', console_index)
        elif accept_type('str'):
            value = expect_type('str',console_index)
        elif accept_token('{'):
            value = create_array()
        elif accept_type('flt'):
            value = expect_type('flt', console_index)
        elif accept_type('bool'):
            value = expect_type('bool', console_index)
        else:
            output = expect_type('type', console_index)
            #make sure output is not var type - can't convert to variable type 
            if output.token == 'var':
                print(f'[Out_{console_index}]: Type Error: {tokens[line][current_index].token} is not a valid type to be converted to')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (tokens[line][current_index].location - len(tokens[line][current_index].token)) + '^' * len(tokens[line][current_index].token))
                raise Parser_Error('')
        expect(']', console_index)
        return Run_Func(value, output)
    def create_free():
        return expect_type('var', console_index)
    def create_for():
        nonlocal current_index
        #current_index += 1
        var = expect_type('var', console_index)
        expect('=', console_index)
        #iterate through array
        if accept_token('in'):
            for_type = 'array'
        #flt - must use start/stop/step
        elif accept_type('flt'):
            for_type = 'num'
            #start/stop/step need to be set to int to be used in loop
            start = int(expect_type('flt', console_index).token)
            expect(',', console_index)
            stop = int(expect_type('flt', console_index).token)
            #step will defult to 1 if not provided
            if accept_token('do'):
                #accept token increases index by 1, have to decrease it
                current_index -= 1
                step = 1
            else:
                expect(',', console_index)
                step = int(expect_type('flt', console_index).token)
            values = [start, stop, step]
        return var, for_type, values
    def create_func(check_type=True):
        nonlocal current_index
        name = expect_type('var', console_index)
        expect('[', console_index)
        #break if no arguments
        args = []
        while not accept_token(']'):
            #allows this to be used for running functions, not just making them
            if check_type:
                arg_type = expect_type('type', console_index)
                arg_name = expect_type('var', console_index)
                arg = {
                    'type': arg_type,
                    'name': arg_name,
                }
                args.append(arg)
                #check for type to return
            else:
                args.append(tokens[line][current_index])
                current_index += 1
            if accept_token(']'):
                break
            else:
                expect(',', console_index)
        #return if running the function
        if check_type == False:
            return name, args
        #check for return type and return if making the fucnton
        else:
            expect('->', console_index)
            return_type = expect_type('type', console_index)
            return name, args, return_type
    def create_class():
        #get name
        name = expect_type('var', console_index)
        expect('[', console_index)
        #loop until closing ] is found
        parents = []
        while not accept_token(']'):
            if accept_type('var'):
                parents.append(expect_type('var', console_index))
                #check for comma
            if accept_token(']'):
                break
            else:
                expect(',', console_index)
        return name, parents
    def create_return():
        nonlocal current_index
        values = []
        #loop through all values being saved
        #getout clause
        if check_line_end():
            values.append(None)
        else:
            values.append(tokens[line][current_index])
            current_index += 1
        return values
    def accept_token(token):
        '''returns boolean if next token is given token'''
        nonlocal current_index
        if token == tokens[line][current_index].token:
            current_index += 1
            return True
        else:
            return False
    #return boolean if next token has the same type as the inputted type
    def accept_type(token_type):
        '''returns boolen if next token is the given token type'''
        nonlocal current_index
        if token_type == tokens[line][current_index].token_type:
            #increase current index here?
            return True
        else:
            return False
    #error if next token is not the same as input
    def expect(token, console_index, error_type='Syntax'):
        '''raises error if expected token is not next token'''
        nonlocal current_index
        #check if equal, else raise error
        if token == tokens[line][current_index].token:
            current_index += 1
            return tokens[line][current_index - 1]
        else:
            error_token = tokens[line][current_index]
            out_length = len(f'[Out_{console_index}]: ')
            #allows for diffferent errors to occur
            match error_type:
                case 'Syntax':
                    print(f'[Out_{console_index}]: Syntax Error: Expected {token}')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (error_token.location - len(error_token.token)) + '^' * len(error_token.token))
            raise Parser_Error('')
    #error if next token is not the same type as input
    def expect_type(token_types, console_index, error_type='Type'):
        '''Raises error if expected type isn't next token'''
        nonlocal current_index
        #check if types are equal, else raise error
        if tokens[line][current_index].token_type in token_types:
            current_index += 1
            return tokens[line][current_index - 1]
        else:
            error_token = tokens[line][current_index]
            out_length = len(f'[Out_{console_index}]: ')
            #allows for diffferent errors to occur
            match error_type:
                case 'Type':
                    print(f'[Out_{console_index}]: Type Error: {tokens[line][current_index].token} is not a {token_types}')
            print(' ' * out_length + input_string)
            print(' ' * out_length + ' ' * (error_token.location - len(error_token.token)) + '^' * len(error_token.token))
            raise Parser_Error('')
    #function to create statements
    def statement():
        nonlocal if_cache
        '''Makes Statement Objects'''
        nonlocal current_index, line
        #create if statement
        if accept_token('if'):
            comp = arrange_comps()
            #check if then is the next token
            expect('then', console_index)
            #move to next line if at end of current line
            change_line_end()
            st = []
            expect('{', console_index)
            #add blocker to if cache, helps with if statements insde the block
            if_cache.append(If_Block())
            change_line_end()
            #loop until closing } is found
            while not accept_token('}'):
                st.append(statement())
                change_line_end()
            clear_if_cache()
            obj = If_statement(comp, st)
            if_cache.append(obj)
            return obj
        elif accept_token('elif'):
            if len(if_cache) > 0:
                #check for parent if
                if isinstance(if_cache[-1], If_statement):
                    parent = if_cache[-1]
                elif isinstance(if_cache[-1], Elif_statement):
                    parent = if_cache[-1]
                #remove previous and add current to if cache
                if_cache.pop()
                comp = arrange_comps()
                #check if then is the next token
                expect('then', console_index)
                #move to next line if at end of current line
                change_line_end()
                st = []
                expect('{', console_index)
                #add blocker to if_cache
                if_cache.append(If_Block())
                change_line_end()
                #loop until closing } is found
                while not accept_token('}'):
                    st.append(statement())
                    change_line_end()
                clear_if_cache()
                obj = Elif_statement(comp, st, parent)
                if_cache.append(obj)
                return obj
        #create else statement
        elif accept_token('else'):
            if len(if_cache) > 0:
                #check for a parent if or elif
                if isinstance(if_cache[-1], If_statement):
                    parent = if_cache[-1]
                elif isinstance(if_cache[-1], Elif_statement):
                    parent = if_cache[-1]
                if_cache.pop()
                #move to next line if at end of current line
                change_line_end()
                expect('{', console_index)
                #add blocker to if cache
                if_cache.append(If_Block)
                change_line_end()
                st = []
                #loop until closing } is found
                while not accept_token('}'):
                    st.append(statement())
                    change_line_end()
                clear_if_cache()
                return Else_statement(st, parent)
        else:
            #clear if cache if there is not an if (if chain is done)
            clear_if_cache()
            #create make statement 
            if accept_token('make'):
                var_type, var, value = create_make()
                return Make_statement(var_type, var, value)
            #create function
            elif accept_token('func'):
                #get name and args
                name, args, return_type = create_func()
                #prep to make block statement
                change_line_end()
                expect('{', console_index)
                change_line_end()
                st = []
                #loop until closing } is found
                while not accept_token('}'):
                    st.append(statement())
                    change_line_end()
                return Function(name, args, st, return_type)
            #create class
            elif accept_token('class'):
                name, parents = create_class()
                change_line_end()
                #check for start of block
                expect('{', console_index)
                change_line_end()
                functions = {}
                while True:
                    #only functions are allowed. Check for functions
                    if accept_token('func'):
                        current_index -= 1
                        #get new function
                        new_func = statement()
                        #functions are a dictionary with name as key
                        #check if function already exists
                        if not new_func.name.token in set(functions.keys()):
                            functions[new_func.name.token] = new_func
                        else:
                            #raise error
                            pass
                    change_line_end()
                    #check for closing }
                    if accept_token('}'):
                        break
                return Class(name, parents, functions)
            #return statements
            elif accept_token('return'):
                values = create_return()
                return Return(values)
            #create while loop
            elif accept_token('while'):
                comp = arrange_comps()
                expect('do', console_index)
                change_line_end()
                expect('{', console_index)
                change_line_end()
                st = []
                while not accept_token('}'):
                    st.append(statement())
                    change_line_end()
                return While_Loop(comp, st)
            #create for loop
            elif accept_token('for'):
                var, for_type, values = create_for()
                expect('do', console_index)
                change_line_end()
                expect('{', console_index)
                st = []
                change_line_end()
                while not accept_token('}'):
                    st.append(statement())
                    change_line_end()
                return For_Loop(var, for_type, values, st)
            #display statements
            elif accept_token('display'):
                #current_index += 1 
                value = create_display()
                return Display(value)
            elif accept_token('free'):
                var = create_free()
                return Free_statement(var)
            elif accept_token('input'):
                #current_index += 1
                if check_line_end():
                    if accept_type('str'):
                        return Input(string=expect_type('str', console_index))
                    else:
                        return Input()
                else:
                    return Input()
    def change_line_end():
        '''Changes line if at the end of the line'''
        nonlocal current_index, line
        if current_index >= len(tokens[line]) - 1:
            line += 1
            current_index = 0
    def check_line_end():
        '''Checks if it is at the end of the line'''
        nonlocal current_index, line
        if current_index >= len(tokens[line]):
            return True
        else:
            return False
    def clear_if_cache():
        nonlocal if_cache
        #get out if cache is empty
        if len(if_cache) == 0:
            return
        #loop until there is only one if left
        while len(if_cache) > 1:
            #break if a block indicator is found
            if if_cache[-1].type == 'if_block':
                break
            else:
                if_cache.pop()
        #pop last one or if block
        if_cache.pop()
    #keep track of location in line and token
    syntax_tree = []
    if_cache = []
    line = 0
    current_index = 0
    #iterate through lines
    while line < len(tokens):
        #figure out what next token type is
        if accept_type('keyword'):
            st = statement()
            if st != None:
                syntax_tree.append(st)
        #check for variable name to run functions
        elif accept_type('var'):
            name, args= create_func(check_type=False)
            syntax_tree.append(Custom_Func(name, args))
        #move to next line if at end of current line
        change_line_end()
    return syntax_tree