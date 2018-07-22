# -*- coding: utf-8 -*-
"""
Created on Fri Jun 08 15:42:34 2018

@author: github.com/paulorcmendes
@author: github.com/andsfonseca
@author: github.com/robertrdas
@author: github.com/elheremes
"""

import re as re
from gurobipy import *

def gurobi_AHA(A, V, model_name):
    try:
        # Create a new model
        m = Model(model_name)
        # Create variables
       
        X = m.addVars(len(A), len(A), vtype=GRB.BINARY, name = "x")    	
        Y = m.addVars(len(A), vtype=GRB.BINARY, name="y")
        # Restrição itens tem que caber

        m.addConstrs(( sum([X[j,i]*A[j] for j in range(len(A))]) <= V*Y[i] for i in range(len(A))), "itqc")
        
        # Item só pode ta num lugar
        m.addConstrs((sum([X[i,j] for j in range(len(A))]) == 1 for i in range(len(A))), "sptnl")
        
        # Set objective
            
        m.setObjective(sum([Y[i] for i in range(len(A))]), GRB.MINIMIZE)
        
        
        m.optimize()
    
       #for v in m.getVars():
       #    print('%s %g' % (v.varName, v.x))
    
        print('Obj: %g' % m.objVal)
        
        
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))
    
    except AttributeError:
        print('Encountered an attribute error')


with open("testFiles/binpack3.txt", "r") as arch:
    fileList = arch.read().replace(" ", "\n").split("\n")
    
    fileList = filter(lambda a: a != '', fileList)
    P = int(fileList.pop(0))

    l_temp = re.split(r'(u\d+_\d+)', ' '.join(fileList))

    fileList = [[item] + l_temp[i+1].strip().split(' ') 
        for i, item in enumerate(l_temp) if item.startswith('u')]

    for listA in fileList:
        model_name = listA.pop(0)
        V = int(listA.pop(0))
        listA.pop(0)
        solIdeal = listA.pop(0)
        
        listA = [ int(x) for x in listA ]
       
        gurobi_AHA(listA, V, model_name)
        print "Expected Solution "+solIdeal
        break

#for i in range(P):
    #gurobi(A, V)
#gurobi_AHA([4, 3, 2, 5], 5, "teste")