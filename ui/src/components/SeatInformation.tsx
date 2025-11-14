const SeatInformation = () => {
  return (
    <div className="border-t pt-6">
      <h3 className="font-semibold text-slate-800 mb-4">Seat information</h3>
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
  )
}

export default SeatInformation
