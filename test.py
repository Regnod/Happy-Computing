from workshop import Workshop

def test(workshop):
    time, profit, client_count, v1, v2, t1, t2, t3, ts1 = workshop.main()
    
    print(f"Tiempo total de simulacion: {time}")
    print(f"Ganancia Total: {profit}")
    print(f"Cantidad de Clientes: {client_count}")
    print(f"Cantidad de CLientes repartidos por el vendedor 1: {v1}")
    print(f"Cantidad de Clientes repartidos por el vendedor 2: {v2}")
    print(f"Cantidad de Clientes atendidos por el tecnico 1: {t1}")
    print(f"Cantidad de Clientes atendidos por el tecnico 2: {t2}")
    print(f"Cantidad de Clientes atendidos por el tecnico 3: {t3}")
    print(f"Cantidad de Clientes atendidos por el tecnico especializado: {ts1}")

def beginSampling():
    # d = 45
    n = 0
    # stats = [0 for _ in range(3)]
    while n < 30:
        Taller = Workshop()
        test(Taller)
        n += 1
beginSampling()

# workshop = Workshop()
# test(workshop)