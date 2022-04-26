"""
Created April 24, 2022
Author: Willy Lin
Quine McCluskey EE-26 Project
"""
import pandas as pd
import csv
from functools import reduce
import numpy as np

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

def mintermsToPIs(minterms,dont_cares):

    print("The minterms are: ", minterms)
    print("The don't cares are ", dont_cares)
    
    # number of 1s bits per integer 
    zero_bit = [0]
    one_bit = [1,2,4,8]
    two_bit = [3,5,6,9,10,12]
    three_bit = [7,11,13,14]
    four_bit = [15]
    
    #combine minterms and dont cares
    
    
    
    # Orders the minterms into arrays in the 0's column of the chart
    m = set(minterms).union(set(dont_cares))
    n_0_bit = [x for x in zero_bit if x in m]
    n_1_bit = [x for x in one_bit if x in m]
    n_2_bit = [x for x in two_bit if x in m]
    n_3_bit = [x for x in three_bit if x in m]
    n_4_bit = [x for x in four_bit if x in m]
    
    #adds bools to the end of the 0's cube column
    n_0_bit = addBool(n_0_bit)
    n_1_bit= addBool(n_1_bit)
    n_2_bit= addBool(n_2_bit)
    n_3_bit= addBool(n_3_bit)
    n_4_bit= addBool(n_4_bit)
    
    # finds all the one's cubes 
    onescube0,n_0_bit,n_1_bit= _getOnes(n_0_bit,n_1_bit)
    onescube1,n_1_bit,n_2_bit= _getOnes(n_1_bit,n_2_bit)
    onescube2,n_2_bit,n_3_bit= _getOnes(n_2_bit,n_3_bit)
    onescube3,n_3_bit,n_4_bit= _getOnes(n_3_bit,n_4_bit)
    
    
    # finds all the two's cubes
    twocube0,onescube0,onescube1 = _getTwos(onescube0,onescube1)
    twocube1,onescube1,onescube2 = _getTwos(onescube1,onescube2)
    twocube2,onescube2,onescube3 = _getTwos(onescube2,onescube3)
    
    print("0's True means it has been checked off: ")
    print(n_0_bit)
    print(n_1_bit)
    print(n_2_bit)
    print(n_3_bit)
    print(n_4_bit)
    
    print("ones cubes")
    print(onescube0)
    print(onescube1)
    print(onescube2)
    print(onescube3)
    
    print("twos cube")
    print(twocube1)
   
    
    unuseds = []
    # adds all of the cubes into one list so that we can find the Essential PIs
    all_lists = n_0_bit + n_1_bit + n_2_bit + n_3_bit + n_4_bit + onescube0 + onescube1 + onescube2 + onescube3 + twocube1
    unuseds = findUnuseds(all_lists)

    print("Prime Implicants are: ",unuseds)
    print("Now looking for Essential PIs")
    
    return unuseds
    
          

def main():
    minterms = []
    dc = []
    (minterms,dc) = read_in()
    unuseds = mintermsToPIs(minterms[0],dc[0])  


main()