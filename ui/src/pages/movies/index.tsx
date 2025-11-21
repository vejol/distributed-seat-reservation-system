import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router"

type GetMoviesResponse = Array<{
  id: string
  title: string
  director: string
  duration: number
  genre: string[]
  cast: string[]
  language: string[]
  advisory: {
    ageLimit: number
    content: string[]
  }
}>

const Movies = () => {
  const { data } = useQuery<GetMoviesResponse>({
    queryKey: ["movies"],
    queryFn: () => fetch("/api/movies").then((res) => res.json()),
  })

  return (
    <main>
      <h1 className="text-3xl font-bold mb-8">Movies</h1>
      <ul className="space-y-4">
        {data?.map((movie) => (
          <li key={movie.id} className="p-4 border border-slate-300 rounded-lg">
            <Link to={`/movies/${movie.id}`}>
              <h2 className="text-2xl font-semibold">{movie.title}</h2>
              <p className="text-slate-700">Director: {movie.director}</p>
              <p className="text-slate-700">
                Duration: {movie.duration} minutes
              </p>
              <p className="text-slate-700">Genre: {movie.genre.join(", ")}</p>
              <p className="text-slate-700">Cast: {movie.cast.join(", ")}</p>
              <p className="text-slate-700">
                Language: {movie.language.join(", ")}
              </p>
              <p className="text-slate-700">
                Advisory: {movie.advisory.ageLimit}+ (
                {movie.advisory.content.join(", ")})
              </p>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  )
}

export default Movies
