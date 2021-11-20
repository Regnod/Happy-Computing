import typer

from workshop import Workshop

def simulate():
    workshop = Workshop()
    workshop.main()
    return workshop


def main():
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo("En esta simulación tenemos 2 vendedores, 3 técnicos y 1 técnicos especializado.")
    typer.echo("Cada simulación representa una jornada laboral de 8 horas")
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    number_simulation = int(
        typer.prompt("Cuantas veces quiere ejecutar la simulación?")
    )
    promedio_profits = 0
    promedio_time = 0
    promedio_clients = 0
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    with typer.progressbar(range(number_simulation)) as simulations:
        for _ in simulations:
            workshop = simulate()
            promedio_time += workshop.time
            promedio_profits += workshop.profit
            promedio_clients += workshop.client_count

    promedio_time /= number_simulation
    promedio_profits /= number_simulation
    promedio_clients /= number_simulation

    promedio_time = round(promedio_time, 3)
    promedio_profits = round(promedio_profits, 3)
    promedio_clients = round(promedio_clients,3)

    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style("Tiempo promedio:", fg=typer.colors.BRIGHT_GREEN)
        + f" {promedio_time} minutos"
    )
    typer.echo(
        typer.style("Promedio de profit: ", fg=typer.colors.BRIGHT_GREEN)
        + f" {promedio_profits}$"
    )

    typer.echo(
        typer.style("Número de clientes promedio: ", fg=typer.colors.BRIGHT_GREEN)
        + f" {promedio_clients}"
    )


if __name__ == "__main__":
    typer.run(main)