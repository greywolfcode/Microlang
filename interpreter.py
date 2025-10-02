#import standerd libraries
import copy
import re
#define custom exception to call
class Interpreter_Error(Exception):
    '''This class creates the custom exception'''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
#define variables
variables = {}
def clear_vars():
    global variables
    variables = {}
def display_vars(console_index):
    global variables
    #display all variables
    output_length = len(f'[Out_{console_index}]:')
    #check if there are no variables
    if len(list(variables.values())) == 0:
        print(f'[Out_{console_index}]: No Variables Exist')
    else:
        print(f'[Out_{console_index}]:')
        #loop through and print all exisiting variables
        for var in variables:
            if variables[var].type == 'array':
                #convert array to be readable
                print_array = convert_array_tokens(variables[var].value)
                print_array = str(print_array)
                #convert brackets to ones used by the console
                print_array = print_array.replace('[', '{')
                print_array = print_array.replace(']', '}')
                print(f'{" " * output_length}{var}: {print_array}')
            else:
                print(f'{" " * output_length}{var}: {variables[var].value}')
    print('')
#token class
class Token():
    def __init__(self, token, token_type):
        self.token = token
        self.token_type = token_type
        self.type = 'token'
    def print_vars(self):
        print(self.token, self.token_type, self.location)
class Variable():
    '''Variable storing class'''
    def __init__(self, var_type, value):
        self.type = var_type 
        self.value = value
class Make_Statement():
    '''Class to store data to make variables'''
    def __init__ (self, var_type, var, value):
        self.var_type = var_type
        self.var = var
        self.value = value
        self.type = 'make'
class Class_Instance():
    '''Class to store class instances'''
    def __init__(self, instance_class, instance_vars):
        #variable to point to what class this is an instance of
        self.instance_class = instance_class
        self.instance_vars = instance_vars
        self.type = 'class_instance'
#function to make arrays able to be displayed; outside interpreter function for displaying all variables
def convert_array_tokens(array):
    #deep copy array so editing it or inside arrays will not effect the actual array 
    modified_array = copy.deepcopy(array)
    for num in range(len(array)):
        token = modified_array[num];
        if token.token_type == 'array':
            #convert inside arrays recursivley
            modified_array[num] = convert_array_tokens(token.token)
        #make floats look correct
        elif token.token_type == 'flt':
            modified_array[num] = float(token.token)
        #make variables look correct
        elif token.token_type == 'var':
            #check if variable exists
            if token.token in set(variables.keys()):
                #handle different variable types
                if variables[token.token].type == 'flt':
                    modified_array[num] = float(variables[token.token].value)
                elif variables[token.token].type == 'array':
                    #convert inside arrays recursivley
                    modified_array[num] = convert_array_tokens(variables[token.token].value)
                else:
                    modified_array[num] = variables[token.token].value
        #make booleans look correct
        elif token.token_type == 'bool':
            if token.token == 'True':
                modified_array[num] = True
            elif token.token == 'False':
                modified_array[num] = False
        else:
            modified_array[num] = token.token
        string_array = str(modified_array)
        #replace 1st and last charchter of string with proper brackets
        string_array = '{' + string_array[1:-1] + '}'
    return string_array
#interpreter function
def interpreter(syntax_tree, console_index, input_string):
    #get all console variables
    global variables
    #variable to check if an output has been acomplished
    output_done = False
    #list of helper functions to de specific interpeter tasks
    def interpret_equation(postfix):
        '''Interpret and Calulate Postfix Expressions'''
        output_stack = []
        for token in postfix:
            if token.token_type == 'flt':
                output_stack.append(token)
            elif token.token_type == 'var':
                #check if variable exists
                if token.token in set(variables.keys()):
                    #check to make sure the variable is a float
                    if variables[token.token].type == 'flt':
                        #add tokenized variable to output stack
                        output_stack.append(Token(variables[token.token].value, variables[token.token].type))
                    else:
                        print(f'[Out_{console_index}]: Type Error: {token.token} is not a float')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                else:
                    print(f'[Out_{console_index}]: Name Error: {element.value.token} does not exist')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
            else:
                #evaluate expression if operator is found and add to stack
                num_1 = output_stack.pop().token
                num_2 = output_stack.pop().token
                new_value = eval(f'{num_2} {token.token} {num_1}')
                output_stack.append(Token(new_value, 'flt'))
        #return final value
        return output_stack[0]
    def interpret_comp(comp):
        '''Return boolean value of a Comparison'''
        def get_token(token):
            '''Helper function to return token or nested comparison'''
            if token.type == 'equation':
                value = f'float("{interpret_equation(token.postfix).token}")'
            elif token.type == 'comp':
                value = interpret_comp(token)
            elif token.type == 'token':
                #check for individual values; need to explicitly set to type for eval to work
                if token.token_type == 'str':
                    value = f'"{token.token}"'
                elif token.token_type == 'flt':
                    value = f'float("{token.token}")'
                elif token.token_type == 'var':
                    #check if variable exists
                    if token.token in set(variables.keys()):
                        var_value = variables[token.token].value
                        var_type = variables[token.token].type
                        #check for individual values; need to explicitly set to type for eval to work
                        if var_type == 'str':
                            value = f'"{var_value}"'
                        elif var_type == 'flt':
                            value = f'float("{var_value}")'
                        else:
                            value = var_value
                    else:
                        print(f'[Out_{console_index}]: Name Error: {token.token} does not exist')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (token.location - len(token.token)) + '^' * len(token.token))
                        raise Interpreter_Error('')
                else:
                    value = token.token
            return value
        left = get_token(comp.left)
        right = get_token(comp.right)
        comp_op = comp.comp_op.token
        return eval(f'{left} {comp_op} {right}')
    def run_func(element):
        #convert inner changers to new type first
        if element.value.type == 'changer':
            new_value = run_func(element.value)
            element.value = new_value
        #only strings and arrays can have numerical outputs, check for that first
        if element.output.token_type == 'flt':
            #check if input is proper type
            if element.value.token_type == 'var':
                #check if variable exists
                if element.value.token in set(variables.keys()):
                    #check if variable is the right type
                    var_value = variables[element.value.token].value
                    if variables[element.value.token].type == 'str':
                        try:
                            #get value from array
                            #arrays contain token objects
                            value = var_value[int(element.output.token)]
                            return Token(value, 'str')
                        except IndexError:
                            print(f'[Out_{console_index}]: Index Error: Array index out of range')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                            raise Interpreter_Error('')
                        except ValueError:
                            print(f'[Out_{console_index}]: Index Error: Array index must be a whole number')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                            raise Interpreter_Error('')
                    elif variables[element.value.token].type == 'array':
                        try:
                            #get value from array
                            #arrays contain token objects
                            value = var_value[int(element.output.token)]
                            return Token(value.token, value.token_type)
                        except IndexError:
                            print(f'[Out_{console_index}]: Index Error: Array index out of range')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                            raise Interpreter_Error('')
                        except ValueError:
                            print(f'[Out_{console_index}]: Index Error: Array index must be a whole number')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                            raise Interpreter_Error('')
                    else:
                        print(f'[Out_{console_index}]: Type Error: {variables[element.value.token].token} is not an acceptable type ({variables[element.value.token].token_type})')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                        raise Interpreter_Error('')
                else:
                    print(f'[Out_{console_index}]: Name Error: {element.value.token} does not exist')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise Interpreter_Error('')
            elif element.value.token_type == 'str':
                try:
                    #get value from array
                    #arrays contain token objects
                    value = element.value.token[int(element.output.token)]
                    return Token(value, 'str')
                except IndexError:
                    print(f'[Out_{console_index}]: Index Error: Array index out of range')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise Interpreter_Error('')
                except ValueError:
                    print(f'[Out_{console_index}]: Index Error: Array index must be a whole number')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise Interpreter_Error('')
            elif element.value.token_type =='array':
                try:
                    #get value from array
                    #arrays contain token objects
                    value = element.value.token[int(element.output.token)]
                    return Token(value.token, value.token_type)
                except IndexError:
                    print(f'[Out_{console_index}]: Index Error: Array index out of range')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise Interpreter_Error('')
                except ValueError:
                    print(f'[Out_{console_index}]: Index Error: Array index must be a whole number')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise Interpreter_Error('')
            else:
                print(f'[Out_{console_index}]: Type Error: {element.value.token} is not an acceptable type ({element.value.token_type})')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                raise Interpreter_Error('')
        #check for keyword type
        elif element.output.token_type == 'keyword':
            #get input type
            if element.output.token == 'get':
                if element.value.token_type == 'var':
                    #check if variable exists
                    if element.value.token in set(variables.keys()):
                        return Token(variables[element.value.token].type, 'str')
                    else:
                        print(f'[Out_{console_index}]: Name Error: {element.value.token} does not exist')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                        raise Interpreter_Error('')
                else:
                    return Token(element.value.token_type, 'str')
            #get input length
            elif element.output.token == 'len':
                if element.value.token_type == 'var':
                    #check if variable exists
                    if element.value.token in set(variables.keys()):
                        #only str and array can have lengths
                        if variables[element.value.token].type in {'str', 'array'}:
                            return Token(len(variables[element.value.token].token), 'flt')
                        else:
                            print(f'[Out_{console_index}]: Type Error: Element of type {variables[element.value.token].type} does not have a length')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                            raise Interpreter_Error('')
                    else:
                        print(f'[Out_{console_index}]: Name Error: {element.value.token} does not exist')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                        raise Interpreter_Error('')
                else:
                    #only str and array can have lengths
                    if element.value.token_type in {'str', 'array'}:
                        return Token(len(element.value.token), 'flt')
                    else:
                        print(f'[Out_{console_index}]: Type Error: Element of type {element.value.token_type} does not have a length')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                        raise Interpreter_Error('')
        #this code changes the type of the object
        else:
            #check if input is a variable
            if element.value.token_type == 'var':
                #check if variable exists
                if element.value.token in set(variables.keys()):
                    #make sure variable is the right type
                    var_value = variables[element.value.token]
                    if variables[element.value.token].type == 'str':
                        if element.output.token == 'flt':
                            #use regex to check if the string can be converted to a float
                            float_reg = re.compile(r'^[0-9.-]+$')
                            if float_reg.search(var_value.token):
                                value = eval(f'{float(var_value)}')
                                return Token(value, 'flt')
                            else:
                                print(f'[Out_{console_index}]: Value Error: Could not convert string ({var_value}) to float')
                                out_length = len(f'[Out_{console_index}]: ')
                                print(' ' * out_length + input_string)
                                print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                                raise Interpreter_Error('')
                        elif element.output.token == 'str':
                            return var_value
                        elif element.output.token == 'array':
                            return Token([var_value], 'array')
                        else:
                            print(f'[Out_{console_index}]: Type Error: Could not convert string to {element.output}')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                            raise Interpreter_Error('')
                    #convert arrays
                    elif variables[element.value.token].type == 'array':
                        if element.output.token == 'flt':
                            print(f'[Out_{console_index}]: Type Error: array cannot become float')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                            raise Interpreter_Error('')
                        elif element.output.token == 'str':
                            return Token(convert_array_tokens(var_value.value), 'str')
                        elif element.output.token == 'array':
                            return Token([var_value], 'array')
                        else:
                            print(f'[Out_{console_index}]: Type Error: Could not convert array to {element.output}')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                            raise Interpreter_Error('')
                    elif variables[element.value.token].type == 'flt':
                        if element.output.token == 'flt':
                            return Token(var_value.value, 'flt')
                        elif element.output.token == 'str':
                            return Token(str(var_value.value), 'str')
                        elif element.output.token == 'array':
                            return Token([var_value], 'array')
                        else:
                            print(f'[Out_{console_index}]: Type Error: Could not convert float to {element.output.token}')
                            out_length = len(f'[Out_{console_index}]: ')
                            print(' ' * out_length + input_string)
                            print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token)) 
                            raise Interpreter_Error('')
                    else:
                        print(f'[Out_{console_index}]: Type Error: {element.value.token} is not an acceptable type ({variables[element.value.token].type})')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                        raise Interpreter_Error('')
                else:
                    print(f'[Out_{console_index}]: Name Error: {element.value.token} does not exist')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise Interpreter_Error('')
            elif element.value.token_type == 'str':
                if element.output.token == 'flt':
                    #use regex to check if the string can be converted to a float
                    float_reg = re.compile(r'^[0-9.-]+$')
                    if float_reg.search(element.value.token):
                        value = eval(f'{float(element.value.token)}')
                        return Token(value, 'flt')
                    else:
                        print(f'[Out_{console_index}]: Value Error: Could not convert string ({var_value}) to float')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                        raise Interpreter_Error('')
                elif element.output.token == 'str':
                    return Token(element.value.token, element.value.token_type)
                elif element.output.token == 'array':
                    return Token([element.value], 'array')
                else:
                    print(f'[Out_{console_index}]: Type Error: Could not convert string to {element.output.token}')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise Interpreter_Error('')
            elif element.value.token_type =='array':
                if element.output.token == 'flt':
                    print(f'[Out_{console_index}]: Type Error: array cannot become float')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise SyntaxError
                elif element.output.token == 'str':
                    return Token(convert_array_tokens(element.value), 'str')
                elif element.output.token == 'array':
                    return Token([element.value], 'array')
                else:
                    print(f'[Out_{console_index}]: Type Error: Could not convert array to {element.output.token}')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                    raise Interpreter_Error('')
            elif element.value.token_type == 'flt':
                if element.output.token == 'flt':
                    return element.value
                elif element.output.token == 'str':
                    return Token(str(element.value.token), 'str')
                elif element.output.token == 'array':
                    return Token([element.value], 'array')
                else:
                    print(f'[Out_{console_index}]: Type Error: Could not convert float to {element.output.token}')
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token)) 
                    raise Interpreter_Error('')
            else:
                print(f'[Out_{console_index}]: Type Error: {element.value.token} is not an acceptable type ({element.value.token_type})')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                raise Interpreter_Error('')
    def output_display(element):
        global variables
        statement = element.value
        print(statement)
        if statement.type == 'changer':
            #get output
            output = run_func(element.value)
            print(f'[Out_{console_index}]: {output.token}')
            print('')
        elif statement.type == 'equation':
            #solve equation
            value = interpret_equation(statement.value)
            print(f'[Out_{console_index}]: {value}')
            print('')
        elif statement.token_type == 'var':
            #make sure variable exists
            if statement.token in set(variables.keys()):
                #make arrays look good
                if variables[statement.token].type == 'array':
                    array_value = convert_array_tokens(variables[statement.token].value)
                    #convert array to array_string
                    print_array = str(array_value)
                    #convert brackets to ones used by the console syntax
                    print_array = print_array.replace('[', '{')
                    print_array = print_array.replace(']', '}')
                    #print the array
                    print(f'[Out_{console_index}]: {print_array}')
                    print('')
                else:
                    print(f'[Out_{console_index}]: {variables[statement.token].value}')
                    print('')
            else:
                print(f'[Out_{console_index}]: Name Error: {statement.token} does not exist')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (statement.location - len(statement.token)) + '^' * len(statement.token))
                raise Interpreter_Error('')
        elif statement.token_type == 'array':
            #requires deepcopy so that  multi d (i.e. 2d, 3d) arrays won't break to to modification for printing
            print_array = copy.deepcopy(statement.token)
            #convert all inside tokens to human readable charachters
            print_array = convert_array_tokens(print_array)
            #convert array to array_string
            print_array = str(print_array)
            #convert brackets to ones used by the console syntax
            print_array = print_array.replace('[', '{')
            print_array = print_array.replace(']', '}')
            #print the array
            print(f'[Out_{console_index}]: {print_array}')
            print('')
        else:
            print(f'[Out_{console_index}]: {statement.token}')
            print('')
    def set_vars(element):
        #get variable value if setting a variable to another variable
        if element.var_type.token == 'var':
            #make sure variable exists
            if element.value.token in set(variables.keys()):
                var_type = variables[element.value.token].type
                #make sure variables are not linked
                value = copy.deepcopy(variables[element.value.token].value)
                #can pull proper values straight from other variable
                variables[element.var.token] = Variable(var_type, value)
                print(f'[Out_{console_index}]: {"Done"}')
                print('')
            else:
                print(f'[Out_{console_index}]: Name Error: {element.value.token} does not exist')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                raise Interpreter_Error('')
        elif element.value.type == 'changer':
            #get changer token
            value = run_func(element.value)
            if value.token_type == element.var_type.token:
                #no longer need the token stuff in variable class
                variables[element.var.token] = Variable(element.var_type.token, value.token)
                print(f'[Out_{console_index}]: {"Done"}')
                print('')
            else:
                print(f'[Out_{console_index}]: Type Error: {value.token_type} is not a {element.var_type.token}')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                raise Interpreter_Error('')
        elif element.value.type == 'equation':
            #no longer need the token stuff in token class
            value = interpret_equation(element.value.postfix)
            variables[element.var.token] = Variable(element.var_type.token, value.token)
            print(f'[Out_{console_index}]: {"Done"}')
            print('')
        #edit arrays so that varibles are converted to their own values 
        elif element.var_type.token == 'array':
            #convert values inside arrays
            converted_array = copy.deepcopy(element.value.token)
            #iterate through origional array and change values in the new array
            for num in range(len(element.value.token)):
                #check for variables
                if converted_array[num].token_type == 'var':
                    #ensure variable exists
                    if converted_array[num].token in set(variables.keys()):
                        #create new token in array based on variable value
                        converted_array[num] = Token(variables[converted_array[num].token].value, variables[converted_array[num].token].type) 
                    else:
                        print(f'[Out_{console_index}]: Name Error: {converted_array[num].token} does not exist')
                        out_length = len(f'[Out_{console_index}]: ')
                        print(' ' * out_length + input_string)
                        print(' ' * out_length + ' ' * (converted_array[num].location - len(converted_array[num].token)) + '^' * len(converted_array[num].token))
                        raise Interpreter_Error('')
            #add variable to dictionary of variables
            variables[element.var.token] = Variable(element.var_type.token, converted_array)
            print(f'[Out_{console_index}]: {"Done"}')
            print('')
        else:
            #no longer need the token stuff in token class
            variables[element.var.token] = Variable(element.var_type.token, element.value.token)
            print(f'[Out_{console_index}]: {"Done"}')
            print('')
    #function to run commands based on type
    def run_command(element):
        nonlocal found_if
        nonlocal if_used
        nonlocal output_done
        if element.type == 'display':
            output_display(element)
            #set variable to show output was completed
            output_done = True
        elif element.type == 'equation':
            output_value = interpret_equation(element.postfix)
            print(f'[Out_{console_index}]: {output_value.token}')
            print('')
            output_done = True
        elif element.type == 'if':
            found_if = True
            #check whether the comaprison is true or false
            if interpret_comp(element.comparison):
                if_used = True
                run_command(element.statement)
                #set variable to show output was completed
                output_done = True
        elif element.type == 'elif':
            #check if an if statement has been found, otherwise error
            if found_if == True:
                #check if precursor if/elif statement was found to be true
                if if_used == False:
                    #check whether the comaprison is true or false
                    if interpret_comp(element.comparison):
                        if_used = True
                        run_command(element.statement)
                        #set variable to show output was completed
                        output_done = True
            else:
                #raise error if if statment hasn't come 1st
                print(f'[Out_{console_index}]: Syntax Error: Expected "if"')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + '^' * len('elif'))
                raise Interpreter_Error('')
        elif element.type == 'else':
            #check if an if statement has been found, otherwise error
            if found_if == True:
                #check if precursor if/elif statement was found to be true
                if if_used == False:
                    #check whether the comaprison is true or false
                    if_used = True
                    run_command(element.statement)
                    #set variable to show output was completed
                    output_done = True
            else:
                #raise error if if statment hasn't come 1st
                print(f'[Out_{console_index}]: Syntax Error: Expected "if"')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + '^' * len('else'))
                raise Interpreter_Error('')
        elif element.type == 'make':
            output = set_vars(element)
            #set variable to show output was completed
            output_done = True
    #these are used to check if if has been (for elif), and if found true (for elif)
    found_if = False 
    if_used = False 
    #loop through syntax tree
    for element in syntax_tree:
        run_command(element)
    #print an out if no output was done
    if not output_done:
        print(f'[Out_{console_index}]: ')
        print('')

#interpreter function for files
def file_interpreter(syntax_tree, console_index, input_string, path):
    #define class structure for variable scope tree
    class Node():
        def __init__(self, parent, input_string=input_string, path=path):
            #store dictionary of variables
            self.variables = {}
            self.input_string = input_string
            self.path = path
            #store parent scope
            self.parent = parent
    def raise_error(message, line):
        file = current_scope.path 
        input_string = current_scope.input_string
        print('File "' + file + '", Line ' + str(line + 1) +':')
        print(message)
        print(input_string[line])
        print('^'*len(input_string[line]))
        #raise error
        raise Interpreter_Error(message)
    def search_vars(current_scope, variable, line, all_scopes=True, give_value=True):
        '''Get a variable moving up the scope tree '''
        #check if variable is in local scope
        if variable in set(current_scope.variables.keys()):
            #allows getting mutable list oject to gat refrence to it
            if give_value == True:
                return current_scope.variables[variable]
            else:
                return current_scope.variables[variable]
        #check if there is no parent, or if it shouldn't search parent scopes
        elif current_scope.parent == None or all_scopes == False:
            raise_error('Name Error: Variable of name "' + variable + '" does not exist', line)
        #search parent scope for variable
        else:
            return search_vars(current_scope.parent, variable)
    variables = {}
    #create global variables node, which has no parent
    global_vars = Node(None)
    #define current scope
    current_scope = global_vars
    def interpret_equation(postfix, line):
        '''Interpret and Calulate Postfix Expressions'''
        output_stack = []
        for token in postfix:
            if token.token_type == 'flt' or token.token_type == 'int':
                output_stack.append(token)
            elif token.token_type == 'var':
                #check if variable exists
                var = search_vars(current_scope, token.token)
                #check to make sure the variable is a float or int
                if var.type == 'flt' or var.type == 'int':
                    #add tokenized variable to output stack
                    output_stack.append(Token(var.value, var.type))
                else:
                    raise_error('Type Error: Variable of type "' + var.type + '" cannot be used in equation', line)
                    out_length = len(f'[Out_{console_index}]: ')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
            else:
                #evaluate expression if operator is found and add to stack
                num_1 = output_stack.pop().token
                num_2 = output_stack.pop().token
                new_value = eval(f'{num_2} {token.token} {num_1}')
                output_stack.append(Token(new_value, 'flt'))
        #return final value
        return output_stack[0]
    def run_func(element):
        #changing types
        if element.output.token_type == 'type':
            if element.output.token == 'flt':
                #can only convert strings and ints to floats
                if element.value.token_type == 'str' or element.value.token_type == 'flt' or element.value.token_type == 'int':
                    try:
                        value = float(element.value.token)
                        return Token(value, 'flt')
                    except:
                        #only will error if converting a string
                        raise_error('Value Error: String "' + element.value.token + '" could not be converted to type "int"', element.line)
                elif element.value.token_type == 'var':
                    #check if variable exists
                    var = search_vars(current_scope, element.value.token)
                    try:
                        value = float(var.value)
                        return Token(value, 'flt')
                    except:
                        raise_error('Type Error: Variable of type "' + var.type + '" cannot be converted to type "flt"', element.line)
                else:
                    raise_error('Type Error: Object of type "' + element.value.token_type + '" could not be converted to type "flt"', element.line)
            elif element.output.token == 'int':
                #can only convert strings and floats to ints
                if element.value.token_type == 'str' or element.value.token_type == 'flt' or element.value.token_type == 'int':
                    try:
                        value = int(element.value.token)
                        return Token(value, 'int')
                    except:
                        #will only error if converting a string
                        raise_error('Value Error: String "' + element.value.token + '" could not be converted to type "int"', element.line)
                elif element.value.token_type == 'var':
                    #check if variable exists
                    var = search_vars(current_scope, element.value.token)
                    try:
                        value = int(var.value)
                        return Token(value, 'int')
                    except:
                        raise_error('Type Error: Variable of type "' + var.type  + '" could not be converted to type "int"', element.line)
                else:
                    raise_error('Type Error: Object of type "' + element.value.token_type + '" could not be converted to type "int"', element.line)
            elif element.output.token == 'str':
                if element.value.token_type == 'var':
                    var = search_vars(current_scope, element.value.token)
                    #check if variable is an array
                    if var.type == 'array':
                        value = convert_array_tokens(variables[element.value.token].value)
                        return Token(value, 'str')
                    else:
                        try:
                            value = str(var.value)
                            return Token(value, 'str')
                        except:
                            raise_error('Type Error: Object of type "' + var.type + '" could not be converted to type "str"', element.line)
                #arrays need to be formated correctly so they look correct
                elif element.value.token_type == 'array':
                    value = convert_array_tokens(element.value.token)
                    return Token(value, 'str')
                else:
                    try:
                        value = str(element.value.token)
                        return Token(value, 'str')
                    except:
                        raise_error('Type Error: Object of type "' + element.value.token_type + '" could not be converted to type "str"', element.line)
            elif element.output.token == 'array':
                #check for variables
                if element.value.token_type == 'var':
                    var = search_vars(current_scope, element.value.token)
                    value = Token(var.value, var.type)
                    return Token([value], 'array')
                else:
                    return Token([element.value], 'array')
        elif element.output.token_type == 'keyword':
            #get type of variable
            if element.output.token == 'type':
                if element.value.token_type == 'var':
                    var = search_vars(current_scope, element.value.token)
                    value = var.type
                    return Token(value, 'str')
                else:
                    return Token(element.value.token_type, 'str')
            #get length of variable
            elif element.output.token == 'len':
                if element.value.token_type == 'var':
                    var = search_vars(current_scope, element.value.token)
                    value = variables[element.value.token]
                    #only arrays and strings have a length
                    if value.type in {'array', 'str'}:
                        return Token(len(value.value), 'flt')
                    else:
                        raise_error('Type Error: Object of type "' + value.type + '" has no attribute "len"', element.line)
                else:
                    if element.value.type in {'array', 'str'}:
                        return Token(len(element.value.token), 'flt')
            #create linked variables
            elif element.output.token == 'link':
                if element.value.token_type == 'var':
                    #get variable
                    var = search_vars(current_scope, element.value.token)
                    return var
                else:
                    raise_error('Type Error: Cannot linke variable to object of type "' + element.value.token_type + '"', element.line)
    def find_not(value):
        '''returns Not the entered value'''
        #check if it is a comparison first
        if value.type == 'comp':
            value = not interpret_comp(value)
            #tokens should be stored as strings
            return Token(str(value), 'bool')
        #note bool(string) does not convert it to a bool, so other method has to be sued
        if value.token_type == 'var':
            var = search_vars(current_scope, value.token)
            if var.type == 'bool':
                value = not var.value == 'True'
                return Token(str(value), 'bool')
            else:
                return Token(var.value, var.type)
        elif value.token_type == 'bool':
            value = not value.token == 'True'
            return Token(str(value), 'bool')
        else:
            return value
    def interpret_comp(comp):
        '''Return boolean value of a Comparison'''
        def get_token(token):
            '''Helper function to return token or nested comparison'''
            if token.type == 'equation':
                value = f'float("{interpret_equation(token.postfix).token}")'
            elif token.type == 'comp':
                value = interpret_comp(token)
            elif token.type == 'not_statement':
                value = find_not(token.value).token
            elif token.type == 'token':
                #check for individual values; need to explicitly set to type for eval to work
                if token.token_type == 'str':
                    value = f'"{token.token}"'
                elif token.token_type == 'flt':
                    value = f'float("{token.token}")'
                elif token.token_type == 'var':
                    #check if variable exists
                    var = search_vars(current_scope, token.token)
                    var_value = var.value
                    var_type = var.type
                    #check for individual values; need to explicitly set to type for eval to work
                    if var_type == 'str':
                        value = f'"{var_value}"'
                    elif var_type == 'flt':
                        value = f'float("{var_value}")'
                    else:
                        value = var_value
                else:
                    value = token.token
            return value
        left = get_token(comp.left)
        right = get_token(comp.right)
        comp_op = comp.comp_op.token
        return eval(f'{left} {comp_op} {right}')
    def set_vars(element):
        value = get_var_value(element.var_type, element.value, element.line)
        #save variable
        current_scope.variables[element.var.token]  = value
        #modify variables in class instances
        if 'self.' in element.var.token:
            #variable is saved in parent of function scope; make variables refrenced to current variables so that instance variables get saved
            getattr(current_scope.parent, 'class_vars', {})[element.var.token] = current_scope.variables[element.var.token]
    def get_array_value(var, index):
        #check if there are nested values to retrieve
        if var.type == 'get_array_value':
            #recursively get next value in the chain 
            return get_array_value(var.var, var.index).token[int(index.token)] 
        else:
            #get variable
            var = search_vars(current_scope, var.token)
            return var.value[int(index.token)]
    def slice_string(value):
        #check if slicing is attached to an array
        if value.var.type == 'get_array_value':
            var = get_array_value(value.var.var, value.var.index)
            #make var into variable object for processing below
            var = Variable(var.token_type, var.token)
        else:
            var = search_vars(current_scope, value.var.token)
        #make sure value is a string
        if var.type == 'str':
            #use normal python string slicing to slice the value
            string = var.value[int(value.start.token):int(value.stop.token):int(value.step.token)]
            new_value = Variable('str', string)
        else:
            raise_error('Type Error: Cannot slice variable of type "' + var.type + '"', value.line)
        return new_value
    def get_class_value(value, line, get_class=False):
        if value.instance.type == 'get_class_value':
            value.instance = get_class_value(value.instance, line)
        #get class instance if required
        if not isinstance(value.instance, Class_Instance):
            instance = search_vars(current_scope, value.instance.token)
        else:
            instance = value.instance
        #make sure variable is an instance of a class
        if instance.type == 'class_instance':
            #make sure class has correct variable
            if 'self.' + value.var.token in set(instance.instance_vars.keys()):
                return instance.instance_vars['self.' + value.var.token]
            else:
                raise_error('Name Error: Variable of name "' + value.var.token + '" does not exist in instance of class "' + instance.instance_class.name + '"', line)
        else:
            raise_error('Type Error: Cannot retrieve value from object of type "' + instance.type + '"', line)
    def get_nested_class(outer_classes, current_class, line):
        for inner_class in outer_classes:
            if current_class.type == 'class':
                if inner_class.token in set(current_class.functions.keys()):
                    current_class = current_class.functions[inner_class.token]
                else:
                    raise_error('Name Error: Funton of name "' + inner_class.token + '" is not in current_class.name', line)
            elif isinstance(current_class, Class_Instance):
                if inner_class.token in set(current_class.instance_vars.keys()):
                    #make sure variable stores a class instance
                    if isinstance(current_class.instance_vars[inner_class.token], Class_Instance):
                        current_class = current_class.instance_vars[inner_class.token]
                    else:
                        raise_error('Type Error: Cannot retrieve value from object of type "' + current_class.instance_vars[inner_class.token].type + '"', line)
                elif inner_class.token in set(current_class.instance_class.functions.keys()):
                    current_class = current_class.instance_class.functions[inner_class.token]
                else:
                    raise_error('Name Error: Variable of name "' + inner_class.token + '" does not exist in instance of class "' + current_class.instance_class.name + '"', line)
            else:
                raise_error('Type Error: Cannot retrieve class value from object of type "' + current_class.type + '"', line)
        return current_class
    def get_var_value(var_type, value, line, ignore_type=False):
        #get variable value if setting a variable to another variable
        if var_type.token == 'var':
            #check if it is coming from an array
            if value.type == 'get_array_value':
                result = get_array_value(value.var, value.index)
                value = Variable(result.token_type, result.token)
            else:
                #make sure variable exists
                var = search_vars(current_scope, value.token, line)
                #can pull proper values straight from other variable
                value = copy.deepcopy('var')
        #get comparisons 
        elif value.type == 'comp':
            value = Variable('bool', interpret_comp(value))
        elif value.type == 'not_statement':
            boolean = find_not(value.value)
            if boolean.token_type == 'bool':
                value = Variable('bool', boolean.token)
            else:
                value = Variable(boolean.token_type, boolean.token)
        elif value.type == 'get_class_value':
            #loop for nested classes
            value = get_class_value(value)
        elif value.type == 'run_func':
            #get changer token
            result = run_func(value)
            #check if a variable object is returned
            if isinstance(result, Variable):
                #check if types match
                if result.type == var_type.token or ignore_type:
                    value = result
                else:
                    raise_error('Type Error: Cannot assign value of type "' + result.type + '" to variable of type "' + var_type.token, line)
            elif result.token_type == var_type.token:
                #no longer need the token stuff in variable class
                value = Variable(var_type.token, result.token)
            else:
                raise_error('Type Error: Cannot assign value of type "' + result.token_type + '" to variable of type "' + var_type.token + '"', line)
        elif value.type == 'custom_func':
            #run function and get value
            result = custom_func(value)
            #make sure type matches
            if result.token_type == var_type.token or ignore_type:
                value = Variable(var_type.token, result.token)
            else:
                raise_error('Type Error: Returned value of type "' + result.token_type + '" cannot be assigned to variable of type "' + var_type.token + '"', line)
        elif value.type == 'make_class_instance':
            #check if there are outer classes
            if len(value.outer_classes) != 0:
                current_class = search_vars(current_scope, value.outer_classes[0].token)
                #starting at first inner class
                final_class = get_nested_class(value.outer_classes[1:], current_class)
                #get instance from current_class
                instance_class = get_nested_class([value.name], final_class)
            else:
                instance_class = search_vars(current_scope, value.name.token)
            instance = Class_Instance(instance_class, {})
            #check if there is an init function
            if '__init__' in set(instance_class.functions.keys()):
                #run using run function class
                run_class_func_init(instance_class.functions['__init__'], value, instance.instance_vars, instance.instance_class.functions)
                #remove reference to instance variables in current_scope
                del current_scope.class_vars
            value = instance
        elif value.type == 'class_func':
            result = run_class_func(value)
            value = Variable(var_type.token, result.token)
            #remove refrence to instance variables in current_scope
            del current_scope.class_vars
        elif value.type == 'string_slice':
            value = slice_string(value)
        elif value.type == 'string_concat':
            #loop through all strings
            strings = []
            for string in value.strings:
                if string.token_type == 'var':
                    #make sure var is the right type
                    var = search_vars(current_scope, string.token)
                    if var.type == 'str':
                        strings.append(var.value)
                    elif var.type == 'flt' or var.type == 'int' or var.type == 'bool':
                        strings.append(str(var.value))
                    else:
                        raise_error('Type Error: Variable of type "' + var.type +'" can not be concatenated', line)
                #values are already stored as a string in the token
                elif string.token_type == 'str' or string.token_type == 'flt' or string.token_type == 'bool':
                    strings.append(string.token)
            #merge strings
            value = Variable('str',"".join(strings))
        elif value.type == 'get_array_value':
            #run function to get array value
            result = get_array_value(value.var, value.index)
            value = Variable(result.token_type, result.token)
        elif value.type == 'equation':
            #no longer need the token stuff in token class
            num = interpret_equation(value.postfix)
            #make type correct for the variable
            if var_type.token == 'flt':
                value = Variable(var_type.token, float(num.token))
            elif var_type.token == 'int':
                value = Variable(var_type.token, int(num.token))
        #edit arrays so that varibles are converted to their own values 
        elif var_type.token == 'array':
            #convert values inside arrays
            converted_array = copy.deepcopy(value.token)
            #iterate through origional array and change values in the new array
            for num in range(len(value.token)):
                #check for variables
                if converted_array[num].token_type == 'var':
                    #ensure variable exists
                    var = search_vars(current_scope, converted_array[num].token)
                    #create new token in array based on variable value
                    converted_array[num] = Token(variables[converted_array[num].token].value, variables[converted_array[num].token].type) 
            #add variable to dictionary of variables
            value = Variable(var_type.token, converted_array)
        elif value.type == 'input':
            #gets input from the user
            value = Variable(var_type.token, get_input(value.string))
        elif value.token_type == 'var':
            #get var
            var = search_vars(current_scope, value.token)
            #make sure types match
            if var_type.token == var.type:
                #values should not be linked
                value = copy.deepcopy(var)
            else:
                raise_error('Type Error: Object of type "' + var.type + '" cannot be assigned to Variable of type "' + var_type.token + '"', element.line)
        elif ignore_type == True:
            value = Variable(value.token_type, value.token)
        else:
            #no longer need the token stuff in token class
            value = Variable(var_type.token, value.token)
        return value
    def modify_array(array, indexes, value, line):
        #check if there are still indexes
        if len(indexes) != 0:
            #make sure array is array type
            if array.type == 'array':
                array.value[int(indexes[0].token)] = modify_array.value[int(indexes[0]).token, indexes[1:], value]
                return array
            #catch if array is a token
            elif array.token_type == 'array':
                array.token[int(indexes[0].token)] =  modify_array(array.token[int(indexes[0].token)], indexes[1:], value)
                return array
            #check if modifying class
            elif isisntance(array, Class_Instance):
                return modify_class_value(arrya, indexes, value)
            else:
                raise_error('Type Error: Object of type "' + array.type +'" is not a valid type to retrieve from', line)
        else:
            return value
    def modify_class_value(var, indexes, value, line):
        #check if there are still indexes
        if len(indexes) != 0:
            #check if need to modify array instead
            if indexes[0].token_type == 'int':
                if var.type == 'array':
                    return modify_array(var, indexes, value)
                else:
                    raise_error('Type Error: Object to retrieve from must be of type "array" not "' + var.type + '"', line)
            elif isinstance(var, Class_Instance):
                if 'self.' + indexes[0].token in set(var.instance_vars.keys()):
                    var = modify_class_value(var.instance_vars['self.' + indexes[0].token], indexes[1:], value)
                    return var
                else:
                    raise_error('Name Error: No variable of name "' + indexes[0].token +'" in class "' + var.instance_class.name +'"', line)
            else:
                raise_error('Type Error: Object of type "' + var.type + '" is not a valid type to retrieve from', line)
        else:
            return value
    #change exisitng variable's value
    def change_var_value(element):
        '''Change an existing variable's value'''
        #make sure variable exists
        var = search_vars(current_scope, element.var.token)
        #functions and classes should be handled differently due to not having a "value" attribute
        if var.type not in {'function', 'class', 'instance'}:
            #check if modifying array/getting class value
            if element.indexes != None:
                #type doesn't matter, it will be ignored
                value = get_var_value(Token('flt', 'type'), element.value, ignore_type=True)
                #check what type of variable to retrieve
                if element.indexes[0].token_type == 'var':
                    instance = search_vars(current_scope, element.var.token)
                    #make sure instance is in fact a clas instance
                    if isinstance(instance, Class_Instance):
                        #make sure variable exists in instance
                        if 'self.' + element.indexes[0].token in set(instance.instance_vars.keys()):
                            if isinstance(value, Variable):
                                instance.instance_vars['self.' + element.indexes[0].token].value = modify_class_value(instance.instance_vars['self.'+element.indexes[0].token], element.indexes[1:], value).value
                            else:
                                instance.instance_vars['self.' + element.indexes[0].token] = modify_class_value(instance.instance_vars['self.'+element.indexes[0].token], element.indexes[1:], value)
                        else:
                            raise_error('Name Error: No variable of name "' + element.indexes[0].token +'" in class "' + instance.instance_class.name + '"', element.line)
                    else:
                        raise_error('Type Error: Cannot modify instance variable of object of type "' + instance.type + '"', element.line)
                elif element.indexes[0].token_type == 'int':
                    #convert variable to token if required; can't store variable object in array
                    if isinstance(value, Variable):
                        value = Token(value.value, value.type)
                    array = search_vars(current_scope, element.var.token)
                    #call function to modify array
                    array.value[int(element.indexes[0].token)] = modify_array(array.value[int(element.indexes[0].token)], element.indexes[1:], value)
            else:
                #get the new value
                value = get_var_value(Token(var.type, 'type'), element.value, ignore_type=True)
                #make sure types match
                if value.type == var.type:
                    current_scope.variables[element.var.token].value = value.value
                else:
                    raise_error('Type Error: Cannot change variable of type "' + var.type + '" to "' + value.type + '"', element.line)
        else:
           raise_error('Type Error: Cannot change value for object of type "' + var.type + '"', element.line)
    def free_var(element):
        '''Free a variable from memory'''
        nonlocal variables 
        #delete variable if it exists, otherwise raise an error
        var = search_vars(current_scope, element.var.token, element.line)
        del current_scope.variables[element.var.token]
    #print to screen
    def output_display(element):
        nonlocal variables
        statement = element.value
        if statement.type == 'run_func':
            #get output
            output = run_func(element.value)
            print(output.token)
        elif statement.type == 'equation':
            #solve equation
            value = interpret_equation(statement.value)
        elif statement.token_type == 'var':
            #make sure variable exists
            var = search_vars(current_scope, statement.token)
            #make arrays look good
            if var.type == 'array':
                print_array = convert_array_tokens(var.value)
                #print the array
                print(print_array)
            else:
                print(var.value)
        elif statement.token_type == 'array':
            #convert all inside tokens to human readable charachters
            print_array = convert_array_tokens(statement.token)
            #print the array
            print(print_array)
        else:
            print(statement.token)
    def get_input(string):
        return input(string.token)
    def run_class_func(element):
        #check if using nested class
        if element.instance.type == 'get_class_value':
            instance = get_class_value(element.instance, get_class=True)
            #get actual instance using name
        else:
            #retrive class instance
            instance = search_vars(current_scope, element.instance.token)
        #make sure function exists in class
        if element.name.token in set(instance.instance_class.functions.keys()):
            #add refrence to isntance vars in current_scope
            current_scope.class_vars = instance.instance_vars
            #retrive and run the function
            value = run_class_func_init(instance.instance_class.functions[element.name.token], element, instance.instance_vars, instance.instance_class.functions)
        else:
            raise_error('Name Error: Class "' + instance.instance_class.name +'" has no function named "' + element.name.token + '"', element.line)
        #for functions that return a value
        return value
    def custom_func(element):
        func = search_vars(current_scope, element.name.token)
        #make sure func is a function
        if func.type == 'function':
            #return for returns from the fucntions
            return run_custom_func(func, element, input_string=func.input_string, path=func.path)
        else:
            raise_error('Type Error: Expected object of type "function" not "' + func.type +'"', element.line)
    def run_class_func_init(func, element, instance_vars, instance_funcs):
        nonlocal current_scope
        #allow modification to instance vars
        current_scope.class_vars = instance_vars
        #both functions and variables need to be added to the function scope
        vars_to_add = instance_vars | instance_funcs
        #run function running function
        return run_custom_func(func, element, vars_to_add=vars_to_add, input_string=instance.instance_class.input_string, path=instance.instance_class.path)
    #seperate function to run custom functions to make classes easier
    def run_custom_func(func, element, vars_to_add={}, input_string=input_string, path=path):
        nonlocal current_scope
        #create new scope and change scope
        new_scope = Node(current_scope, input_string=input_string, path=path)
        current_scope = new_scope
        #add return type to current scope
        current_scope.return_type = func.return_type
        #if parent scope has class variables, propogate them to new scope
        try:
            current_scope.class_vars = current_scope.parent.class_vars
        except:
            pass
        #make sure the right number of arguments were provided
        if len(element.args) == len(func.args):
            #iterate through args and add them to variables
            for num, arg in enumerate(func.args):
                    if element.args[num].token_type == arg['type'].token:
                        current_scope.variables[arg['name'].token] = Variable(arg['type'].token, element.args[num].token)
                    #handle inputted variables
                    elif element.args[num].token_type == 'var':
                        #get var
                        var = search_vars(current_scope, element.args[num].token)
                        if var.type == arg['type'].token:
                            current_scope.variables[arg['name'].token] = Variable(arg['type'].token, var.value)
                        else:
                            raise_error('Type Error: Variable should be of type "' + arg['type'].token + '" not "' + var.type + '"', element.line)
                    else:
                        raise_error('Type Error: Value should be of type "' + arg['type'].token +'" not "' + element.args[num].token_type +'"', element.line)
        elif len(element.args) > len(func.args):
            raise_error('Type Error: Provided ' + str(len(element.args)) + ' arguments but function "' + func.name.token + '" requires ' + str(len(func.args)), element.line)
        elif len(element.args) < len(func.args):
            raise_error('Type Error: Function "' + func.name.token + '" requires ' + str(len(func.args)) + ' arguments but only ' + str(len(element.args)) + ' were provided', element.line)
        #add any additonal variables (for instance variables)
        current_scope.variables = current_scope.variables | vars_to_add
        #run function code
        for statement in func.statement:
            value = run_command(statement)
            #break if it gets a return value
            if value != None:
                break
        #reset scope once function is done
        current_scope = new_scope.parent
        #free new_scope
        del new_scope
        #return value
        return value
    def run_command(element):
        nonlocal current_scope
        #check what needs to be done based on what type of structure is next
        if element.type == 'display':
            output_display(element)
        elif element.type == 'input':
            get_input(element.string)
        elif element.type == 'make':
            output = set_vars(element)
        elif element.type == 'free':
            free_var(element)
        elif element.type == 'if':
            #check whether the comaprison is true or false
            if interpret_comp(element.comparison):
                #set self to true
                element.true = True
                for statement in element.statement:
                    value = run_command(statement)
                    #get out in case inside a loop/function
                    if value == 'break':
                        return 'break'
                    elif value != None:
                        return value
            #reset to false in case it is in a loop
            else:
                element.true = False
        elif element.type == 'elif':
            #check if precursor if/elif statement was found to be true
            if element.parent.true == False:
                #check whether the comaprison is true or false
                if interpret_comp(element.comparison):
                    #set self to be true
                    element.true = True
                    for statement in element.statement:
                        value = run_command(statement)
                        #getout in case inside a loop/function
                        if value == 'break':
                            return 'break'
                        elif value != None:
                            return value
                    #set variable to show output was completed
                    output_done = True
                else:
                    element.true = False
            #set parent to false and self to true so lower levels don't get wrong signal
            else:
                element.parent.true = False
                element.true = True
        elif element.type == 'else':
            #check if precursor if/elif statement was found to be true
            if element.parent.true == False:
                #check whether the comaprison is true or false
                if_used = True
                for statement in element.statement:
                    value = run_command(statement)
                    #getout in case inside a loop/function
                    if value == 'break':
                        return 'break'
                    elif value != None:
                        return value
                #set variable to show output was completed
                output_done = True
            #clear parent truth value
            else:
                element.parent.true = False
        elif element.type == 'while':
            #check vomaprison
            while interpret_comp(element.comparison):
                #loop through all statements inside
                for statement in element.statement:
                    value = run_command(statement)
                    #getout for break
                    if value == 'break':
                        #using return becuase of nested loop
                        return
                    #getout for return
                    elif value != None:
                        return value
        elif element.type == 'break':
            return 'break'
        elif element.type == 'for':
            #iterating a number up
            if element.for_type == 'num':
                nums = element.values
                flt_token = Token('flt', 'type')
                num_token = Token(nums[0], 'flt')
                var = Make_Statement(flt_token, element.var, num_token)
                #loop through the start, stop step
                for num in range(nums[0], nums[1], nums[2]):
                    num_token = Token(num, 'flt')
                    var.value = num_token
                    #save variable 1st
                    set_vars(var)
                    for statement in element.statement:
                        value = run_command(statement)
                        #getout for break
                        if value == 'break':
                            return
                        #getout for return
                        elif value != None:
                            return value
            elif element.for_type == 'array':
                #check for array vs var
                if element.values.token_type ==  'var':
                    #make sure variable is an array
                    variable = search_vars(current_scope, element.values.token)
                    if variable.type == 'array':
                        array = variable.value
                    else:
                        raise_error('Type Error: Variable should be of type "array", not "' + variable.type + '"', element.line)
                elif element.values.token_type == 'array':
                    array = element.values.token
                else:
                    raise_error('Type Error: Value should be of type "array", not "' + element.values.token_type + '"', element.line)
                #initalise var saving stuff
                type_token = Token('array', 'type')
                value_token = Token('0', 'str')
                var = Make_Statement(type_token, element.var, value_token)
                #loop through array
                for value in array:
                    value_token = Token(value.token, value.token_type)
                    var.value = value_token
                    type_token.token = value.token_type
                    #save var
                    set_vars(var)
                    #loop thorugh commands inside
                    for statement in element.statement:
                        value = run_command(statement)
                        #getout for break
                        if value == 'break':
                            return
                        #getout for return
                        elif value != None:
                            return value
        elif element.type == 'function':
            #saving function to variable
            current_scope.variables[element.name.token] = element
        #make global variable useable in function
        elif element.type == 'global':
            #loop until global scope is found
            scope = current_scope
            while True:
                if scope.parent == None:
                    break
                else:
                    scope = scope.parent
            var = search_vars(scope, element.var.token, all_scopes=False, give_value=False)
            current_scope.variables[element.var.token] = var
        #get nonlocal variable (from one scope up)
        elif element.type == 'nonlocal':
            var = search_vars(current_scope.parent, element.var.token, all_scopes=False, give_value=False)
            current_scope.variables[element.var.token] = var
        #run custom function
        elif element.type == 'custom_func':
            custom_func(element)
        #return statement
        elif element.type == 'return':
            #return the value of the variable if it is a variable
            if element.value[0].token_type == 'var':
                var_value = search_vars(current_scope, element.value[0].token)
                #turn var value into a token to make compatability with other variable setting better
                value = Token(var_value.value, var_value.type)
            else:
                value = element.value[0]
            #make sure output type is correct
            if value.token_type == current_scope.return_type.token:
                #return the value
                return value
            else:
                raise_error('Type Error: Return should be of type "' + current_scope.return_type.token + '" not "' + value.token_type + '"', element.line)
        elif element.type == 'change_var_value':
            change_var_value(element)
        #save class as variable
        elif element.type == 'class':
            #deal with parent class
            if element.parent != None:
                #get parent
                parent = search_vars(current_scope, element.parent.token)
                #make sure parent is a class
                if parent.type == 'class':
                    #create shallow copy of functions
                    parent_funcs = parent.functions.copy()
                    #use shallow copy to change key for __init__ function, but not have to make copied in memory of all functions
                    if '__init__' in set(parent_funcs.keys()):
                        #change key for __init__ to parent.__init__
                        init_func = parent_funcs.pop('__init__')
                        parent_funcs['parent.__init__'] = init_func
                    #add parent functions to class list of functions. The child function with have priority for duplicate function
                    element.functions = parent_funcs | element.functions
                else:
                    raise_error('Type Error: Object of type "' + parent.type + '" cannot be parent of a class', element.line)
            current_scope.variables[element.name.token] = element
        #open file and store it as a string
        elif element.type == 'open_file':
            #open file
            try:
                with open(element.path.token, 'r') as f:
                    file = f.read()
            except FileNotFoundError:
                raise_error('File Not Found Error: File "' + element.path.token + '" could not be found', element.line)
            except Exception as e:
                raise_error('File IO Error: File "' + element.path.token + '" could not be read', element.line)
            #save file as var
            current_scope.variables[element.var.token] = Variable('str', file)
        #save variable to document
        elif element.type == 'save_file':
            #get variable
            var = search_vars(current_scope, element.var.token)
            #prepare variable to save
            if var.type == 'str' or var.type == 'bool':
                value = var.value
            elif var.type == 'flt' or var.type == 'int':
                value = str(var.value)
            elif var.type == 'array':
                value = convert_array_tokens(var.value)
            else:
                raise_error(f'Type Error: Type "{var.type}"" cannot be saved to file', element.line)
            #open and save to file
            with open(element.path.token, 'w') as file:
                file.write(value)
    #loop through all sections of tree
    for tree in syntax_tree:
        run_command(tree)