#import standard libraries
import traceback
import argparse
#import files
import lexer
import parser
import interpreter
#main file running function
def main():
    #set up parser
    arguments = argparse.ArgumentParser(prog='channelCSonverter', description='Run Microlang source files.')
    arguments.add_argument('sourcePath', help='path to Microlang source file')
    #get arguments
    args = arguments.parse_args()
    #function to run a file
    def run_file(path):
        #try to open the file
        try:
            with open(path, 'r') as file:
                file = file.read()
        except FileNotFoundError:
            print(f'File Not Found Error: File "' + path + '" Does not exist')
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
    #run files
    run_file(args.sourcePath)
#run main function
main()