import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import PaperDetailPage from "./components/PaperDetailPage";
import SearchPage from "./components/SearchPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/papers/:paperId" element={<PaperDetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;