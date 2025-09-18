#import standerd libraries
import re
#define custom exception to call
class Lexer_Error(Exception):
    '''This class creates the custom exception'''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
#token class
class Token():
    def __init__(self, token, token_type, location, line):
        self.token = token
        self.token_type = token_type
        self.location = location
        self.line = line
        self.type = 'token'
    def print_vars(self):
        print(self.token, self.token_type, self.location)
#function to split input into tokens
def lexer(input_string, console_index):
    current_token = ''
    tokens = []
    found_quotes = 0
    #helper function to add tokens
    def add_token(token, index):
        nonlocal tokens
        keywords = {'make', 'if', 'elif', 'else', 'then', 'and', 'or', 'display', 'get', 'len'}
        types = {'flt', 'str', 'array', 'var', 'bool'}
        booleans = {'True', 'False'}
        #token is a string if there has been an even number of quotes found
        if found_quotes != 0 and found_quotes % 2 == 0:
            tokens.append(Token(token, 'str', index - len(current_token), 0))
        else:
            #define matching patterns
            float_reg = re.compile(r'^[0-9.-]+$')
            var_reg = re.compile(r'^[_a-zA-z0-9]+$')
            op_reg = re.compile(r'^[+\-*/]+$|^[\**]+$')
            assign_reg = re.compile(r'^[=]+$')
            compare_reg = re.compile(r'^[==]+$|^[!=]+$|^[<=]+$|^[>=]+$|^[<]+$|^[>]+$')
            container_reg = re.compile(r'^[{]+$|^[}]+$')
            orderer_reg = re.compile(r'^[(]+$|^[)]+$')
            seperator_reg = re.compile(r'^[,]+$')
            changer_reg = re.compile(r'^[\[]+$|^[\]]+$')
            #check if it is one of the keywords
            if current_token in keywords:
                tokens.append(Token(token, 'keyword', index - len(current_token), 0))
            #check if it is a type
            elif current_token in types:
                tokens.append(Token(token, 'type', index - len(current_token), 0))
            #check if it is a changer seperator
            elif changer_reg.search(token):
                tokens.append(Token(token, 'changer', index - len(current_token), 0))
            #check for mathmatical operator
            elif op_reg.search(token):
                tokens.append(Token(token, 'op', index - len(current_token), 0))
            #check if it is only numeric
            elif float_reg.search(token):
                tokens.append(Token(token, 'flt', index - len(current_token), 0))
            #check if it is only boolean
            elif current_token in booleans:
                tokens.append(Token(token, 'bool', index - len(current_token), 0))
            #check if it is a valid variable name
            elif var_reg.search(token):
                tokens.append(Token(token, 'var', index - len(current_token), 0))
            #check if it is a assignment equals; length check makes = assignment but == a compare
            elif assign_reg.search(token) and len(token) == 1:
                tokens.append(Token(token, 'assign', index - len(current_token), 0))
            #check if it is a valid variable name
            elif compare_reg.search(token):
                tokens.append(Token(token, 'comp', index - len(current_token), 0))
            #check if it is a container
            elif container_reg.search(token):
                tokens.append(Token(token, 'container', index - len(current_token), 0))
            #check if it is a paren for math
            elif orderer_reg.search(token):
                tokens.append(Token(token, 'orderer', index - len(current_token), 0))
            #check if it is a comma seperator
            elif seperator_reg.search(token):
                tokens.append(Token(token, 'seperator', index - len(current_token), 0))
            #ignore whitespace
            elif current_token in {' ', ''}:
                pass
            #error if anyhting else occurs
            else:
                #check if there is a missing quote mark
                if found_quotes % 2 != 0:
                    out_length = len(f'[Out_{console_index}]: ')
                    print(f'[Out_{console_index}]: Syntax Error: Expected \'')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (index - len(current_token)) + '^')
                    raise Lexer_Error('Missing Quote')
                else:
                    out_length = len(f'[Out_{index}]: ')
                    print(f'[Out_{console_index}]: Syntax Error: Invalid Syntax. Missing Space?')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (index - len(current_token)) + '^' * len(token))
                    raise Lexer_Error('')
            #index - len(current_token)
    #loop through all input charachters
    for index, char in enumerate(input_string):
        if char == "'":
            #check if any quotes have been found, respond accordingly
            found_quotes += 1 
            if found_quotes == 3:
                out_length = len(f'[Out_{console_index}]: ')
                print(f'[Out_{console_index}]: Syntax Error: Expected \'')
                print(' ' * out_length + input_string)
                print(' ' * out_length + ' ' * (index - len(current_token)) + '^')
                raise Lexer_Error('Extra_Quote_Mark')
        #if a token is finished, figure out what it is
        elif char == ' ':
            #total quotes will be divisible by two if a string is completed or if there is no string now
            if found_quotes % 2 == 0:
                add_token(current_token, index)
                current_token = ''
                found_quotes = 0
            else:
                #add to current token if a token is still uncomplete
                current_token = current_token + char 
        else:
            #add to current token if a token is still uncomplete
            current_token = current_token + char
    add_token(current_token, index)
    current_token = ''
    return tokens

#function to split input into tokens
def file_lexer(input_string, console_index):
    comment = False
    block_comment = False
    current_token = ''
    tokens = []
    found_quotes = 0
    #helper function to add tokens
    def add_token(token, index):
        #adds token to current row, as that will be the last one added
        nonlocal tokens, line, block_comment
        #if inside a block comment, discard everything
        if block_comment == True:
            #check if closing symbol is  in the current token
            if '/#'  in token:
                block_comment = False
            else:
                return True
        keywords = {'make', 'if', 'elif', 'else', 'then', 'and', 'or', 'display', 'type', 'len', 'free', 'input', 'while', 'for', 'in', 'do', 'return', 'func', '->', 'class', 'new', 'break', 'global', 'nonlocal', 'open', 'as', 'import', 'link'}
        types = {'flt', 'str', 'array', 'var', 'bool', 'void', 'instance'}
        booleans = {'True', 'False'}
        #variables that need to be called but can't be used as normal names
        special_vars = {'parent.__init__'}
        #token is a string if there has been an even number of quotes found
        if found_quotes != 0 and found_quotes % 2 == 0:
            tokens[-1].append(Token(token, 'str', index - len(current_token), line))
        else:
            #define matching patterns
            float_reg = re.compile(r'^[0-9.-]+$')
            var_reg = re.compile(r'^[_a-zA-Z0-9]+$')
            path_reg = re.compile(r'^[_a-zA-Z0-9/.\\\\]+$')
            op_reg = re.compile(r'^[+\-*/]+$|^[\**]+$|^[%]+$')
            assign_reg = re.compile(r'^[=]+$')
            compare_reg = re.compile(r'^[==]+$|^[!=]+$|^[<=]+$|^[>=]+$|^[<]+$|^[>]+$')
            container_reg = re.compile(r'^[{]+$|^[}]+$')
            orderer_reg = re.compile(r'^[(]+$|^[)]+$')
            seperator_reg = re.compile(r'^[,]+$|^[:]+$')
            changer_reg = re.compile(r'^[\[]+$|^[\]]+$')
            #check for block comment
            if '#/' in token:
                block_comment = True
                return True
            #check if it is a comment. Strings are checked first, so it won't interfere
            elif '#' in current_token:
                return True
            #check if it is one of the keywords
            elif token in keywords:
                tokens[-1].append(Token(token, 'keyword', index - len(current_token), line))
            #check if it is a type
            elif token in types:
                tokens[-1].append(Token(token, 'type', index - len(current_token), line))
            #check if it is a changer seperator
            elif changer_reg.search(token):
                tokens[-1].append(Token(token, 'changer', index - len(current_token), line))
            #check for mathmatical operator
            elif op_reg.search(token):
                tokens[-1].append(Token(token, 'op', index - len(current_token), line))
            #check if it is only numeric
            elif float_reg.search(token):
                tokens[-1].append(Token(token, 'flt', index - len(current_token), line))
            #check if it is only boolean
            elif current_token in booleans:
                tokens[-1].append(Token(token, 'bool', index - len(current_token), line))
            #check if it is a valid variable name
            elif var_reg.search(token):
                tokens[-1].append(Token(token, 'var', index - len(current_token), line))
            #check if self. variable
            elif 'self.' in token and var_reg.search(token[5:]):
                tokens[-1].append(Token(token, 'var', index-len(current_token), line))
            #check if it is a special variable name
            elif current_token in special_vars:
                tokens[-1].append(Token(token, 'special_var', index - len(current_token), 0))
            #check if it is a assignment equals; length check makes = assignment but == a compare
            elif assign_reg.search(token) and len(token) == 1:
                tokens[-1].append(Token(token, 'assign', index - len(current_token), line))
            #check if it is a valid comparison
            elif compare_reg.search(token):
                tokens[-1].append(Token(token, 'comp', index - len(current_token), line))
            #check if it is a path
            elif path_reg.search(token):
                tokens[-1].append(Token(token, 'path', index - len(current_token), line))
            #check if it is a container
            elif container_reg.search(token):
                tokens[-1].append(Token(token, 'container', index - len(current_token), line))
            #check if it is a paren for math
            elif orderer_reg.search(token):
                tokens[-1].append(Token(token, 'orderer', index - len(current_token), line))
            #check if it is a comma seperator
            elif seperator_reg.search(token):
                tokens[-1].append(Token(token, 'seperator', index - len(current_token), line))
            #ignore whitespace
            elif current_token in {' ', ''}:
                pass
            #error if anything else occurs
            else:
                #check if there is a missing quote mark
                if found_quotes % 2 != 0:
                    out_length = len(f'[Out_{console_index}]: ')
                    print(f'[Out_{console_index}]: Syntax Error: Expected \'')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (index - len(current_token)) + '^')
                    raise Lexer_Error('Missing Quote')
                else:
                    print(current_token)
                    out_length = len(f'[Out_{index}]: ')
                    print(f'[Out_{console_index}]: Syntax Error: Invalid Syntax. Missing Space?')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (index - len(current_token)) + '^' * len(token))
                    raise Lexer_Error('')
            #index - len(current_token)
            return False
    #split file into rows
    rows = input_string.splitlines()
    #loop through all rows
    for line, row in enumerate(rows):
        #add new row to tokens
        tokens.append([])
        #loop through all input charachters
        for index, char in enumerate(row):
            if char == "'":
                #check if any quotes have been found, respond accordingly
                found_quotes += 1 
                if found_quotes == 3:
                    out_length = len(f'[Out_{console_index}]: ')
                    print(f'[Out_{console_index}]: Syntax Error: Expected \'')
                    print(' ' * out_length + input_string)
                    print(' ' * out_length + ' ' * (index - len(current_token)) + '^')
                    raise Lexer_Error('Extra_Quote_Mark')
            #check if it is a comment
            #elif char == '#':
                
            #if a token is finished, figure out what it is
            elif char == ' ':
                #total quotes will be divisible by two if a string is completed or if there is no string now
                if found_quotes % 2 == 0:
                    #add token will return true if a comment is coming next
                    if add_token(current_token, index):
                        comment = True
                        continue
                    current_token = ''
                    found_quotes = 0
                else:
                    #add to current token if a token is still uncomplete
                    current_token = current_token + char 
            else:
                #add to current token if a token is still uncomplete
                current_token = current_token + char
        #add last token
        #do safety checks before adding the final token
        if row != '':
            add_token(current_token, index)
            comment = False
        #remove current line if there is nothing in the line
        if len(tokens[-1]) == 0:
            tokens.pop()
        #reset found quotes
        found_quotes = 0
        #reset current token
        current_token = ''
    return tokens