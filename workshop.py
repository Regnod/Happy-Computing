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
        
        self.next_client = 0 # tiempo de arribo del proximo cliente
        self.next_a_client = 0 # tiempo de arribo de un cliente después que el vendedor atiende un cliente
        
        self.vendedores = [0, None, None] # cantidad de clientes atendidos por los vendedores, seguido de 2 vendedores
        self.tecnicos = [0, None, None, None] # cantidad de clientes atendidos por los técnicos, seguido de 3 técnicos
        self.tecnicos_especializados = [0, None] # cantidad de clientes atendidos por el técnico especializado, seguido de 1 técnico especializado
        self.cola = PQueue()
        
        print("opening Shop...")
        
    def generate_new_client(self):
        self.next_client = self.time + poisson(20)
        next_client = Client(choose_service(), self.ta)
        self.cola.push(next_client)
        return self.ta
    
    def attend_seller(self, client):
        if self.vendedores[1] is not None and self.vendedores[2] is not None:
            # aumentar el tiempo de espera
            client.time += seller_action_time()
            self.cola.push(client)
        elif self.vendedores[1] is None:
            self.vendedores[0]+=1
            self.vendedores[1] = client
            self.v1 += 1
            self.action_seller(client, 1)
        else:
            self.vendedores[0]+=1
            self.vendedores[2] = client
            self.v2 += 1
            self.action_seller(client, 2)

    def action_seller(self, client, worker):
        service = client.service
        client.time += seller_action_time()
        # determinar que estado le corresponde al cliente
        if service == 4:
            client.state = "Completed"
        elif service == 3:
            client.state = "Spec Tech"
            self.third_service = True
        else:
            client.state = "Tech"    
        
        self.vendedores[0] -= 1
        self.vendedores[worker] = None
        self.cola.push(client)

    def attend_tech(self, client):
        pass
    def action_tech(self, client, worker):
        pass
    def attend_spectech(self, client):
        pass
    def action_spectech(self, client, worker):
        pass
    def handler(self):
        client = self.cola.pop()
        
        if client.state == "Seller":
            self.time = client.time
            self.client_count += 1
            self.attend_seller(client)
            self.next_client = self.generate_new_client()