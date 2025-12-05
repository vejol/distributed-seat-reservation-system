from cluster_config import get_addresses, get_selfId
from reservation_manager import ReservationManager
from console import run_console, seat_map_changed


def main():
    selfAddr, partners = get_addresses()
    node = ReservationManager(selfAddr, partners, seat_map_changed)

    selfId = get_selfId()
    run_console(node, selfId)


if __name__ == "__main__":
    main()
