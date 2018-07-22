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
        X = []
        Y = []
        # Create a new model
        m = Model(model_name)
    
        # Create variables
        for i in range(len(A)):
            X.append([])
            Y.append(m.addVar(vtype=GRB.BINARY, name="y_" + str(i)))
            for j in range(len(A)):
                    X[i].append(m.addVar(vtype=GRB.BINARY, name="x_" + str(i) + "_" + str(j)))
                    
    
    
        # Restrição itens tem que caber
        
        for i in range(len(A)):
            S1 = 0
            for j in range(len(A)):
                S1 += X[i][j]*A[j]    
            m.addConstr(S1<=V*Y[i], "itqc_" + str(i))
            
    
        # Item só pode ta num lugar
        
        for i in range(len(A)):
            S2 = 0
            for j in range(len(A)):
                S2 += X[j][i]    
            m.addConstr(S2==1, "sptnl_" + str(i))
        
       
    
        # Set objective
        S3=0
        for i in range(len(Y)):
            S3+=Y[i]
        m.setObjective(S3, GRB.MINIMIZE)
        
        m.optimize()
    
        #for v in m.getVars():
        #    print('%s %g' % (v.varName, v.x))
    
        print('Obj: %g' % m.objVal)
    
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))
    
    except AttributeError:
        print('Encountered an attribute error')



with open("testFiles/instancia1.txt", "r") as arch:
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
#gurobi_AHA([4, 3, 2, 5, 3], 6, "teste")