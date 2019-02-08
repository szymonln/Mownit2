from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import random

#zad1
points = []
number = 60

initial_order = []
for i in range(number):
    points.append((random.random(), random.random()))
    initial_order.append(i)


def get_distance(order):
    dist = 0
    last = points[order[0]]
    for n in order[1:]:
        dist += np.linalg.norm(np.array(points[n])-np.array(last))
        last = points[n]
    return dist


def change_order(o):
    order =o.copy()
    idx = random.randint(0, len(order)-2)
    order[idx], order[idx+1] = order[idx+1], order[idx]
    return order

temp = 1
min_temp = 0.00001


def accept(old, new, temp):
    if old > new:
        return True
    else:
        return np.exp((old - new)/temp)


solution = initial_order
history = []
while temp > min_temp:
    new_solution = change_order(solution)
    new_cost = get_distance(new_solution)
    old_cost = get_distance(solution)
    if (accept(old_cost, new_cost, temp)):
        solution = new_solution
    temp = 0.999 * temp
    history.append(get_distance(new_solution))

plt.plot(history)
plt.show()

#zad2
random_pixels = np.random.randint(4, size=(20, 20))
plt.imshow(random_pixels)
plt.show()


def get_energy (array):
    [h,w] = array.shape
    energy = 0
    for y in range(0,h):
        for x in range(0,w):
            energy += (abs(y-h/2) + abs(x-w/2))*array[x][y]
    return energy

def mutate_img(a):
    array = a.copy()
    [h,w] = array.shape
    if(random.random()>0.5):
        idx = random.randint(0, w - 1)
        idy = random.randint(0, h - 2)
        array[idx][idy],array[idx][idy+1] = array[idx][idy+1],array[idx][idy]
    else:
        idx = random.randint(0, w - 2)
        idy = random.randint(0, h - 1)
        array[idx][idy],array[idx+1][idy] = array[idx+1][idy],array[idx][idy]
    return array


temp = 11
minTemp = 0.00001
iteration = 1
solutions = {}
solutions[0] = random_pixels

solution = random_pixels
while(temp > minTemp):
    new_solution = mutate_img(solution)
    new = get_energy(new_solution)
    old = get_energy(solution)
    if(accept(old, new, temp)):
        solution = new_solution
    if(iteration % 1000 == 0):
        solutions[iteration] = solution
    temp = 0.999 * temp
    iteration+=1

plt.imshow(solution)
plt.show()

