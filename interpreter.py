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
class Make_Statment():
    '''Class to store data to make variables'''
    def __init__ (self, var_type, var, value):
        self.var_type = var_type
        self.var = var
        self.value = value
        self.type = 'make'
class Class_Instance():
    '''Class to store class instances'''
    def __init__(self, instance_class):
        #variable to point to what class this is an instance of
        self.instance_class = instance_class
        self.type = 'class_instance'
#define class structure for variable scope tree
class Node():
    def __init__(self, parent):
        #store dictionary of variables
        self.variables = {}
        #store parent scope
        self.parent = parent
def search_vars(current_scope, variable):
    '''Get a variable moving up the scope tree '''
    #check if variable is in local scope
    if variable in set(current_scope.variables.keys()):
        #using lists for a mutable data type, so have to get 1st item in the list
        return current_scope.variables[variable][0]
    #check if there is no parent
    elif current_scope.parent == None:
        #variable does not exist - raise error
        pass
    #search parent scope for variable
    else:
        return search_vars(current_scope.parent, variable)
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
                value = variables[element.value.token].value
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
def file_interpreter(syntax_tree, console_index, input_string):
    variables = {}
    #create global variables node, which has no parent
    global_vars = Node(None)
    #define current scope
    current_scope = global_vars
    def interpret_equation(postfix):
        '''Interpret and Calulate Postfix Expressions'''
        output_stack = []
        for token in postfix:
            if token.token_type == 'flt':
                output_stack.append(token)
            elif token.token_type == 'var':
                #check if variable exists
                var = search_vars(current_scope, token.token)
                #check to make sure the variable is a float
                if var.type == 'flt':
                    #add tokenized variable to output stack
                    output_stack.append(Token(var.value, var.type))
                else:
                    print(f'[Out_{console_index}]: Type Error: {token.token} is not a float')
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
                #can only convert strings to floats
                if element.value.token_type == 'str':
                    try:
                        value = float(element.value.token)
                        return Token(value, 'flt')
                    except:
                        #raise error
                        pass
                elif element.value.token_type == 'var':
                    #chack if variable exists
                    var = search_vars(current_scope, element.value.token)
                    try:
                        value = float(var.value)
                        return Token(value, 'flt')
                    except:
                        #raise error
                        pass
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
                            #raise error
                            pass
                #arrays need to be formated correctly so they look correct
                elif element.value.token_type == 'array':
                    value = convert_array_tokens(element.value.token)
                    return Token(value, 'str')
                else:
                    try:
                        value = str(element.value.token)
                        return Token(value, 'str')
                    except:
                        #raise error
                        pass
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
                        #raise error
                        pass
                else:
                    if element.value.type in {'array', 'str'}:
                        return Token(len(element.value.token), 'flt')
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
        #get variable value if setting a variable to another variable
        if element.var_type.token == 'var':
            #make sure variable exists
            var = search_vars(current_scope, element.value.token)
            var_type = var.type
            value = var.value
            #can pull proper values straight from other variable
            current_scope.variables[element.var.token] = [Variable(var_type, value)]
        elif element.value.type == 'run_func':
            #get changer token
            value = run_func(element.value)
            if value.token_type == element.var_type.token:
                #no longer need the token stuff in variable class
                current_scope.variables[element.var.token] = [Variable(element.var_type.token, value.token)]
            else:
                print(f'[Out_{console_index}]: Type Error: {value.token_type} is not a {element.var_type.token}')
                out_length = len(f'[Out_{console_index}]: ')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (element.value.location - len(element.value.token)) + '^' * len(element.value.token))
                raise Interpreter_Error('')
        elif element.value.type == 'custom_func':
            value = custom_func(element.value)
            #make sure type matches
            if value.token_type == element.var_type.token:
                current_scope.variables[element.var.token] = [Variable(element.var_type.token, value.token)]
            else:
                #raise error
                pass
        elif element.value.type == 'make_class_instance':
            instance_class = search_vars(current_scope, element.value.name.token)
            #check if there is an init function
            if '__init__' in set(instance_class.functions.keys()):
                pass
            else:
                pass
        elif element.value.type == 'equation':
            #no longer need the token stuff in token class
            value = interpret_equation(element.value.postfix)
            current_scope.variables[element.var.token] = [Variable(element.var_type.token, value.token)]
        #edit arrays so that varibles are converted to their own values 
        elif element.var_type.token == 'array':
            #convert values inside arrays
            converted_array = copy.deepcopy(element.value.token)
            #iterate through origional array and change values in the new array
            for num in range(len(element.value.token)):
                #check for variables
                if converted_array[num].token_type == 'var':
                    #ensure variable exists
                    var = search_vars(current_scope, converted_array[num].token)
                    #create new token in array based on variable value
                    converted_array[num] = Token(variables[converted_array[num].token].value, variables[converted_array[num].token].type) 
            #add variable to dictionary of variables
            current_scope.variables[element.var.token] = [Variable(element.var_type.token, converted_array)]
        elif element.value.type == 'input':
            #gets input from the user
            current_scope.variables[element.var.token] = [Variable(element.var_type.token, get_input(element.value.string))]
        else:
            #no longer need the token stuff in token class
            current_scope.variables[element.var.token] = [Variable(element.var_type.token, element.value.token)]
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
                print_array = convert_array_tokens(variables[statement.token].value)
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
    def free_var(element):
        '''Free a variable from memory'''
        nonlocal variables 
        #delete variable if it exists, otherwise raise an error
        var = search_vars(current_scope, element.var.token)
        del current_scope.variables[element.var.token]
    def get_input(string):
        return input(string.token)
    def custom_func(element):
        nonlocal current_scope
        func = search_vars(current_scope, element.name.token)
        #make sure func is a function
        if func.type == 'function':
            #create new scope and change scope
            new_scope = Node(current_scope)
            current_scope = new_scope
            #add return type to current scope
            current_scope.return_type = func.return_type
            #iterate through args and add them to variables
            for num, arg in enumerate(func.args):
                #try except in case not enough argumetns were provided
                try:
                    if element.args[num].token_type == arg['type'].token:
                        current_scope.variables[arg['name'].token] = [Variable(arg['type'].token, element.args[num].token)]
                except:
                    #raise error
                    pass
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
        else:
            #raise error
            pass
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
                element.true = True
                for statement in element.statement:
                    run_command(statement)
            #reset to false in case it is in a loop
            else:
                element.true = False
        elif element.type == 'elif':
            #check if precursor if/elif statement was found to be true
            if element.parent.true == False:
                #check whether the comaprison is true or false
                if interpret_comp(element.comparison):
                    element.true = True
                    for statement in element.statement:
                        run_command(statement)
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
                    run_command(statement)
                #set variable to show output was completed
                output_done = True
            #clear parent truth value
            else:
                element.parent.true = False
        elif element.type == 'while':
            while interpret_comp(element.comparison):
                for statement in element.statement:
                    run_command(statement)
        elif element.type == 'for':
            #iterating a number up
            if element.for_type == 'num':
                nums = element.values
                flt_token = Token('flt', 'type')
                num_token = Token(nums[0], 'flt')
                var = Make_Statment(flt_token, element.var, num_token)
                #loop through the start, stop step
                for num in range(nums[0], nums[1], nums[2]):
                    num_token = Token(num, 'flt')
                    var.value = num_token
                    #save variable 1st
                    set_vars(var)
                    for statement in element.statement:
                        run_command(statement)
        elif element.type == 'function':
            #saving function to variable
            current_scope.variables[element.name.token] = [element]
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
                #raise error
                pass
    #loop through all sections of tree
    for tree in syntax_tree:
        run_command(tree)