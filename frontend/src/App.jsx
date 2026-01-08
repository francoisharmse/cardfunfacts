import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Background from './components/Background';
import Sidebar from './components/Sidebar';
import HamburgerMenu from './components/HamburgerMenu';
import Home from './pages/Home';
import Jets from './pages/Jets';
import Sportscars from './pages/Sportscars';
import { defaultBackground } from './data/backgrounds';
import './App.css';

function App() {
  const [currentBackground, setCurrentBackground] = useState(defaultBackground);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <Router>
      <div className="app">
        <Background imageUrl={currentBackground.url} />
        <HamburgerMenu onClick={toggleSidebar} isOpen={sidebarOpen} />
        <Sidebar isOpen={sidebarOpen} onClose={closeSidebar} />
        <main className="main-content">
          <Routes>
            <Route
              path="/"
              element={
                <Home
                  onBackgroundChange={setCurrentBackground}
                  currentBackground={currentBackground}
                />
              }
            />
            <Route path="/jets" element={<Jets />} />
            <Route path="/sportscars" element={<Sportscars />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
