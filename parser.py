#import custom files
import lexer
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
class Global():
    def __init__(self, var):
        self.var = var
        self.type = 'global'
class Nonlocal():
    def __init__(self, var):
        self.var = var
        self.type = 'nonlocal'
class Class():
    def __init__(self, name, parent, objects):
        self.name = name
        self.parent = parent
        self.functions = objects
        self.type = 'class'
class Get_Class_Value():
    def __init__(self, instance, var):
        self.instance = instance
        self.var = var
        self.type = 'get_class_value'
class Make_Class_Instance():
    def __init__(self, name, args, outer_classes):
        self.name = name
        self.args = args
        self.outer_classes = outer_classes
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
class Change_Var_Value():
    def __init__(self, var, value, indexes):
        self.var = var
        self.value = value
        #incase of modifying an array
        self.indexes = indexes
        self.type = "change_var_value"
class Changer():
    def __init__(self, value, output):
        self.value = value
        self.output = output
        self.type = 'changer'
class Open_File():
    def __init__(self, path, var):
        self.path = path
        self.var = var
        self.type = 'open_file'
class Save_File():
    def __init__(self, var, path):
        self.var = var
        self.path = path 
        self.type = 'save_file'
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
        self.type = 'class_func'
class Return():
    def __init__(self, value):
        self.value = value
        self.type = 'return'
class Break():
    def __init__ (self):
        self.type = 'break'
class Comparison():
    def __init__(self, left, comp, right):
        self.left = left
        self.comp_op = comp 
        self.right = right
        self.type = 'comp'
class Not_Statement():
    def __init__(self, value):
        self.value = value
        self.type = 'not_statement'
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
class String_Slice():
    def __init__(self, var, start, stop, step):
        self.var = var
        self.start = start
        self.stop = stop
        self.step = step
        self.type = 'string_slice'
class String_Concat():
    def __init__(self, strings):
        self.strings = strings
        self.type = 'string_concat'
class Get_Array_Value():
    def __init__(self, var, index):
        self.var = var
        self.index = index
        self.type = 'get_array_value'
#function to raise error
def raise_error(message, input_string, token, file):
    #print error message
    print('File "' + file + '", Line ' + str(token.line + 1) + ':')
    print(message)
    print(input_string[token.line])
    print('~' * (token.location) + '^' * len(token.token))
    #raise error
    raise Parser_Error(message)
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
        elif accept_type('int'):
            current_index -= 1
            if bracketed_expression() == 'equation':
                value = equation()
            else:
                value = expect_type('int', console_index)
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
        elif accept_type('flt') or accept_type('int'):
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
        #check for flt for string slicing/getting value from array
        if accept_type('flt') or accept_type('int'):
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
def file_parser(tokens, console_index, input_string, path):
    def braketed_expression():
        '''Checks what type of brackated expression it is'''
        #first check if there is just a float next 
        if len(tokens[line]) <= current_index + 2:
            return 'float'
        elif (tokens[line][current_index + 1].token_type == 'flt' or tokens[line][current_index + 1].token_type == 'var' or tokens[line][current_index + 1].token_type == 'int') and tokens[line][current_index + 2].token_type == 'op':
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
                if accept_type('flt') or accept_type('int'):
                    #add token to output
                    output.append(current_token)
                elif accept_type('var'):
                    #add token to output
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
        #get parts of the comparison object
        if accept_token('('):
            left = comparison()
            expect(')', console_index)
        #check for not 
        elif accept_token('not'):
            if accept_token('('):
                value = comparison()
                expect(')', console_index)
                left = Not_Statement(value)
            else:
                value = tokens[line][current_index]
                left = Not_Statement(value)
                current_index += 1
            #check if only using not
            if accept_token(')'):
                current_index -= 1
                return left
        else:
            left = expect_type(['var', 'flt', 'int', 'str', 'bool'], console_index)
        comp = expect_type(['comp'], console_index)
        if accept_token('('):
            right = comparison()
            expect(')', console_index)
        elif accept_token('not'):
            if accept_token('('):
                value = comparison()
                expect(')', console_index)
                right = Not_Statement(value)
            else:
                value = tokens[line][current_index]
                right = Not_Statement(value)
                current_index += 1
        else:
            right = expect_type(['var', 'flt', 'int', 'str', 'bool'], console_index)
        #make sure valid comparison operator is used
        if not comp.token in {'==', '!=', 'and', 'or'}:
            #check if they are both floats or variables
            if (not left.token_type in {'var', 'flt', 'int'}) or (not right.token_type in {'var', 'flt', 'int'}):
                #raise error if wrong comparison is used for a number
                raise_error(f'Type Error: {comp.token} is not supported for non-number objects', input_string, comp, path)
        return Comparison(left, comp, right)
    def create_display():
        '''Creates Display Objects'''
        nonlocal current_index
        nonlocal line
        if accept_type('var'):
            value = tokens[line][current_index]
        elif accept_type('flt') or accept_type('int'):
            #current_index -= 1
            if braketed_expression() == 'equation':
                current_index += 1
                value = equation()
            else:
                value = expect_type(['flt', 'int'], console_index)
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
        var_type = expect_type('type', console_index)
        var_name = expect_type('var', console_index)
        expect('=', console_index)
        value = get_var_value(var_type)
        return var_type, var_name, value
    def string_array_retrieving(var):
        '''Create get array value/string slicing objects'''
        #uses same slicing syntax as python
        start = expect_type('int', console_index)
        #check for string slicing (:) or array value ( ) )
        if accept_token(')'):
            value = Get_Array_Value(var, start)
        else:
            expect(':', console_index)
            stop = expect_type('int', console_index)
            #check for step or end
            if accept_token(')'):
                step = Token(1, 'int')
            else:
                expect(':', console_index)
                step = expect_type('int', console_index)
                expect(')', console_index)
            value = String_Slice(var, start, stop, step)
        return value
    def get_var_value(var_type, do_type_check=True):
        nonlocal current_index
        used = False
        #allow to get user input set to a variable. This will always be a string, and should be set as so
        if accept_token('input') and (var_type.token == 'str' or do_type_check == False):
            if not check_line_end():
                if accept_type('str'):
                    value = Input(string=expect_type('str', console_index))
                else:
                    value = Input()
            else:
                value = Input()
            used = True
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
                #for running instances of classes
                elif accept_token('.'):
                    #decrement current_index, it was increased to run checks
                    current_index -= 2
                    #get class instance
                    instance = expect_type('var', console_index)
                    #pass over period
                    expect('.', console_index)
                    #if at line end, don't bother checking for function
                    while True:
                        #check if retreiving variable or running function
                        current_index += 1
                        if check_line_end():
                            #retrieve variable_name
                            current_index -= 1
                            var = expect_type('var', console_index)
                            value = Get_Class_Value(instance, var)
                            break
                        else:
                            if accept_token('['):
                                #decrement current_index (accept_token increases current_index)
                                current_index -= 2
                                name, args = create_func(check_type=False)
                                value = Class_Func(instance, name, args)
                                break
                            else:
                                #retrieve variable name
                                current_index -= 1
                                value = expect_type('var', console_index)
                                value = Get_Class_Value(instance, value)
                                instance = value
                                if check_line_end():
                                    break
                                else:
                                    expect('.', console_index)
                    #tell next chain of if statements to not run
                    used = True
                #for string slicing
                elif accept_token('('):
                    #decrement current_index, it was increased to run the checks
                    current_index -= 2
                    #get variable to slice/get array value from
                    value = expect_type('var', console_index)
                    #loop to get multi dimensional arrays
                    expect('(', console_index)
                    while True:
                        #get object
                        value = string_array_retrieving(value)
                        #break if at end of the line
                        if check_line_end():
                            break
                        else:
                            expect('(', console_index)
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
            #store outer classes
            outer_classes = []
            #check if being made from nested class
            while True:
                current_index += 1
                if accept_token('.'):
                    current_index -= 2
                    outer_classes.append(expect_type('var', console_index))
                    expect('.', console_index)
                else:
                    current_index -= 1
                    break
            #hijacking create_func to get class definition
            name, args = create_func(check_type=False)
            value = Make_Class_Instance(name, args, outer_classes)
        #check if a variable function is being run
        elif accept_type('type') or accept_type('keyword'):
            value = create_run_func()
        #arrays need to be parsed. they have to be seperated by type check and not due to current index issues
        elif var_type.token == 'array':
            #check for {
            expect('{', console_index)
            value = create_array()
        elif accept_token('{') and do_type_check == False:
            value = create_array()
        #allows equations to be used as input
        elif (var_type.token == 'flt' or var_type.token == 'int') or ((accept_type('flt') or accept_type('int')) and  do_type_check == False):
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
                    #check if requiering same type
                    if do_type_check:
                        value = expect_type(var_type.token, console_index)
                    else:
                        value = tokens[line][current_index]
        #check for comparison objects
        elif var_type.token == 'bool':
            if accept_token('('):
                value = comparison()
                expect(')', console_index)
            else:
                value = expect_type('bool', console_index)
        #allow for changing variable value using comaprison value
        elif accept_token('(') and do_type_check == False:
            value = comparison()
        #string concatenation
        elif var_type.token == 'str' or  (accept_type('str') and do_type_check == False):
            #incrase index to check for +
            current_index += 1
            if not check_line_end():
                expect('+', console_index)
                strings = []
                current_index -= 2
                while True:
                    if accept_type('var'):
                        strings.append(expect_type('var', console_index))
                    else:
                        strings.append(expect_type('str', console_index))
                    if check_line_end():
                        break
                    else:
                        expect('+', console_index)
                value = String_Concat(strings)
            else:
                current_index -= 1
                value = expect_type('str', console_index)
        #get remaining value
        elif do_type_check == False:
            value = tokens[line][current_index]
            current_index += 1
        else:
            #check for right type if not array or equation
            value = expect_type(var_type.token, console_index)
        return value
    def create_array():
        '''Creates Arrays'''
        nonlocal current_index
        array = []
        while True:
            if accept_type('var'):
                array.append(tokens[line][current_index])
            elif accept_type('flt') or accept_type('int'):
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
        #change type of variable
        if accept_type('type'):
            output = expect_type('type', console_index)
        #functions on variables
        elif accept_token('len'):
            output = tokens[line][current_index - 1]
        #get type of variable
        elif accept_token('type'):
            output = tokens[line][current_index - 1]
        #create linked variables
        elif accept_token('link'):
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
        elif accept_type('int'):
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
        #get variable name to assign to
        var = expect_type('var', console_index)
        #iterate through array
        if accept_token('in'):
            for_type = 'array'
        else:
            expect('=', console_index)
        #int must be used for start/stop/step
        if accept_type('int'):
            for_type = 'num'
            #start/stop/step need to be set to int to be used in loop
            start = int(expect_type('int', console_index).token)
            expect(',', console_index)
            stop = int(expect_type('int', console_index).token)
            #step will defult to 1 if not provided
            if accept_token('do'):
                #accept token increases index by 1, have to decrease it
                current_index -= 1
                step = 1
            else:
                expect(',', console_index)
                step = int(expect_type('int', console_index).token)
            values = [start, stop, step]
        #var and array for iterating through arrays
        elif accept_type('var'):
            values = expect_type('var', console_index)
        elif accept_token('{'):
            values = create_array()
        else:
            #raise error
            expect_type(['var', 'int'], console_index)
        return var, for_type, values
    def get_func_args(check_type):
        nonlocal current_index
        #check for opening [
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
        return args
    def create_func(check_type=True):
        nonlocal current_index
        name = expect_type('var', console_index)
        #run arguments getting function
        args = get_func_args(check_type)
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
        #check for single parent
        if not accept_token(']'):
            parent = expect_type('var', console_index)
            expect(']', console_index)
        else:
            parent = None
        return name, parent
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
        if not check_line_end():
            if token == tokens[line][current_index].token:
                current_index += 1
                return True
            else:
                return False
        else:
            raise_error('Syntax Error: Invalid Syntax', input_string, tokens[line][current_index - 1], path)
    #return boolean if next token has the same type as the inputted type
    def accept_type(token_type):
        '''returns boolen if next token is the given token type'''
        nonlocal current_index
        #check if there are tokens left to check
        if not check_line_end():
            if token_type == tokens[line][current_index].token_type:
                return True
            else:
                return False
        else:
            raise_error('Syntax Error: Invalid Syntax', input_string, tokens[line][current_index - 1], path)
    #error if next token is not the same as input
    def expect(token, console_index):
        '''raises error if expected token is not next token'''
        nonlocal current_index
        #chcek if there are tokens left to check
        if not check_line_end():
            #check if equal, else raise error
            if token == tokens[line][current_index].token:
                current_index += 1
                return tokens[line][current_index - 1]
            else:
                error_token = tokens[line][current_index]
                out_length = len(f'[Out_{console_index}]: ')
                #allows for diffferent errors to occur
                raise_error(f'Syntax Error: Expected {token}', input_string, error_token, path)
        else:
            raise_error(f'Syntax Error: Expected {token}', input_string, tokens[line][current_index - 1], path)
    #error if next token is not the same type as input
    def expect_type(token_types, console_index):
        '''Raises error if expected type isn't next token'''
        nonlocal current_index
        #check if there are tokens to check
        if not check_line_end():
            #check if types are equal, else raise error
            if tokens[line][current_index].token_type in token_types:
                current_index += 1
                return tokens[line][current_index - 1]
            else:
                error_token = tokens[line][current_index]
                raise_error(f'Type Error: {error_token.token} is not a {token_types}', input_string, error_token, path)
        else:
            raise_error(f'Type Error: Missing token of type {token_types}', input_string, tokens[line][current_index - 1], path)
    #function to create statements
    def statement():
        nonlocal if_cache
        '''Makes Statement Objects'''
        nonlocal current_index, line
        #create if statement
        if accept_token('if'):
            expect('(', console_index)
            comp = comparison()
            expect(')', console_index)
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
                st.append(get_element())
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
                else:
                    raise_error('Syntax Error: Missing if/elif', input_string, tokens[line][current_index - 1], path)
                #remove previous and add current to if cache
                if_cache.pop()
                expect('(', console_index)
                comp = comparison()
                expect(')', console_index)
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
                    st.append(get_element())
                clear_if_cache()
                obj = Elif_statement(comp, st, parent)
                if_cache.append(obj)
                return obj
            else:
                raise_error('Syntax Error: Missing if/elif', input_string, tokens[line][current_index - 1], path)
        #create else statement
        elif accept_token('else'):
            if len(if_cache) > 0:
                #check for a parent if or elif
                if isinstance(if_cache[-1], If_statement):
                    parent = if_cache[-1]
                elif isinstance(if_cache[-1], Elif_statement):
                    parent = if_cache[-1]
                else:
                    raise_error('Syntax Error: Missing if/elif', input_string, tokens[line][current_index - 1], path)
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
                    st.append(get_element())
                clear_if_cache()
                return Else_statement(st, parent)
            else:
                raise_error('Syntax Error: Missing if/elif', input_string, tokens[line][current_index - 1], path)
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
                #update current block
                current_block.append('func')
                st = []
                #loop until closing } is found
                while not accept_token('}'):
                    st.append(get_element())
                #update current_block
                current_block.pop()
                return Function(name, args, st, return_type)
            #create class
            elif accept_token('class'):
                name, parents = create_class()
                change_line_end()
                #check for start of block
                expect('{', console_index)
                change_line_end()
                objects = {}
                #update current block
                current_block.append('class')
                while True:
                    #only functions and classes are allowed. Check for functions
                    if accept_token('func'):
                        current_index -= 1
                        #get new function
                        new_func = statement()
                        #functions are a dictionary with name as key
                        #function will overwrite previous function with the same name
                        objects[new_func.name.token] = new_func
                    #check for classes
                    elif accept_token('class'):
                        current_index -= 1
                        new_class = statement()
                        #will overwrite previously defined class
                        objects[new_class.name.token] = new_class
                    change_line_end()
                    #check for closing }
                    if accept_token('}'):
                        break
                return Class(name, parents, objects)
            #return statements
            elif accept_token('return'):
                #make sure currently inside a function block
                if 'func' in current_block:
                    values = create_return()
                    return Return(values)
                else:
                    raise_error('Syntax Error: Keyword "return" cannot be used outside a function block', input_string, tokens[line][current_index - 1], path)
            #breaking from loop
            elif accept_token('break'):
                #make sure currently inside loop block (functions can't break loops, and if/elif/else do nto update current block)
                if current_block[-1] == 'loop':
                    return Break()
                else:
                    raise_error('Syntax Error: Keyword "break" cannot be used outside of a while or for loop block', input_string, tokens[line][current_index - 1], path)
            #global/nonlocal for functions
            elif accept_token('global'):
                #make sure inside a function
                if 'func' in current_block:
                    var = expect_type('var', console_index)
                    return Global(var)
                else:
                    raise_error('Syntax Error: Keyword "global" cannot be used outside a function block', input_string, tokens[line][current_index - 1], path)
            elif accept_token('nonlocal'):
                #make sure inside a function
                if 'func' in current_block:
                    var = expect_type('var', console_index)
                    return Nonlocal(var)
                else:
                    raise_error('Syntax Error: Keyword "nonlocal" cannot be used outside a function block', input_string, tokens[line][current_index - 1], path)
            #create while loop
            elif accept_token('while'):
                #get comparison and setup tokens
                expect('(', console_index)
                comp = comparison()
                expect(')', console_index)
                expect('do', console_index)
                change_line_end()
                expect('{', console_index)
                change_line_end()
                #update current block
                current_block.append('loop')
                st = []
                #loop through until closing { is found
                while not accept_token('}'):
                    st.append(get_element())
                #update current block
                current_block.pop()
                return While_Loop(comp, st)
            #create for loop
            elif accept_token('for'):
                var, for_type, values = create_for()
                expect('do', console_index)
                change_line_end()
                expect('{', console_index)
                #update current_block 
                current_block.append('loop')
                st = []
                change_line_end()
                #loop until closing { is found
                while not accept_token('}'):
                    st.append(get_element())
                #update current block
                current_block.pop()
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
            #loading files
            elif accept_token('open'):
                file_path = expect_type('path', console_index)
                expect('as', console_index)
                var = expect_type('var', console_index)
                return Open_File(file_path, var)
            #saving files
            elif accept_token('save'):
                var = expect_type('var', console_index)
                expect('in', console_index)
                file_path = expect_type('path', console_index)
                return Save_File(var, file_path)
            #importing other files
            elif accept_token('import'):
                #load file
                file_path = expect_type('path', console_index)
                try: 
                    with open(file_path.token + '.microlang', 'r') as file:
                        file = file.read()
                except FileNotFoundError:
                    raise_error('File Not Found Error: File "' + file_path.token + '" could not be found', input_string, tokens[line][current_index - 1], path)
                except Exception:
                    raise_error('File IO Error: File "' + file_path.token + '" could not be read', input_string, tokens[line][current_index -1], path)
                file_name = file_path.token
                #run other file through lexer
                file_tokens = lexer.file_lexer(file, console_index, file_path.token)
                #parse the otehr file
                file_syntax_tree = file_parser(file_tokens, console_index, file, file_path.token)
                #get only classes and functions from file
                objects = {}
                for item in file_syntax_tree:
                    if isinstance(item, Class):
                        objects[item.name.token] = item
                    elif isinstance(item, Function):
                        objects[item.name.token] = item
                #get name from path
                if '/' in file_name:
                    name = Token(file_name.split('/')[-1], 'var')
                elif '\\' in file_name:
                    name = Token(file_name.split('\\')[-1], 'var')
                else:
                    name = Token(file_name, 'var')
                #file is stored as a class object with path as name (so it cannot be made an instance of)
                file_class = Class(file_path, None, objects)
                #add to syntax tree. This prevents having to return two objects
                syntax_tree.append(file_class)
                #Add command to make an instance of the class
                instance = Make_Class_Instance(file_path, [], [])
                make_command = Make_statement(Token('instance', 'type'), name, instance)
                return make_command
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
    line = 0
    current_index = 0
    #list of entire syntax tree
    syntax_tree = []
    #keep track of if statement parents
    if_cache = []
    #keep track if it is in a block for block specific commands (nonlocal, break, etc.)
    current_block = ['global']
    def get_element():
        nonlocal current_index
        #figure out what next token type is
        if accept_type('keyword'):
            st = statement()
            if st != None:
                element = st
        #check for variable name to run functions
        elif accept_type('var'):
            #increase index to check for equals
            current_index += 1
            #check if changing variable type
            if accept_token("=") or accept_token('(') or accept_token('.'):
                #decrement by 2 to get variable name
                current_index -= 2
                var = expect_type('var', console_index)
                #check for modifying array values
                indexes = None
                # = does not require getting indexes
                if not accept_token('='):
                    #get type to look for
                    if accept_token('('):
                        next_type = 'bracket'
                    elif accept_token('.'):
                        next_type = 'class_value'
                    indexes = []
                    #loop until no more indexes are found
                    while True:
                        if next_type == 'bracket':
                            index = expect_type('flt', console_index)
                            indexes.append(index)
                            expect(')', console_index)
                        elif next_type == 'class_value':
                            index = expect_type('var', console_index)
                            indexes.append(index)
                        #break if new index is not found
                        if accept_token('('):
                            next_type = 'bracket'
                        elif accept_token('.'):
                            next_type = 'class_value'
                        else:
                            break
                else:
                    #get variable name. Using the variable as stand-in token for a type because it is not being used, but still being checked
                    value = get_var_value(var, do_type_check=False)
                    element = Change_Var_Value(var, value, indexes)
            else:
                current_index -= 1
                name, args= create_func(check_type=False)
                element = Custom_Func(name, args)
        #check for special case variables
        elif accept_type('special_var'):
            #initalising parent of class
            if accept_token('parent.__init__'):
                current_index -= 1
                name = expect_type('special_var', console_index)
                args = get_func_args(False)
                element = Custom_Func(name, args)
        #move to next line if at end of current line
        change_line_end()
        return element
    #iterate through lines
    while line < len(tokens):
        syntax_tree.append(get_element())
    return syntax_tree