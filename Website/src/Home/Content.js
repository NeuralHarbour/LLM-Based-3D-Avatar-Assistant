import React from 'react';
import text from '../Assets/text.png';
import { Link } from 'react-router-dom';
import './content.css';

function Content() {
  return (
    <main id = "Home" className="main">
      <div className="Bg">
        <div className="ImageWrapper">
          <img src={text} alt="Text" className="Image" />   
            <p className='In-Text'>EpsilonAI Co., Ltd. is a visionary venture company dedicated to the concept of "Live with Characters." The mission is to create a world where individuals can experience the joy of living alongside their favorite characters.</p>
            <button className="button-56"><Link to = "/Register">Get Started</Link></button>
        </div>
      </div>
    </main>
  );
}

export default Content;
