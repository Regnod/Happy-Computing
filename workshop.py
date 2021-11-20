from utils import *

class Workshop:
    def __init__(self):
        self.time = 0 # tiempo actual
        self.duration = 480 # jornada laboral de 8h
        self.client_count = 0 # cantidad de clientes atendidos por el taller
        self.profit = 0 # dinero ganado hasta el momento
        self.third_s = False 
        
        self.v1  = [0] # clientes atendidos por el vendedor 1
        self.v2  = [0] # clientes atendidos por el vendedor 2
        self.t1  = [0] # clientes atendidos por el técnico 1
        self.t2  = [0] # clientes atendidos por el técnico 2
        self.t3  = [0] # clientes atendidos por el técnico 3
        self.ts1 = [0] # clientes atendidos por el técnico especializado 1
        
        self.arrivals = []
        self.exits = []
        
        self.next_client = 0 # tiempo de arribo del proximo cliente
        
        self.vendedores = [0, None, None] # cantidad de clientes atendidos por los vendedores, seguido de 2 vendedores
        self.tecnicos = [0, None, None, None] # cantidad de clientes atendidos por los técnicos, seguido de 3 técnicos
        self.tecnicos_especializados = [0, None] # cantidad de clientes atendidos por el técnico especializado, seguido de 1 técnico especializado
        self.cola = PQueue()
        
        # print("opening Shop...")
    
    def third_service(self):
        return self.cola.waiting_change()
    
    def generate_new_client(self):
        self.next_client = self.time + poisson(20)
        if self.next_client > self.duration:
            return self.time
        self.arrivals.append(self.next_client)
        next_client = Client(choose_service(), self.next_client)
        next_client.arrival_time = self.next_client
        self.cola.push(next_client)
        return self.next_client
    
    def attend_seller(self, client):
        if self.vendedores[1] is not None and self.vendedores[2] is not None:
            # aumentar el tiempo de espera
            client.time += seller_action_time()
            self.cola.push(client)
        elif self.vendedores[1] is None and self.vendedores[2] is None:
            u = random.uniform(0,1)
            if u < 0.5:
                self.vendedores[0]+=1
                self.vendedores[1] = client
                self.v1[0] += 1
                client.worker = 1
            else:
                self.vendedores[0]+=1
                self.vendedores[2] = client
                self.v2[0] += 1
                client.worker = 2
        elif self.vendedores[1] is None:
            self.vendedores[0]+=1
            self.vendedores[1] = client
            self.v1[0] += 1
            client.worker = 1
        else:
            self.vendedores[0]+=1
            self.vendedores[2] = client
            self.v2[0] += 1
            client.worker = 2
        self.action_seller(client, client.worker)

    def action_seller(self, client, worker):
        service = client.service
        client.time += seller_action_time()
        # determinar que estado le corresponde al cliente
        if service == 4:
            client.state = "Completed"
        elif service == 3:
            client.state = "Spec Tech"
            self.third_s = True
        else:
            client.state = "Tech"    
        
        self.vendedores[0] -= 1
        self.vendedores[worker] = None
        self.cola.push(client)

    def attend_tech(self, client):
        if self.tecnicos[1] is not None and self.tecnicos[2] is not None and self.tecnicos[3] is not None:
            if not self.third_service() and self.tecnicos_especializados[1] is None:
                self.tecnicos_especializados[0] += 1
                self.tecnicos_especializados[1] = client
                self.ts1[0] += 1
                self.action_spectech(client, 1)
            else:
                # aumentar el tiempo de espera
                client.time += seller_action_time()
                self.cola.push(client)
        elif self.tecnicos[1] is None:
            self.tecnicos[0]+=1
            self.tecnicos[1] = client
            self.t1[0] += 1
            self.action_tech(client, 1)
        elif self.tecnicos[2] is None:
            self.tecnicos[0]+=1
            self.tecnicos[2] = client
            self.t2[0] += 1
            self.action_tech(client, 2)
        else:
            self.tecnicos[0]+=1
            self.tecnicos[3] = client
            self.t3[0] += 1
            self.action_tech(client, 3)

    def action_tech(self, client, worker):
        repair_time = repair_time_tech()
        
        client.time += repair_time
        client.worker = worker
        client.attended_by = "Tech"
        client.state = "Completed"
        self.cola.push(client)
    
    def attend_spectech(self, client):
        if self.tecnicos_especializados[1] is None:
            self.tecnicos_especializados[0] += 1
            self.tecnicos_especializados[1] = client
            self.ts1[0] += 1
            self.action_spectech(client, 1)
        else:
            # aumentar el tiempo de espera
            client.time += seller_action_time()
            self.cola.push(client)
    
    def action_spectech(self, client, worker):
        repair_time = repair_time_spec()
        
        client.time += repair_time
        client.worker = worker
        client.attended_by = "Spec Tech"
        client.state = "Completed"
        self.cola.push(client)
    
    def check(self, client):
        client.exit_time = client.time
        self.exits.append(client.time)
        self.client_count += 1
        att = client.attended_by
        worker = client.worker
        if att == "Seller":
            if worker == 1:
                self.v1.append((client.arrival_time, client.exit_time))
            else:
                self.v2.append((client.arrival_time, client.exit_time))
        elif att == "Tech":
            if worker == 1:
                self.t1.append((client.arrival_time, client.exit_time))
            elif worker == 2:
                self.t2.append((client.arrival_time, client.exit_time))
            else:
                self.t2.append((client.arrival_time, client.exit_time))
        else:
            self.ts1.append((client.arrival_time, client.exit_time))
    
    def handler(self):
        try:
            client = self.cola.pop()
        except Exception as e:
            print(e)
        if client.state == "Seller":
            self.time = client.time
            self.attend_seller(client)
            self.next_client = self.generate_new_client()
        elif client.state == "Tech":
            self.time = client.time
            self.attend_tech(client)
        elif client.state == "Spec Tech":
            self.time = client.time
            self.attend_spectech(client)
        elif client.state == "Completed":
            if not self.cola.empty():
                temp = self.cola.pop()
                self.time = min(temp.time, client.time)
                self.cola.push(temp)
            else:
                self.time = client.time
            if client.attended_by == "Seller":
                self.vendedores[0] -= 1
                self.vendedores[client.worker] = None
            elif client.attended_by == "Tech":
                self.tecnicos[0] -= 1
                self.tecnicos[client.worker] = None
            else:
                self.tecnicos_especializados[0] -= 1
                self.tecnicos_especializados[1] = None
                self.third_s = False
                
            self.check(client)
            if client.service == 2:
                self.profit += 350
            if client.service == 3:
                self.profit += 500
            if client.service == 4:
                self.profit += 750
    def main(self):
        self.generate_new_client()
        while self.time < self.duration and not self.cola.empty():
            self.handler()
        while not self.cola.empty():
            self.handler()
        
        return self.arrivals, self.exits, self.time, self.profit, self.client_count, self.v1, self.v2, self.t1, self.t2, self.t3, self.ts1