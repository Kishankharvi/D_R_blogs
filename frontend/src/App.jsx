import "./App.css";
import { Route, Routes, BrowserRouter } from "react-router-dom";
import Index from "./views/core/Index.jsx";
import MainWrapper from "../src/layouts/MainWrapper";
function App() {
  return (
    <>
      <BrowserRouter>
        <MainWrapper>
          <Routes>
            <Route path="/" element={<Index />} />
            {/* <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} /> */}
          </Routes>
        </MainWrapper>
      </BrowserRouter>
    </>
  );
}

export default App;
