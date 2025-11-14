import { useState } from "react"
import Header from "./components/Header"
import type { Seat } from "./types"
import SeatSelection from "./components/SeatSelection"
import BookingSummary from "./components/BookingSummary"

function App() {
  const rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
  const seatsPerRow = 10

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

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4">
      <main className="max-w-7xl mx-auto">
        <Header />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <SeatSelection seats={seats} rows={rows} toggleSeat={toggleSeat} />
          <BookingSummary seats={seats} />
        </div>
      </main>
    </div>
  )
}

export default App
