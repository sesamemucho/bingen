========
Usage
========

bingen provides a convenient API to generate binary data. It can
present the data in several formats, including raw binary files, hex
output, assignment fragments for inclusion in to C or C++ or other
programs, or as an iterator for direct use in a Python program.

bingen accepts input in binary, octal, decimal and hex radicies, 

Currently, everything is little-endian. In particular, the elements
are laid out like little-endian gcc bitfields. Remember this when
reading the examples below.

You can use bingen to generate binary data in two ways: first, by
directly using the Python API (it's designed to make this
straightforward), or by parsing a bingen input file. The second way is
a little more concise, but access to Python is not available.

Examples
========

Example 1
---------

This example file shows the simplest way to enter data. There is a
single grouped element of 3 data items (surrounded by the braces
"{}").

The bingen input file

::

  {
    9:0x15A
    4:0xF
    3:6
  }

will produce the 16-bit value 0xDF5A (remember, it's all
little-endian).

Group-elements can have a label for later access::

  Element1: {
    9:0x15A
    4:0xF
    3:6
  }

  
Group-elements can themselves be grouped::

  {
    {
      3:5
      3:6
    }
    {
      3:2
      3:7
    }
    {
      4:0xE
    }
  }
  
=========
Reference
=========

Use cases
=========

HEY! PUT STORIES IN HERE!!!

Three elements, no grouping
~~~~~~~~~~~~~~~~~~~~~~~~~~~

(dot graph goes here, of     9:0x15A
    4:0xF
    3:6
)

At the end of the graph, everything can be evaluated immediately, so
evaluation proceeds right to left (top to bottom in the displayed
graph).

Five elements, one group
~~~~~~~~~~~~~~~~~~~~~~~~

(dot graph of
{
  3:2
  3:6
  Group1: {
    9:0x15A
    4:0xF
    3:6
  }
}

Group1 is the deepest compound item, so it is evaluated first. The top
level is then evaluated right to left.

Three elements, no grouping, one modifier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(dot graph goes here, of    
    16:0x1234 (with BigEndian modifier)
    4:0xF
    4:6
)

At the end of the graph, everything can be evaluated immediately, so
evaluation proceeds right to left (top to bottom in the displayed
graph).



Bingen input file
=================

A bingen input file has the form::

  {
  <Element 1>
  [<Element 2...n>]
  }

An element has one of the two forms::

  [<Label>:] [<Element type>] <element size>:<element value>

where

   Label
     a string without spaces and that does not start
     with a number.
   
   Element Type
     Indicates the type of value. Valid types are: Int, Float,
     String. If not specfied, the type defaults to Int.
   
   Element size
     The length of the item in bits.
   
   Element value
     The value of the item. This may be a numerical constant, for Int
     or Float types, or a unicode string (TBD) for String types. This
     may also be one or more functions.

Bingen API
==========

modifiers
~~~~~~~~~

This is a list of functions that will be applied to change the value
of the element. It is passed to the constructor as a list::

  (modifer1, (modifier2, arg1, arg2), (modifier3, arg1))

modifier1 takes one parameter, the current value of the element.

modifier2 takes two arguments which are the names of two other
elements. It acts on the data from the first element to the last
element, inclusive.

modifier3, yagni?

The modifiers are applied (when they are applied) in right-to-left
order.

=========
Dev notes
=========

Currently, everything is little-endian. In particular, the elements
are laid out like little-endian gcc bitfields.

Elements that have modifier functions must have a length that matches
a C integer type: char, short, long, long long.

#No: Groups must have a length that matches a C integer type.

An element (or group) may be converted to big-endian (via
to_bigendian), but the element's size must be that of a C integer
type. It is not required that the element also be aligned on an
integer type boundary (that is, a 16-bit quantity can be converted to
big-endian even though it is on an odd byte boundary).

Maybe: Switch between big and little endian modes?

Unless otherwise mentioned, the modifier functions that come with
bingen operate on bytes. 
