from cluster_config import get_addresses
from reservation_manager import ReservationManager
from console import run_console


def main():
    selfAddr, partners = get_addresses()
    node = ReservationManager(selfAddr, partners)

    run_console(node)


if __name__ == "__main__":
    main()
