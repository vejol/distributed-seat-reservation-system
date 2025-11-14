import type { Seat, SeatStatus } from "../types"
import Screen from "./Screen"
import SeatInformation from "./SeatInformation"

interface Props {
  rows: string[]
  seats: Seat[]
  toggleSeat: (seatId: string) => void
}

const SeatSelection = ({ seats, toggleSeat, rows }: Props) => {
  const getSeatColor = (status: SeatStatus) => {
    switch (status) {
      case "available":
        return "bg-indigo-400 hover:bg-indigo-300 active:bg-indigo-500 cursor-pointer"
      case "selected":
        return "bg-green-500 hover:bg-green-400 active:bg-green-600 cursor-pointer"
      case "booked":
        return "bg-slate-400 cursor-not-allowed"
      default:
        return "bg-slate-300"
    }
  }
  return (
    <section className="lg:col-span-2 bg-white rounded-lg shadow-lg p-6">
      <Screen />

      {/* Seats Grid */}
      <div className="space-y-3 mb-8">
        {rows.map((row) => (
          <div key={row} className="flex items-center justify-center space-x-4">
            <span className="w-6 text-center font-semibold bg-slate-600 rounded-full text-white">
              {row}
            </span>
            <div className="flex gap-2">
              {seats
                .filter((seat) => seat.row === row)
                .map((seat) => (
                  <button
                    key={seat.id}
                    onClick={() => toggleSeat(seat.id)}
                    disabled={seat.status === "booked"}
                    className={`w-8 h-8 rounded-t-lg transition-colors ${getSeatColor(
                      seat.status
                    )}`}
                    title={`${seat.id} - ${seat.status}`}
                  />
                ))}
            </div>
            <span className="w-6 text-center font-semibold bg-slate-600 rounded-full text-white">
              {row}
            </span>
          </div>
        ))}
      </div>

      <SeatInformation />
    </section>
  )
}

export default SeatSelection
