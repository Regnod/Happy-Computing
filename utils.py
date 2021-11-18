import heapq
import math
import numpy
from numpy.random import default_rng
import random


class Client:
    def __init__(self, service, time):
        self.service : int = service
        self.time = time
        self.state : str = "Seller"
        self.attended_by : str = ''
        self.worker : int = 0
    
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
    u = uniform(0, 1)
    w = round(u, 6)
    try:
        return (-1/lamb)*math.log(w)
    except Exception as e:
        print(e)

def poisson(lamb):
    u = random.random()
    cnt = 0
    while u >= numpy.e**-lamb:
        u = u * (random.random())
        cnt += 1
    return cnt

def seller_action_time():
    return normal_distribution(5, 2)

def repair_time_tech():
    return exp_distribution(20)

def repair_time_spec():
    return exp_distribution(15)


from random import uniform

def normal_distribution(mu, sigma_square):
    u = uniform(0, 1)
    y1 = 0
    y2 = 0
    while y2 - (((y1-1)**2)/2) <= 0:
        y1 = exp_distribution(1)
        y2 = exp_distribution(1)
    u = uniform(0, 1)
    ans = y1 if u > 0.5 else -y1
    return ans* math.sqrt(sigma_square) + mu