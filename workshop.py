import time
from utils import *


class Workshop:
    def __init__(self):
        self.time = 0 # tiempo actual
        self.duration = 480 # jornada laboral de 8h
        self.client_count = 0 # cantidad de clientes atendidos por el taller
        self.profit = 0 # dinero ganado hasta el momento
        
        self.v1  = 0 # clientes atendidos por el vendedor 1
        self.v2  = 0 # clientes atendidos por el vendedor 2
        self.t1  = 0 # clientes atendidos por el técnico 1
        self.t2  = 0 # clientes atendidos por el técnico 2
        self.t3  = 0 # clientes atendidos por el técnico 3
        self.ts1 = 0 # clientes atendidos por el técnico especializado 1
        
        self.vendedores = [None, None]
        self.tecnicos = [None, None, None]
        self.tecnicos_especializados = [None]
        self. cola = PQueue()
        
        print("opening Shop...")
        
        def generate_new_client(self):
            pass
        def attend_seller(self, client):
            pass
        def action_seller(self, client, worker):
            pass
        def attend_tech(self, client):
            pass
        def action_tech(self, client, worker):
            pass
        def attend_spectech(self, client):
            pass
        def action_spectech(self, client, worker):
            pass
        def handler(self):
            pass