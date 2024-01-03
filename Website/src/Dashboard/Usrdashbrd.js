import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import logo from '../Assets/EpsilonAI.png';
import './dash.css';

const Usrdashbrd = () => {
  const [activeLink, setActiveLink] = useState(0);

  const handleLinkClick = (index) => {
    setActiveLink(index);
  };

  return (
    <section className='sec'>
      <div className="contan">
        <aside>
          <div className="top">
            <div className="logo">
              <img src={logo} alt = ''/>
            </div>
            <div className="close" id="close-btn">
              <span className='fa fa-times' />
            </div>
          </div>
          <div className="sidebar">
            <Link
              to="#"
              onClick={() => handleLinkClick(0)}
              className={activeLink === 0 ? 'active' : ''}
            >
              <span className='fa fa-home' />
              <h2>Dashboard</h2>
            </Link>
            <Link
              to="#"
              onClick={() => handleLinkClick(1)}
              className={activeLink === 1 ? 'active' : ''}
            >
              <span className='fa fa-user' />
              <h2>Manage Avatars</h2>
            </Link>
            <Link
              to="#"
              onClick={() => handleLinkClick(2)}
              className={activeLink === 2 ? 'active' : ''}
            >
              <span className='fa fa-running' />
              <h2>Skills</h2>
            </Link>
            <Link
              to="#"
              onClick={() => handleLinkClick(3)}
              className={activeLink === 3 ? 'active' : ''}
            >
              <span className='fa fa-mobile' />
              <h2>Linked Devices</h2>
            </Link>
            <Link
              to="#"
              onClick={() => handleLinkClick(4)}
              className={activeLink === 4 ? 'active' : ''}
            >
              <span className='fas fa-shopping-bag' />
              <h2>Your Orders</h2>
            </Link>
            <Link
              to="#"
              onClick={() => handleLinkClick(5)}
              className={activeLink === 5 ? 'active' : ''}
            >
              <span className='fa fa-wrench' />
              <h2>Settings</h2>
            </Link>
            <Link
              to="#"
              onClick={() => handleLinkClick(6)}
              className={activeLink === 6 ? 'active' : ''}
            >
              <span className='fa fa-exclamation-circle' />
              <h2>Report a problem</h2>
            </Link>
            <Link
              to="#"
              onClick={() => handleLinkClick(7)}
              className={activeLink === 7 ? 'active' : ''}
            >
              <span className='fa fa-plus' />
              <h2>Add device</h2>
            </Link>
            <Link to="#">
              <span className='fa fa-sign-out' />
              <h2>Logout</h2>
            </Link>
          </div>
        </aside>
        <main className='mein'>
          <h1 className='tx'>Dashboard</h1>
          <div className='insights'>


            <div className='avatars'>
              <span className='fa fa-user'/>
              <div className="middle">
                <div className="lef">
                  <h3>Avatars Added</h3>
                  <h1 className='tx'>2</h1>
                </div>
                <div className="progress">
                  <svg>
                    <circle cx = '38' cy='38' r='36'/>
                  </svg>
                  <div className='number'>
                    <p>5%</p>
                  </div>
                </div>
              </div>
              <small className='text-muted'>Last Updated at</small>
            </div>


            <div className='skills'>
              <span className='fa fa-running'/>
              <div className="middle">
                <div className="lef">
                  <h3>Skills Added</h3>
                  <h1 className='tx'>2</h1>
                </div>
                <div className="progress">
                  <svg>
                    <circle cx = '38' cy='38' r='36'/>
                  </svg>
                  <div className='number'>
                    <p>5%</p>
                  </div>
                </div>
              </div>
              <small className='text-muted'>Last Updated at</small>
            </div>

            <div className='devices'>
              <span className='fa fa-mobile'/>
              <div className="middle">
                <div className="lef">
                  <h3>Linked Devices</h3>
                  <h1 className='tx'>2</h1>
                </div>
                <div className="progress">
                  <svg>
                    <circle cx = '38' cy='38' r='36'/>
                  </svg>
                  <div className='number'>
                    <p>5%</p>
                  </div>
                </div>
              </div>
              <small className='text-muted'>Last Updated at</small>
            </div>
          </div>
          <div className="recent-order">
            <h2>Recent Orders</h2>
            <table>
              <thead>
                <tr>
                  <th>Product Name</th>
                  <th>Product No</th>
                  <th>Payment</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Lorem Ipsum</td>
                  <td>0</td>
                  <td>COD</td>
                  <td>Pending</td>
                  <td>Details</td>
                </tr>
                <tr>
                  <td>Lorem Ipsum</td>
                  <td>0</td>
                  <td>COD</td>
                  <td>Pending</td>
                  <td>Details</td>
                </tr>
                <tr>
                  <td>Lorem Ipsum</td>
                  <td>0</td>
                  <td>COD</td>
                  <td>Pending</td>
                  <td>Details</td>
                </tr>
                <tr>
                  <td>Lorem Ipsum</td>
                  <td>0</td>
                  <td>COD</td>
                  <td>Pending</td>
                  <td>Details</td>
                </tr>
              </tbody>
            </table>
            <Link to="#" className='ref'>Show All</Link>
          </div>
        </main>
        <div className="right">
          <div className="top">
            <button id = "menu-btn">
              <span className='fas fa-bars'/>
            </button>
            <div className="theme-toggler">
              <span className='fa fa-sun'/>
              <span className='fa fa-moon'/>
            </div>
            <div className="profile">
              <div className="info">
                <p>Hey, <b>ABC</b></p>
              </div>
              <div className='profile-photo'>
                <img src = 'https://img.freepik.com/free-vector/illustration-businessman_53876-5856.jpg?w=740&t=st=1691049849~exp=1691050449~hmac=24fbf4dbf9c89ff81dd8882c45884a954ce393a8b022761041164564aa013c2a' alt =''></img>
              </div>
            </div>
          </div>
          <div className="recent-updates">
            <h2>News</h2>
            <div className="updates">
              <div className="update">
                <div className='profile-photo'>
                  <img src = 'https://img.freepik.com/free-vector/illustration-user-avatar-icon_53876-5907.jpg?w=740&t=st=1691050160~exp=1691050760~hmac=aa466d7e93ede4aca809ce83453dcce0e500af3be6e53bf263ff487e5bbf4ef6' alt = ''/>
                </div>
                <div className='message'>
                  <p>Lorem Ipsum Dolor Sit Amet</p>
                  <small className='text-muted'>2 minutes ago</small>
                </div>
              </div>
              <div className="update">
                <div className='profile-photo'>
                  <img src = 'https://img.freepik.com/free-vector/illustration-user-avatar-icon_53876-5907.jpg?w=740&t=st=1691050160~exp=1691050760~hmac=aa466d7e93ede4aca809ce83453dcce0e500af3be6e53bf263ff487e5bbf4ef6' alt = ''/>
                </div>
                <div className='message'>
                  <p>Lorem Ipsum Dolor Sit Amet</p>
                  <small className='text-muted'>2 minutes ago</small>
                </div>
              </div>
              <div className="update">
                <div className='profile-photo'>
                  <img src = 'https://img.freepik.com/free-vector/illustration-user-avatar-icon_53876-5907.jpg?w=740&t=st=1691050160~exp=1691050760~hmac=aa466d7e93ede4aca809ce83453dcce0e500af3be6e53bf263ff487e5bbf4ef6' alt = ''/>
                </div>
                <div className='message'>
                  <p>Lorem Ipsum Dolor Sit Amet</p>
                  <small className='text-muted'>2 minutes ago</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Usrdashbrd;
