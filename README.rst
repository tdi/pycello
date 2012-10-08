==========
pycello.py
==========

Some cellular automata fun in curses. 

:Author: Dariusz Dwornikowski
:Version: 0.1

Synopsis
========
::

  pycello.py -h | --help 
  pycello.py -d [delay] | --delay [delay]
  pycello.py -g [GEOM] | --geom [GEOM]
  pycello.py --rand_factor [rand_fact]
  pycello.py --cell_char [character]
  pycello.py --llrule [RULE]

Description
===========

Just a cellular automata fun program in curses, written in Python 3.X. 
Examples:

Run Conway's game of life with delay 0. 

  $ ./pycello.py -d 0 --llrule "B3/S23" 

Options
=======
``-d DELAY``
A delay between drawing next generations.
``--llrule "RULE"``
Life-like game rule. More on rules can be found `here <http://en.wikipedia.org/wiki/Life-like_cellular_automaton>`_ .
``--rand_factor FACTOR`` 
Default: 0.25 means 0.25 of the bord will be filled randomely at start.
``-g GEOM``
Default: max of the terminal. Geometry is given as "XxY" dimensions.
Example: 50x50. 
``--cell_char CHARACTER``
The character to use for a living cell. 

Copyright
=========
(c) 2012 Dariusz Dwornikowski

This program comes with ABSOLUTELY NO WARRANTY.
THIS IS FREE SOFTWARE, AND YOU ARE WELCOME TO REDISTRIBUTE IT UNDER THE TERMS
AND CONDITIONS OF THE MIT LICENSE.  YOU SHOULD HAVE RECEIVED A COPY OF THE
LICENSE ALONG WITH THIS SOFTWARE; IF NOT, YOU CAN DOWNLOAD A COPY FROM HTTP://WWW.OPENSOURCE.ORG.


