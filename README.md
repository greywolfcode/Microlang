# Microlang
A small scripting language written in Python
## Requirements
- Python3
- Python standard library
## Setup 
Clone the repository 
## Usage
Run the main file with your source file as an argument. Note that the path needs to be a full path or relative to your installation of the interpreter files.
## Syntax
```python3
#print statement
display 'Hi!'

#make a variable
make int a = 0

#basic function
func basicFunc [ int b ] -> int
{
  make flt c = b * 2
  return c
}

#call the function
make int c = basicFunc [ a ]

#if statements
if ( a < 2 )
{
  display 'a is less than 2'
}
elif ( a > 2 )
{
  display 'a is greate than 2'
}
else
{
  display 'a equals 2'
}
```
See the tutorial folder for all syntax tutorials.
