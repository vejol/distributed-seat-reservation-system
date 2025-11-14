const Header = () => {
  return (
    <header className="flex justify-between mb-8">
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
    </header>
  )
}

export default Header
