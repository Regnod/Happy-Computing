from workshop import Workshop

def test(workshop):
    arrivals, exits, time, profit, client_count, v1, v2, t1, t2, t3, ts1 = workshop.main()
    return arrivals, exits, time, profit, client_count, v1, v2, t1, t2, t3, ts1
    # print(f"Tiempo total de simulacion: {time}")
    print(f"Ganancia Total: {profit}")
    # print(f"Cantidad de Clientes: {client_count}")
    # print(f"Cantidad de CLientes repartidos por el vendedor 1: {v1}")
    # print(f"Cantidad de Clientes repartidos por el vendedor 2: {v2}")
    # print(f"Cantidad de Clientes atendidos por el tecnico 1: {t1}")
    # print(f"Cantidad de Clientes atendidos por el tecnico 2: {t2}")
    # print(f"Cantidad de Clientes atendidos por el tecnico 3: {t3}")
    # print(f"Cantidad de Clientes atendidos por el tecnico especializado: {ts1}")

def beginSampling():
    # d = 45
    n = 0
    # stats = [0 for _ in range(3)]
    time = 0
    profit = 0
    count = 0
    while n < 1000:
        Taller = Workshop()
        arrivals, exits, _time, _profit, _n, v1, v2, t1, t2, t3, ts1 = test(Taller)
        time+=_time
        count += _n
        n += 1
        profit+= _profit
    print(time/  1000)
    print(count/ 1000)
    print(profit/1000)
beginSampling()

# workshop = Workshop()
# test(workshop)