""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    nc = 0 #räknare för hur många punkter som hamnar inuti cirkeln
    
    inpointsx = [] #inuti cirkeln
    outpointsx = [] #inuti cirkeln
    inpointsy = []  # utanför cirkeln
    outpointsy = [] #utanför cirkeln
    for i in range(n):
        x = random.uniform(-1,1) #skapar ett x värde
        y = random.uniform(-1,1) #skapar ett y värde
        if x**2+y**2 <= 1: # kollar ifall den är inuti cirkeln
            nc += 1 
            inpointsx.append(x)
            inpointsy.append(y)
        else:
            outpointsx.append(x)
            outpointsy.append(y)
    pi_estimate = 4*nc/n # Estimerar pi 
    
    print(f"n = {n}")
    print(f"pi ≈ {pi_estimate}")
    
    plt.figure() #graf  
    plt.scatter(inpointsx,inpointsy,color = 'red')
    plt.scatter(outpointsx,outpointsy,color = 'blue')
    
    return pi_estimate

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    nc = 0 # igen en räknare som räknar mängden punkter som är "inuti" "sfären"

    for i in range(n):
        point = [random.uniform(-1,1) for _ in range(d)] # skapar n mängd punkter i den d:e dimensionen 

        sum_sq = sum(map(lambda x: x**2, point)) #räknar ut distansen till "origo"

        if sum_sq <= 1: # om den är inuti "sfären" så ökas räknaren 
            nc += 1

    volym = (2**d)*(nc / n) # räknar ut uppskattad volym

    return volym


def hypersphere_exact(n,d): #Ex2, real value
     #n is the number of points
    # d is the number of dimensions of the sphere 
    return (m.pi**(d/2))/m.gamma(d/2 + 1) #Räknar ut volymen exakt 



#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
      #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    with future.ProcessPoolExecutor(max_workers=np) as ex:
        list_n = [n] * np
        list_d = [d] * np

        resultat = list(ex.map(sphere_volume, list_n, list_d))

    return mean(resultat)

    
    


#Ex4: parallel code - parallelize actual computations by splitting data
def count_inside(n, d): #hjälpfunktione som räknar antalet punkter i "sfären"
    nc = 0
    for i in range(n): #loopar n gånger
        point = [random.uniform(-1,1) for i in range(d)] #slumpmässig punkt i sfären
        if sum(x**2 for x in point) <= 1:
            nc += 1 #kontrollerar om punkten är i sfären 
    return nc
def sphere_volume_parallel2(n,d,np=10):#samma som trean den bara delar upp arbetet 
      #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    
    chunk = n // np  # dela upp arbetet

    list_n = [chunk] * np #skapar input till varje process 
    list_d = [d] * np

    with future.ProcessPoolExecutor(max_workers=np) as ex:#startar parallel pool 
        results = list(ex.map(count_inside, list_n, list_d))

    total_nc = sum(results) #summerar alla inside counts

    volume = (2**d) * (total_nc / n) #estimerar volymen

    return volume
    
    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    #Ex3
    n = 100000
    d = 11
    resultat=[]
    start = pc()
    for y in range (10):
        a=sphere_volume(n,d)
        resultat.append(a)
    average_resultat=sum(resultat)/len(resultat)
    stop = pc()
    print(average_resultat)
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    start1=pc()
    sphere_volume_parallel1(100000,11)
    stop1=pc()
    print(f"parallel time is {stop1-start1}")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    start2=pc()
    sphere_volume_parallel2(1000000, 11)
    stop2=pc()
    print(f"parallel times is {stop2-start2}")

    
    

if __name__ == '__main__':
	main()
