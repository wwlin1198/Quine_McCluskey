#!/usr/bin/env python3

"""
Created April 24, 2022
Author: Willy Lin
Quine McCluskey EE-26 Project
"""
from numpy import count_nonzero

import csv
from functools import reduce
import numpy as np

from pprint import pprint

def read_in():
    print("in read in")
    #csv file name 
    filename = "values.csv"
    
    #initializing titles and rows 
    minterms = []
    dc = []
    iter = 0

    #reading csv file 
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = list(map(int, row))
            iter += 1
            if(iter % 2 == 0):
                dc.append(row)
            else:
                minterms.append(row)
    return minterms,dc 



def _getOnes(n_a_bit, n_b_bit):
    # This function determs from the input of two 0's arrays all of the one's cubes
    onescube = []
    for i in range(len(n_b_bit)):
        for j in range(len(n_a_bit)): 
            first = n_b_bit[i]
            second = n_a_bit[j]
            diff = first[0] - second[0]
            if (diff == 1 or diff == 2 or diff == 4 or diff == 8 or diff == 16):
                onecube = [first[0], second [0], diff, False]
                onescube.append(onecube)
                n_b_bit[i][1] = True
                n_a_bit[j][1] = True
    return onescube,n_a_bit,n_b_bit

def _getTwos(arr1, arr2):
    #This function determines from the input of two ones cubes arrays if there exists two cubes
    twoscubes=[]
    for i in range(len(arr2)):
        for j in range(len(arr1)):
            first = arr2[i]
            second = arr1[j]
            if first[2] == second[2] and ((first[3] == False) and (second[3] == False)) :
                diff2 = first[0] - second [0]
                twocube = [first[0], first[1], second[0], second[1], first[2] , diff2, False]
                twoscubes.append(twocube)
                arr2[i][3] = True
                arr1[j][3] = True
    return twoscubes,arr1,arr2

def compare(x,y):
    counter = -1;
    out = []
    x = "".join(reversed(x))
    y = "".join(reversed(y))
    for i in range(max(len(x),len(y))):
        l = x[i] if i < len(x) else '0'
        r = y[i] if i < len(y) else '0'

        print(f"{l=},{r=},{i=}")
        if(l == r):
            out.append(l)
            continue
        if counter != -1:
            return False
        counter = i
        out.append('X')
       
    out = reversed(out)

    return "".join(out)
    
    

    


def mintermsToPIs(minterms,dc):

    # print("The minterms are: ", minterms)
    # print("The don't cares are ", dc)
    
    count = {0:{}}    
    mintermsdc = minterms+dc


    for i in range(len(mintermsdc)):
        if(mintermsdc[i] == 0):
            count[0][0] = [bin(0)[2:]]
        elif(bin(mintermsdc[i]).count('1') in count[0]):

            count[0][bin(mintermsdc[i]).count('1')].append(bin(mintermsdc[i])[2:])
        else:

            count[0][bin(mintermsdc[i]).count('1')] = [bin(mintermsdc[i])[2:]]

    # print(count)


    # print(count)

    for i_cubes in range(5): 
        if i_cubes not in count:
            break   
        for i in count[i_cubes].keys():
            count[i_cubes][i].append(False)
        for i in range(max(count[i_cubes].keys()) + 1):
            if i in count[i_cubes] and i+1 in count[i_cubes]:
                for x in count[i_cubes][i][:-1]: 
                    for y in count[i_cubes][i+1][:-1]:
                        print(f"{x=}, {y=}")
                        print(compare(x,y))
                        ones = compare(x,y)
                        if not ones:
                            continue
                        if i_cubes + 1 not in count:
                            count[i_cubes + 1] = {}
                        if ones.count('1') in count[i_cubes+1]:
                            count[i_cubes + 1][ones.count('1')].append(ones)
                        else:
                            count[i_cubes + 1][ones.count('1')] = [ones]
    pprint(count)
            
    
    # print("0's True means it has been checked off: ")
    # print(n_0_bit)
    # print(n_1_bit)
    # print(n_2_bit)
    # print(n_3_bit)
    # print(n_4_bit)
    
    # print("ones cubes")
    # print(onescube0)
    # print(onescube1)
    # print(onescube2)
    # print(onescube3)
    
    # print("twos cube")
    # print(twocube1)
   
    
    unuseds = []
    # # adds all of the cubes into one list so that we can find the Essential PIs
    # all_lists = n_0_bit + n_1_bit + n_2_bit + n_3_bit + n_4_bit + onescube0 + onescube1 + onescube2 + onescube3 + twocube1
    # unuseds = findUnuseds(all_lists)

    # print("Prime Implicants are: ",unuseds)
    # print("Now looking for Essential PIs")
    
    return unuseds
    
          

def main():
    minterms = []
    dc = []
    (minterms,dc) = read_in()
    unuseds = mintermsToPIs(minterms[0],dc[0])  


main()