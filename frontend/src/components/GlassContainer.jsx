import './GlassContainer.css';

const GlassContainer = ({ children, className = '', style = {} }) => {
  return (
    <div className={`glass-container ${className}`} style={style}>
      {children}
    </div>
  );
};

export default GlassContainer;
