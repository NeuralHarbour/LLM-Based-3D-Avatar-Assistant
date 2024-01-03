import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import logo from '../Assets/EpsilonAI.png';
import './Navbar.css';

function Header() {
  const [clicked, setClicked] = useState(false);
  const handleClick = () => {
    setClicked(!clicked);
  };

  return (
    <nav>
      <img className="image" src={logo} alt="logo" />

      <div>
        <ul id="navbar" className={clicked ? '#navbar active' : '#navbar'}>
          <li>
            <Link to="/" className="active">
              Home
            </Link>
          </li>
          <li>
            <Link to="/news">News</Link>
          </li>
          <li>
            <Link to="/products">Products</Link>
          </li>
          <li>
            <a href='#Contact'>Contact</a>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
        </ul>
      </div>
      <div id="mobile" onClick={handleClick}>
        <i id="bar" className={clicked ? 'fas fa-times' : 'fas fa-bars'}></i>
      </div>
    </nav>
  );
}

export default Header;
