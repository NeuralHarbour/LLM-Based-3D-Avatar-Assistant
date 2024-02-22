import React from 'react'
import './Footer.css'
const Footer = () => {
  const today = new Date();
  return (
    <div className="footer">
      <div className="conta">
        <div className="col">
          <h1>Comapny</h1>
          <ul>
            <li>About</li>
            <li>Services</li>
            <li>Social</li>
            <li>Get in Touch</li>
          </ul>
        </div>
        <div className='col'>
          <h1>Products</h1>
          <ul>
            <li>About</li>
            <li>Services</li>
            <li>Social</li>
            <li>Get in Touch</li>
          </ul>
        </div>
        <div className="col">
          <h1>Resources</h1>
          <ul>
            <li>Webmail</li>
            <li>Redeem code</li>
            <li>WHOIS lookup</li>
            <li>Site map</li>
            <li>Web templates</li>
            <li>Email templates</li>
          </ul>
        </div>
        <div className="col">
          <h1>Support</h1>
          <ul>
            <li>Contact us</li>
            <li>Web chat</li>
            <li>Open ticket</li>
          </ul>
        </div>
        <div className="col social">
          <h1>Social</h1>
          <ul>
            <li>
              <a href="#!" role="button" style={{ color: '#3b5998' }}>
                <i className="fab fa-facebook-f fa-lg" style={{ width: '32px' }}></i>
              </a>
            </li>
            <li>
              <a href="#!" role="button" style={{ color: '#ac2bac' }}>
                <i className="fab fa-instagram fa-lg" style={{ width: '32px' }}></i>
              </a>
            </li>
            <li>
              <a href="#!" role="button" style={{ color: '#55acee' }}>
                <i className="fab fa-twitter fa-lg" style={{ width: '32px' }}></i>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Footer