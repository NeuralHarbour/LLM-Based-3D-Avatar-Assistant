import React from 'react'
import { Link,useNavigate } from 'react-router-dom';
import './Login.css'
const Register = () => {

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
                    SignUp
                </div>
                <div className="input-box">
                    <input type = 'Text' placeholder='Username' required/>
                    <div className='underline'/>
                </div>
                <div className="input-box">
                    <input type = 'Text' placeholder='Email-ID' required/>
                    <div className='underline'/>
                </div>
                <div className="input-box">
                    <input type = 'Text' placeholder='Phone No' required/>
                    <div className='underline'/>
                </div>
                <div className="input-box">
                    <input type = 'password' placeholder='Password' required/>
                    <div className='underline'/>
                </div>
                <div className="input-box button">
                    <input type = 'submit' value="SignUp"/>
                </div>
            </form>
            <div className="crac">
                <Link to = "/Login">Already Have An Account ?</Link>
            </div>
        </div>
    </section>
  )
}

export default Register