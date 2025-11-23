import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import "./index.css"
import App from "./App.tsx"
import { BrowserRouter, Route, Routes } from "react-router"
import Seats from "./pages/seats.tsx"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"
import SingleMovie from "./pages/movies/single.tsx"
import Movies from "./pages/movies/index.tsx"
import Showtimes from "./pages/showtimes.tsx"

const queryClient = new QueryClient()

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <ReactQueryDevtools initialIsOpen={false} />
      <BrowserRouter>
        <Routes>
          <Route index element={<App />} />
          <Route path="showtimes" element={<Showtimes />} />
          <Route path="movies">
            <Route index element={<Movies />} />
            <Route path=":movies/seats" element={<Seats />} />
            <Route path=":movies" element={<SingleMovie />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>
)
