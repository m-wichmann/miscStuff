#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""This tool tries to analyse python source code and determine the computational complexity"""

# TODO:
# - be able to use multiple files
# - really do something ;-)

#####
#cc_calc
#
#Copyright 2012, erebos42 (https://github.com/erebos42/miscScripts)
#
#This is free software; you can redistribute it and/or modify it
#under the terms of the GNU Lesser General Public License as
#published by the Free Software Foundation; either version 2.1 of
#the License, or (at your option) any later version.
#
#This software is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this software; if not, write to the Free
#Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
#02110-1301 USA, or see the FSF site: http://www.fsf.org.
#####

import ast

def main():
    """main function"""

    # TODO: use options parser to specify file

    # open source code under analysis
    fd = open('test.py', 'r')

    # concat source code to a string...
    code = ""
    for line in fd:
        code = code + line

    # parse code using ast
    parsetree = ast.parse(code)

    # get first level of child nodes
    gen = ast.iter_child_nodes(parsetree)

    # create return var
    ret = []

    # go recursively through the nodes
    listchildnodes(gen, ret, 0)

    # TODO: analyse ret
    
    





def listchildnodes(node, ret, num):
    """go recursively through all nodes. node=parent node, ret=return buffer, num=level in the tree"""

    # keep running until there are no child nodes...
    keeprunning = True
    while keeprunning:
        # try to get the next child...
        try:
            # get the next node and append to the return list
            next = node.next()
            ret.append(next)

            # output the tree in a "formatted" fashion
#            blank = ""
#            for i in xrange(num):
#                blank = blank + " "
#            print blank + str(type(next))

            # get next level of child nodes
            gen = ast.iter_child_nodes(next)

            # create a sublist
            subret = []
            
            # go through next level of child nodes
            listchildnodes(gen, subret, num + 1)

            # only append the sublist if it isn't empty
            if len(subret) > 0:
                ret.append(subret)

        # ...otherwise stop iteration
        except StopIteration:
            keeprunning = False

if __name__ == '__main__':
    main()

















