import { useState, useEffect } from 'react';
import { getAircraftImages, getAircraftImage } from '../api/client';
import GlassContainer from '../components/GlassContainer';
import ImageModal from '../components/ImageModal';
import './Jets.css';

const Jets = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [modalLoading, setModalLoading] = useState(false);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        setLoading(true);
        const data = await getAircraftImages();
        setImages(data.images);
        setError(null);
      } catch (err) {
        setError('Failed to load aircraft images. Please try again later.');
        console.error('Error fetching images:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, []);

  const handleImageClick = async (image, index) => {
    try {
      setModalLoading(true);
      setSelectedIndex(index);
      const imageDetail = await getAircraftImage(image.object_name);
      setSelectedImage(imageDetail);
    } catch (err) {
      console.error('Error fetching image details:', err);
      // Fallback to using the image from the list
      setSelectedImage(image);
    } finally {
      setModalLoading(false);
    }
  };

  const handleCloseModal = () => {
    setSelectedImage(null);
    setSelectedIndex(-1);
  };

  const handleNextImage = async () => {
    if (selectedIndex < images.length - 1) {
      const nextIndex = selectedIndex + 1;
      await handleImageClick(images[nextIndex], nextIndex);
    }
  };

  const handlePreviousImage = async () => {
    if (selectedIndex > 0) {
      const prevIndex = selectedIndex - 1;
      await handleImageClick(images[prevIndex], prevIndex);
    }
  };

  // Convert internal Docker URL to localhost for browser access
  const getPublicUrl = (url) => {
    return url.replace('http://storage:9000', 'http://localhost:9000');
  };

  if (loading) {
    return (
      <div className="jets-page">
        <div className="loading-container">
          <GlassContainer>
            <div className="loading-spinner"></div>
            <p className="loading-text">Loading aircraft images...</p>
          </GlassContainer>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="jets-page">
        <div className="error-container">
          <GlassContainer>
            <div className="error-icon">⚠️</div>
            <p className="error-text">{error}</p>
          </GlassContainer>
        </div>
      </div>
    );
  }

  return (
    <div className="jets-page">
      <div className="jets-header">
        <GlassContainer className="header-container">
          <h1 className="jets-title">Aircraft Gallery</h1>
          <p className="jets-count">{images.length} Images</p>
        </GlassContainer>
      </div>

      <div className="jets-grid">
        {images.map((image, index) => (
          <div
            key={image.object_name}
            className="jet-card"
            style={{ animationDelay: `${index * 0.05}s` }}
            onClick={() => handleImageClick(image, index)}
          >
            <GlassContainer className="jet-card-inner">
              <div className="jet-image-wrapper">
                <img
                  src={getPublicUrl(image.public_url)}
                  alt={image.object_name}
                  className="jet-image"
                  loading="lazy"
                />
                <div className="jet-overlay">
                  <svg className="zoom-icon" fill="white" viewBox="0 0 24 24" width="32" height="32">
                    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                  </svg>
                </div>
              </div>
              <div className="jet-info">
                <h3 className="jet-name">{image.object_name}</h3>
                <p className="jet-size">{(image.size / 1024).toFixed(1)} KB</p>
              </div>
            </GlassContainer>
          </div>
        ))}
      </div>

      {selectedImage && !modalLoading && (
        <ImageModal
          image={selectedImage}
          onClose={handleCloseModal}
          onNext={handleNextImage}
          onPrevious={handlePreviousImage}
          hasNext={selectedIndex < images.length - 1}
          hasPrevious={selectedIndex > 0}
        />
      )}

      {modalLoading && (
        <div className="modal-overlay">
          <div className="loading-spinner"></div>
        </div>
      )}
    </div>
  );
};

export default Jets;
