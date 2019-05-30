# Nari 🐹
Nari is a stack-based, statically-typed scripting language designed to be powerful, simple and portable.
While it's not as intuitive as [other languages I've designed](https://github.com/lartu/ldpl), nari aims
to suppress some problems those languages had, letting you do more by writting less.

In some obtuse way, nari could be seen as a language opposite to LDPL verbosity.

This repository contains the source code and releases of the nari interpreter.

## How does nari look?
```coffeescript
# First, a hello world! example #
"Hello World!" print                        # push "Hello World!" to the stack and print it #

# Then a disan count #
"Enter a number: " print                    # print "Enter a number: " #
accept toAux(.iterator)                     # accept a number and store it in the var .iterator #
while aux(.iterator) 0 > do                 # while the var .iterator is greater than 0 #
  if aux(.iterator) 2 % 0 = then            # if the var .iterator is even #
    aux(.iterator) " is even!" join print   # then print "<.iterator> is even!" # 
  endif
  aux(.iterator) 1 - toAux(.iterator)       # decrement the value of .iterator #
repeat
```

For information on what's a Disan Count please refer to [this site](https://esolangs.org/wiki/Disan_Count).

## Installation
TODO

## Documentation
TODO

## How can I contribute to the nari language?
TODO

## Where can I get more help, if I need it?
TODO

## License
Nari is distributed under the GNU General Public License 3.0. All nari art is released under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.
