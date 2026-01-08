import './HamburgerMenu.css';

const HamburgerMenu = ({ onClick, isOpen }) => {
  return (
    <button
      className={`hamburger-menu ${isOpen ? 'open' : ''}`}
      onClick={onClick}
      aria-label="Toggle menu"
    >
      <span></span>
      <span></span>
      <span></span>
    </button>
  );
};

export default HamburgerMenu;
