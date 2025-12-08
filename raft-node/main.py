from cluster_config import get_addresses, parse_args
from reservation_manager import ReservationManager
from console import run_console, seat_map_changed


def main():
    args = parse_args()
    selfAddr, partners = get_addresses(args)

    if args.prod:  # Launch in production mode
        node = ReservationManager(selfAddr, partners, seat_map_changed, diskJournal=True)
        run_console(node, args.id, mode='prod')

    else:  # Launch in demo mode
        initialShowTimes = {
            1: {
                "a1": None,
                "a2": None,
                "a3": None,
                "a4": None,
                "a5": None,
                "a6": None,
                "b1": None,
                "b2": None,
                "b3": None,
                "b4": None,
                "b5": None,
                "b6": None,
                "c1": None,
                "c2": None,
                "c3": None,
                "c4": None,
                "c5": None,
                "c6": None,
                "d1": None,
                "d2": None,
                "d3": None,
                "d4": None,
                "d5": None,
                "d6": None,
            }
        }
        node = ReservationManager(
            selfAddr, partners, seat_map_changed, initialShowTimes
        )
        run_console(node, args.id, mode='demo')


if __name__ == "__main__":
    main()
