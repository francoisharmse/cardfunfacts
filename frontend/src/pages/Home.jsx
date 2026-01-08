import { useState } from 'react';
import GlassContainer from '../components/GlassContainer';
import { backgrounds, defaultBackground } from '../data/backgrounds';
import './Home.css';

const Home = ({ onBackgroundChange, currentBackground }) => {
  const [selectedBg, setSelectedBg] = useState(currentBackground || defaultBackground);

  const handleBackgroundChange = (e) => {
    const bg = backgrounds.find(b => b.id === e.target.value);
    setSelectedBg(bg);
    onBackgroundChange(bg);
  };

  return (
    <div className="home-page">
      <GlassContainer className="home-container">
        <div className="home-content">
          <h1 className="home-title">Welcome to Flash Facts</h1>
          <p className="home-description">
            Explore our collection of military aircraft and customize your viewing experience
          </p>

          <div className="background-selector">
            <label htmlFor="bg-select" className="selector-label">
              Choose Background
            </label>
            <select
              id="bg-select"
              value={selectedBg.id}
              onChange={handleBackgroundChange}
              className="bg-dropdown"
            >
              {backgrounds.map((bg) => (
                <option key={bg.id} value={bg.id}>
                  {bg.name}
                </option>
              ))}
            </select>
          </div>

          <div className="home-stats">
            <div className="stat-card glass">
              <div className="stat-number">24</div>
              <div className="stat-label">Aircraft Images</div>
            </div>
            <div className="stat-card glass">
              <div className="stat-number">8</div>
              <div className="stat-label">Backgrounds</div>
            </div>
          </div>
        </div>
      </GlassContainer>
    </div>
  );
};

export default Home;
