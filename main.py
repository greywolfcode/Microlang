#TODO:
#fix all remaining bugs :)
#make error correction code point to the correct spot in the input string
#add for loops: for STATEMENT then STATEMENT
#add iterating through arrays to for loop
#raise error in parser if elif/else do not have a parent
#single raise error function
#fill in all missing areas requireing raise error
#add importing microlang files with: import FILENAME
#add opening files with: open FILEPATH {}
#add break command for loops
#add global and nonlocal commands for functions
#make parents for classes work

#import standerd libraries
import traceback
#import files
import lexer
import parser
import interpreter
#startup prints
print('Welcome to the Micro Console')
print('"We are not just a fancy calculator ™"')
print()
print('type "help" to get help')
print()
#setup input counter
index = 1
#main console function
def main():
    #function to run a file
    def run_file(path):
        global index
        #try to open the file
        try:
            with open(path, 'r') as file:
                file = file.read()
        except FileNotFoundError:
            print(f'[Out_{index}]: File ' + path + ' Does not exist')
            print()
            index += 1
            return
        #increase index and put out
        print(f'[Out_{index}]:')
        #run program if it loads succesfully
        #tokenize input string 
        try:
            tokens = lexer.file_lexer(file, index)
        #handle errors
        except lexer.Lexer_Error:
            index += 1
            return
        #parse input command
        try:
            syntax_tree = parser.file_parser(tokens, index, file)
        #handle errors
        except parser.Parser_Error:
            index += 1
            return
        #interpret command to python code
        try:
            interpreter.file_interpreter(syntax_tree, index, file)
        #handle errors
        except interpreter.Interpreter_Error:
            index += 1 
            return
        #increase index and print space
        index += 1
        print()
    #function to actully run the console
    def console_loop():
        #get input counter
        global index
        #set up running Variables
        running = True
        #main console loop
        while running:
            #get input
            input_string = input(f'[In_{index}]: ')
            #check for special console-only keywords
            match input_string:
                #ends the program
                case 'quit':
                    #loop until valid input is given
                    while True:
                        check = input('Y/N: ')
                        if check.upper() == 'Y':
                            interpreter.clear_vars()
                            #exit program
                            running = False
                            print('')
                            break
                        elif check.upper() == 'N':
                            print(f'[Out_{index}]:')
                            print('')
                            break
                    index += 1
                    continue
                #clears all console entries
                case 'clear_console':
                    #loop until valid input is given
                    while True:
                        check = input('Y/N: ')
                        if check.upper() == 'Y':
                            #clear console - see https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
                            print("\033[H\033[J", end="")
                            #reprint title stuff
                            print('Welcome to MiniCon')
                            print('"We are not just a fancy calculator ™"')
                            print()
                            print('type "help" to get help')
                            print()
                            break
                        elif check.upper() == 'N':
                            print(f'[Out_{index}]:')
                            print()
                            break
                        else:
                            print('Syntax Error: Invalid Entry')
                            print('')
                    index += 1
                    continue
                #clears all console entries and resets index to 1
                case 'reset_console':
                    #loop until valid input is given
                    while True:
                        check = input('Y/N: ')
                        if check.upper() == 'Y':
                            #clear console - see https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
                            print("\033[H\033[J", end="")
                            #reprint title stuff
                            print('Welcome to MiniCon')
                            print('"We are not just a fancy calculator ™"')
                            print()
                            print('type "help" to get help')
                            print()
                            index = 1
                            break
                        elif check.upper() == 'N':
                            print(f'[Out_{index}]:')
                            print()
                            index += 1
                            break
                        else:
                            print('Syntax Error: Invalid Entry')
                            print('')
                    continue
                #clears all variables
                case 'clear_vars':
                    #loop until valid input is given
                    while True:
                        check = input('Y/N: ')
                        if check.upper() == 'Y':
                            interpreter.clear_vars()
                            print(f'[Out_{index}]: Variables Cleared')
                            print('')
                            break
                        elif check.upper() == 'N':
                            print(f'[Out_{index}]:')
                            print('')
                            break
                        else:
                            print('Syntax Error: Invalid Entry')
                            print('')
                    index += 1
                    continue
                #displays all variables
                case 'display_vars':
                    interpreter.display_vars(index)
                    index += 1
                    continue
                #prints help menu
                case 'help':
                    print(f'[Out_{index}]:')
                    print('Put spaces between all tokens except inside of strings')
                    print()
                    print('Type "display_vars" to see all variables')
                    print('Type "clear_vars" to see clear all variables')
                    print('Type "clear_console" to clear the console')
                    print('Type "reset_console" to reset the console')
                    print('type "quit" to quit')
                    print()
                    print('Set variable: make TYPE VARIABLE_NAME = VALUE \n Types: flt = float, str = string, array = array, var = variable (only for making a varible equal to another)')
                    print('If statment: if COMPARISON then STATEMENT elif COMPARISON then STATEMENT else STATEMENT \n ==, !=, <=, >=, <, >, and, or')
                    print('Math operators: +, -, *, /, **')
                    print("make array: { 0 , 9 , a , 'm' } etc.")
                    print('booleans: True, False')
                    print()
                    print('Get charachter from string: [ STRING , FLOAT ] \n Positive float starts at the begining, negative float starts at the end. Starts at 0')
                    print('Get value from array: [ ARRAY , FLOAT ] \n Positive float starts at the begining, negative float starts at the end. Starts at 0')
                    print('Change Type: [ VALUE , TYPE ] \n returns object of new type')
                    print('Get type: [ VALUE , get ] \n returns string containing type')
                    print('Get length of object [ VALUE , len ] \n returns flt containing type')
                    print()
                    index += 1
                    continue

            #check if running a file
            command = input_string.split(' ')
            if len(command) == 2:
                if command[0] == 'run':
                    run_file(command[1])
                    continue
            #add extra space; helps lexer not break
            input_string = input_string + ' '
            #tokenize input string 
            try:
                tokens = lexer.lexer(input_string, index)
            #handle errors
            except lexer.Lexer_Error:
                index += 1
                continue
            #parse input command
            try:
                syntax_tree = parser.parser(tokens, index, input_string)
            #handle errors
            except parser.Parser_Error:
                index += 1
                continue
            #interpret command to python code
            try:
                interpreter.interpreter(syntax_tree, index, input_string)
            #handle errors
            except interpreter.Interpreter_Error:
                index += 1 
                continue
            #increase index
            index += 1
    #function to prevent console from crashing during errors
    def run_console():
        '''Runs console loop and handle exceptions'''
        #store if var is found
        exception_found = False
        #catch and print errors without crash console so other tests can be done
        try:
            #run main console function
            console_loop()
        except Exception as e :
            global index
            #print exception; using traceback library to get full error without crashing
            print(f'[Out_{index}]: Console Source Code Error:')
            print()
            print(traceback.format_exc())
            exception_found = True
            #increase console index
            index += 1
        #restarting console loop from inside except causes all previous excpetions to be printed when a new exception occurs
        if exception_found:
            #restart console loop
            run_console()
    #run the console
    run_console()
#run main function
main()
print('Closing Console...')