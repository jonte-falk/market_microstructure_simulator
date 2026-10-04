from agents import NoiseTrader, MarketMaker
from simulation import Simulation


def main():

    agents = [
        NoiseTrader(1),
        NoiseTrader(2),
        NoiseTrader(3),
        NoiseTrader(4),
        MarketMaker(5)
    ]

    simulation = Simulation(agents)

    simulation.run()

    for snapshot in simulation.statistics.snapshots:
        print(snapshot)

    simulation.statistics.plot_mid_price(show=True)


if __name__ == "__main__":
    main()