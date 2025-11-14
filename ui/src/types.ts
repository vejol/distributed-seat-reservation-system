export type SeatStatus = "available" | "selected" | "booked"

export interface Seat {
  id: string
  row: string
  number: number
  status: SeatStatus
  price?: number
}