import { useGetShowtimeByParamId } from "../api/movies"

const Header = () => {
  const { data: showtimes } = useGetShowtimeByParamId()

  return (
    <header className="flex justify-between mb-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Seat reservation</h1>
        <p className="text-slate-800">
          {showtimes?.theater?.location[0]} / {showtimes?.theater?.name}
        </p>
      </div>
      <div className="text-right space-y-2">
        <p className="text-slate-800">
          {showtimes?.movie?.language.join(", ")}
        </p>
        <p className="text-slate-800">
          <span className="px-2 py-1 font-bold bg-slate-800 text-red-50 rounded-md mr-2">
            {showtimes?.movie?.advisory.ageLimit}+
          </span>
          {showtimes?.movie?.advisory.content.join(", ")}
        </p>
      </div>
    </header>
  )
}

export default Header
