import { useQuery } from "@tanstack/react-query"
import { useParams } from "react-router"

interface GetMoviesResponse {
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
}

const SingleMovie = () => {
  const { movies: movieId } = useParams()
  const { data: movie } = useQuery<GetMoviesResponse>({
    queryKey: ["movies", movieId],
    queryFn: () => fetch(`/api/movies/${movieId}`).then((res) => res.json()),
  })

  if (!movie) {
    return <p>Loading...</p>
  }

  return (
    <main>
      <h1 className="text-3xl font-bold mb-8">Movies</h1>
      <article key={movie.id} className="p-4 max-w-sm">
        <h2 className="text-2xl font-semibold">{movie.title}</h2>
        <p className="text-slate-700">Director: {movie.director}</p>
        <p className="text-slate-700">Duration: {movie.duration} minutes</p>
        <p className="text-slate-700">Genre: {movie.genre.join(", ")}</p>
        <p className="text-slate-700">Cast: {movie.cast.join(", ")}</p>
        <p className="text-slate-700">Language: {movie.language.join(", ")}</p>
        <p className="text-slate-700">
          Advisory: {movie.advisory.ageLimit}+ (
          {movie.advisory.content.join(", ")})
        </p>
      </article>
    </main>
  )
}

export default SingleMovie
