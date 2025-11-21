import Header from "../components/Header"
import SeatSelection from "../components/SeatSelection"
import BookingSummary from "../components/BookingSummary"

function Seats() {
  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4">
      <main className="max-w-7xl mx-auto">
        <Header />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <SeatSelection />
          <BookingSummary />
        </div>
      </main>
    </div>
  )
}
export default Seats
