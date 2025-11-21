import { useQuery } from "@tanstack/react-query"
import { useParams } from "react-router"

interface GetShowtimeResponse {
  id: string
  movieId: string
  theater: {
    id: string
    name: string
    location: string[]
    seats: {
      rows: { row: string; seats: number }[]
    }
  }
  reservedSeats: Record<string, { paid: boolean; ttl: Date }>
  movie: {
    id: number
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
  price: number
  time: string
  theaterId: string
}

export const useGetShowtimeByParamId = () => {
  const { movies: movieId } = useParams<{ movies: string }>()
  const query = useQuery<GetShowtimeResponse>({
    queryKey: ["showtimes", movieId],
    queryFn: () => fetch(`/api/showtimes/${movieId}`).then((res) => res.json()),
  })
  return query
}
