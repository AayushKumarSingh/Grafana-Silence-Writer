import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Login";
import CreateSilence from "./CreateSilence";
import History from "./History";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/create" element={<CreateSilence />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  );
}
