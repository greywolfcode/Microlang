# Microlang
A small scripting language written in Python
## Requirements
- Python3
- Python standard library
## Setup 
Clone the repository and have python installed.
## Usage
Run the main file, then enter the path to your .microlang source file. Note that the path needs to be a full path or relative to your installation of the interpreter files.
## Syntax
```python3
#print string to console
display 'Hi!'

#make a variable of type float
make flt a = 0

#basic function that returns an int
func basicFunc [ int b ] -> int
{
  make int c = b * 2
  return c
}

#call the function
make int d = basicFunc [ a ]

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
