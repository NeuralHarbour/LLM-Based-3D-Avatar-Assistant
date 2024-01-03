import React from 'react'
import { Link,useNavigate } from 'react-router-dom';
import './Login.css'
const Login = () => {

  const history = useNavigate();

  const handleGoBack = () => {
    history(-1);
  };
  return (
    <section className='bod'>
        <div onClick={handleGoBack} className="back-button responsive">
            <i className='fa-solid fa-arrow-left' />
        </div>
        <div className='contain'>
            <form action='#'>
                <div className='title'>
                    Login
                </div>
                <div className="input-box">
                    <input type = 'Text' placeholder='Username' required/>
                    <div className='underline'/>
                </div>
                <div className="input-box">
                    <input type = 'password' placeholder='Password' required/>
                    <div className='underline'/>
                </div>
                <div className="input-box button">
                    <Link to = "/Usrdashbrd"><input type = 'submit' value="Login"/></Link>
                </div>
            </form>
            <div className="option">
                or Login with any of the following
            </div>
            <div className="google">
                <Link to = '#'>
                    <i className = "fa-brands fa-google"></i>
                    Login with Google
                </Link>
            </div>
            <div className="facebook">
                <Link to = '#'>
                    <i className = "fab fa-facebook-f"></i>
                    Login with Facebook
                </Link>
            </div>
            <div className="crac">
                <Link to = "/Register">Don't Have An Account ?</Link>
            </div>
        </div>
    </section>
  )
}

export default Login