import { useState } from "react"

type SeatStatus = "available" | "selected" | "booked"

interface Seat {
  id: string
  row: string
  number: number
  status: SeatStatus
  price?: number
}

function App() {
  const rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
  const seatsPerRow = 10

  // Initialize seats
  const [seats, setSeats] = useState<Seat[]>(() => {
    const initialSeats: Seat[] = []
    rows.forEach((row) => {
      for (let i = 1; i <= seatsPerRow; i++) {
        const isBooked = Math.random() < 0.1 // 10% chance seat is booked

        initialSeats.push({
          id: `${row}${i}`,
          row,
          number: i,
          status: isBooked ? "booked" : "available",
          price: 10,
        })
      }
    })
    return initialSeats
  })

  const toggleSeat = (seatId: string) => {
    setSeats((prevSeats) =>
      prevSeats.map((seat) => {
        if (seat.id === seatId && seat.status !== "booked") {
          return {
            ...seat,
            status: seat.status === "selected" ? "available" : "selected",
          }
        }
        return seat
      })
    )
  }

  const selectedSeats = seats.filter((seat) => seat.status === "selected")
  const totalPrice = selectedSeats.reduce(
    (sum, seat) => sum + (seat.price || 0),
    0
  )

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
    <div className="min-h-screen bg-slate-50 py-8 px-4">
      {/* Main Container */}
      <div className="max-w-7xl mx-auto">
        <section className="flex justify-between mb-8">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold">Seat reservation</h1>
            <p className="text-slate-800">Helsinki / Theater 2</p>
          </div>
          <div className="text-right space-y-2">
            <p className="text-slate-800">English, Finnish subtitles</p>
            <p className="text-slate-800">
              <span className="px-2 py-1 font-bold bg-slate-800 text-red-50 rounded-md mr-2">
                12+
              </span>
              Violence
            </p>
          </div>
        </section>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Seat Selection Card */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-lg p-6">
            {/* Screen */}
            <div className="mb-16">
              <div className="h-2 bg-linear-to-b from-slate-400 to-slate-300 rounded-t-full mb-2"></div>
              <p className="text-center text-slate-600 text-sm">SCREEN</p>
            </div>

            {/* Seats Grid */}
            <div className="space-y-3 mb-8">
              {rows.map((row) => (
                <div
                  key={row}
                  className="flex items-center justify-center space-x-4"
                >
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

            {/* Legend */}
            <div className="border-t pt-6">
              <h3 className="font-semibold text-slate-800 mb-4">
                Seat information
              </h3>
              <div className="flex flex-wrap gap-6">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 bg-indigo-400 rounded-t-lg"></div>
                  <span className="text-sm text-slate-700">Available</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 bg-green-500 rounded-t-lg"></div>
                  <span className="text-sm text-slate-700">Selected</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 bg-slate-400 rounded-t-lg"></div>
                  <span className="text-sm text-slate-700">Booked</span>
                </div>
              </div>
            </div>
          </div>

          {/* Booking Summary Card */}
          <div className="lg:col-span-1 bg-white rounded-lg shadow-lg p-6 h-fit space-y-8">
            <h2 className="text-xl font-bold text-slate-800">
              Booking Summary
            </h2>

            <div className="space-y-2">
              <p className="font-bold">Show</p>
              <p>Back to the future</p>
              <p className="text-slate-600">13.11.2025</p>
              <p className="text-slate-600">19.00 - 21.45</p>
            </div>

            <div className="space-y-2">
              <p className="font-bold">Seats</p>
              {selectedSeats.length === 0 ? (
                <p className="text-slate-400">No seats selected</p>
              ) : (
                <>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-800">
                      Total Seats: {selectedSeats.length}
                    </span>
                  </div>
                  <div>
                    <div className="space-y-2 divide-y divide-slate-200">
                      {selectedSeats.map((seat) => (
                        <div
                          key={seat.id}
                          className="flex justify-between items-center space-y-2"
                        >
                          <span className="text-slate-800">Seat {seat.id}</span>
                          <span className="text-slate-800">{seat.price} €</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>

            <div className="flex justify-between items-center">
              <span className="text-xl font-bold text-slate-800">Total:</span>
              <span className="text-xl font-bold text-indigo-500">
                {totalPrice} €
              </span>
            </div>

            <button className="w-full bg-black/90 hover:bg-black/80 active:bg-black active:scale-95 text-white font-semibold py-3 px-4 rounded-lg transition">
              Checkout
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
