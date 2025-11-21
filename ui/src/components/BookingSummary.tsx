import { useGetShowtimeByParamId } from "../api/movies"

const BookingSummary = () => {
  const { data: showtimes } = useGetShowtimeByParamId()
  const price = showtimes?.price ?? 0

  // @todo: Apply selected seats from state management
  const selectedSeats: Array<{ id: string; price: number }> = []

  return (
    <section className="lg:col-span-1 bg-white rounded-lg shadow-lg p-6 h-fit space-y-8">
      <h2 className="text-xl font-bold text-slate-800">Booking Summary</h2>

      <div className="space-y-2">
        <p className="font-bold">Show</p>
        <p>{showtimes?.movie?.title}</p>
        <p className="text-slate-600">
          {new Date(showtimes?.time ?? "").toLocaleDateString("fi-FI")}
        </p>
        <p className="text-slate-600">
          {new Date(showtimes?.time ?? "").toLocaleTimeString("fi-FI", {
            hour: "2-digit",
            minute: "2-digit",
          })}
          {` - `}
          {new Date(
            new Date(showtimes?.time ?? "").getTime() +
              (showtimes?.movie?.duration ?? 0) * 60000
          ).toLocaleTimeString("fi-FI", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
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
          {selectedSeats.length * price} €
        </span>
      </div>

      <button className="w-full bg-black/90 hover:bg-black/80 active:bg-black active:scale-95 text-white font-semibold py-3 px-4 rounded-lg transition">
        Checkout
      </button>
    </section>
  )
}

export default BookingSummary
