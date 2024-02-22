import React, { useState } from 'react';
import styled from "styled-components";
import logo from "../Assets/Logo.png";
import { GiHamburgerMenu } from "react-icons/gi";
import { MdClose } from "react-icons/md";
import { useScroll } from "../useScroll";
import { motion } from "framer-motion";
import { navAnimation } from "../Animation";

function Navbar() {
  const [isNavOpen, setIsNavOpen] = useState(false);
  const [element, controls] = useScroll();
  return <Nav ref={element}
    variants={navAnimation}
    transition={{ delay: 0.1 }}
    animate={controls}
    state={isNavOpen ? 1 : 0}
  >
    <div className="brand__container">
      <a href="#" className='brand'>
        <img src={logo} alt="logo" />
      </a>
      <div className="toggle">
        {isNavOpen ? (
          <MdClose onClick={() => setIsNavOpen(false)} />
        ) : (
          <GiHamburgerMenu
            onClick={(e) => {
              e.stopPropagation();
              setIsNavOpen(true);
            }}
          />
        )}
      </div>
    </div>
    <div className={`links ${isNavOpen ? "show" : ""}`}>
      <ul>
        <li className="active">
          <a href="#home">Home</a>
        </li>
        <li>
          <a href="#services">About</a>
        </li>
        <li>
          <a href="#portfolio">Products</a>
        </li>
        <li>
          <a href="#blog">Get Started</a>
        </li>
      </ul>
    </div>
  </Nav>
}

const Nav = styled(motion.nav)`
  display: flex;
  justify-content: space-between;
  margin: 0 2rem;
  color: #000;
  padding-top: 2rem;
  .brand__container {
    margin: 0 2rem;
    .toggle {
      display: none;
    }
  }
  .brand__container img {
    width: 250px; /* Adjust the width as needed */
    height: 60px; /* Maintain aspect ratio */
  }

  .links {
    ul {
      list-style-type: none;
      display: flex;
      gap: 3rem;
      .active{
        a {
          border-bottom: 0.2rem solid var(--secondary-color);
        }
      }
      li {
        a {
          color: #000;
          text-decoration: none;
          font-weight: 400;
          font-size: 0.7rem;
          text-transform: uppercase;
          padding-left: 0.3rem;
        }
      }
    }
  }
  @media screen and (min-width: 280px) and (max-width: 1080px) {
    margin: 0;
    position: relative;
    .brand__container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      .toggle {
        padding-right: 1rem;
        display: block;
        z-index: 1;
      }
    }
    .show {
      opacity: 1 !important;
      visibility: visible !important;
    }
    .links {
      position: absolute;
      overflow-x: hidden;
      top: 0;
      right: 0;
      width: ${({ state }) => (state ? "100%" : "0%")};
      height: 100vh;
      background-color: var(--secondary-color);
      opacity: 0;
      visibility: hidden;
      transition: 0.4s ease-in-out;
      ul {
        flex-direction: column;
        text-align: center;
        height: 100%;
        justify-content: center;
      }
    }
  }
`;

export default Navbar;