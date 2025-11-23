import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router"

type GetShowtimesResponse = Array<{
  id: string
  time: string
  price: number
  movieTitle?: string
  movieDuration?: number
  movieCast?: string[]
  movieGenre?: string[]
  theaterName?: string
  theaterLocation?: string
  availableSeats?: number
}>

const Showtimes = () => {
  const { data } = useQuery<GetShowtimesResponse>({
    queryKey: ["showtimes"],
    queryFn: () => fetch("/api/showtimes").then((res) => res.json()),
  })

  console.log(data)

  return (
    <main className="max-w-3xl mx-auto pt-16">
      <h1 className="text-3xl font-bold mb-8">Showtimes</h1>
      <ul className="space-x-4 grid grid-cols-1 md:grid-cols-2 gap-4 flex-wrap">
        {data?.map((showtime) => (
          <li
            key={showtime.id}
            className="p-4 border border-slate-300 rounded-lg aspect-square w-xs"
          >
            <Link
              to={`/movies/${showtime.id}/seats`}
              className="block space-y-2"
            >
              <h2 className="text-2xl font-semibold">{showtime.movieTitle}</h2>
              <p className="text-slate-700">
                Duration: {showtime.movieDuration} minutes
              </p>
              <p className="text-slate-700">
                Cast: {showtime.movieCast?.join(", ")}
              </p>
              <p>Theater: {showtime.theaterName}</p>
              <p>Time: {new Date(showtime.time).toLocaleString()}</p>
              <p>Price: ${showtime.price.toFixed(2)}</p>
              <p>Available Seats: {showtime.availableSeats}</p>
              <span className="text-indigo-600 hover:underline">
                Order seats &gt;&gt;
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  )
}

export default Showtimes
