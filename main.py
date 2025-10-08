#import standard libraries
import traceback
#import files
import lexer
import parser
import interpreter
#main file running function
def main():
    #function to run a file
    def run_file(path):
        #try to open the file
        try:
            with open(path, 'r') as file:
                file = file.read()
        except FileNotFoundError:
            print(f'File Not Found Error: File "' + path + '" Does not exist')
            print()
            print('---')
            print()
            return
        #run program if it loads succesfully
        #split input into lines
        file = file.splitlines()
        #tokenize input string 
        try:
            tokens = lexer.file_lexer(file, 0, path)
        #handle errors
        except lexer.Lexer_Error:
            return
        #parse input command
        try:
            syntax_tree = parser.file_parser(tokens, 0, file, path)
        #handle errors
        except parser.Parser_Error:
            return
        #interpret command to python code
        try:
            interpreter.file_interpreter(syntax_tree, 0, file, path)
        #handle errors
        except interpreter.Interpreter_Error:
            return
        print()
        print('---')
        print()
    #function to actully run the console
    def console_loop():
        #set up running Variables
        running = True
        #main console loop
        while running:
            #get input
            input_string = input('Path: ')
            print()
            #tokenize input string 
            run_file(input_string)
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
            #print exception; using traceback library to get full error without crashing
            print(f'Console Source Code Error:')
            print()
            print(traceback.format_exc())
            exception_found = True
        #restarting console loop from inside except causes all previous excpetions to be printed when a new exception occurs
        if exception_found:
            #restart console loop
            run_console()
    #run the console
    run_console()
#run main function
main()