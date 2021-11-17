import heapq
import math
import numpy
from numpy.random import default_rng
import random


class Client:
    def __init__(self, service, time):
        self.service = service
        self.time = time
        self.state = "Seller"
        self.attended = ''
    
    def __le__(self, other):
        return True if self.time <= other else False

    def __gt__(self, other):
        return True if self.time > other else False

    def __lt__(self, other):
        return True if self.time < other else False

    def __ge__(self, other):
        return True if self.time >= other else False

    def __eq__(self, other):
        return True if self.time == other else False

class PQueue(object):
    def __init__(self):
        self.queue = []
        self.waiting_for_change = 0

    def push(self, obj: Client):
        if obj.service == 3:
            self.waiting_for_change += 1
        heapq.heappush(self.queue, obj)

    def pop(self):
        client = heapq.heappop(self.queue)
        if client.service == 3:
            self.waiting_for_change -= 1
        return client

    def waiting_change(self):
        return self.waiting_for_change != 0

    def count(self):
        return len(self.queue)
    
    def empty(self):
        return True if len(self.queue) == 0 else False

def choose_service():
    prob = random.random()
    if prob < 0.45:
        return 1
    elif 0.45 < prob < 0.70:
        return 2
    elif 0.70 < prob < 0.80:
        return 3
    elif 0.80 < prob < 1:
        return 4

def exp_distribution(lamb):
    u = default_rng.uniform()
    w = round(u, 6)
    try:
        return (-1/lamb)*math.log(w)
    except Exception as e:
        print(e)

def poisson(lamb):
    pass

def seller_action_time():
    pass

def discret_uniform_distribution(n):
    u = default_rng.uniform()
    return 1 + int(u*n)

def normal_distribution(mu, sigma_square):
    u = default_rng.uniform()
    y = exp_distribution(1)
    
    if u <= math.pow(math.e(-1*math.pow(y-1, 2))/2):
        ud = discret_uniform_distribution(2)
        if ud == 1:
            y*= -1
        return y* math.sqrt(sigma_square) + mu
    return normal_distribution(mu, sigma_square)