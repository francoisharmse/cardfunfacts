import { useState, useEffect } from 'react';
import './Background.css';

const Background = ({ imageUrl }) => {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    setLoaded(false);
    const img = new Image();
    img.src = imageUrl;
    img.onload = () => setLoaded(true);
  }, [imageUrl]);

  return (
    <>
      <div className={`background ${loaded ? 'loaded' : ''}`}>
        <img src={imageUrl} alt="Background" />
      </div>
      <div className="background-overlay" />
    </>
  );
};

export default Background;
