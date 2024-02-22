import React from 'react';
import Header from '../Navbar/Header';
import './Landing.css';
import '../About/about'
import gsap from 'gsap'

function Lander() {
    return (
        <section>
            <div className="VWA">
                <div className='main'>
                    <div className="box1">

                    </div>
                    <div className='box2'>
                        <div className="Text">
                            UNLOCKING<br />THE POTENTIAL
                        </div>
                    </div>
                    <div className='custom-nav'>
                        <div className='container'>
                            <Header />
                        </div>
                    </div>
                    <div className='box3'>
                        <div className="PlaceHolder">
                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                Cras efficitur dui quis lectus faucibus lacinia non ut lacus.
                                Aenean ipsum diam, dapibus at tortor eget, tincidunt elementum lacus.
                                Etiam libero ex, mattis sed felis nec, varius tincidunt nisl.
                                Aliquam tincidunt justo eu magna ullamcorper consectetur.</p>
                        </div>
                    </div>
                    <div className='box4'>
                        <button className='Button'>Get Started</button>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Lander;
