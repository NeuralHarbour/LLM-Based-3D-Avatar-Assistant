import React, { useEffect } from 'react';
import './Services.scss';
import { Title, Service } from '../Title';
import holographyImage from '../Assets/Holography.png';
import AIMLImage from '../Assets/AIML.png';
import Robotics from '../Assets/Robotics.png';
import Webdev from '../Assets/WebDev.png';
import Cloud from '../Assets/Cloud.jpg';
import ARVR from '../Assets/ARVR.jpg';

const Services = () => {
    return (
        <body className="Service">
            <Title value="services" />
            <Service value="we provide" />
            <section class="intro"></section>
            <div class="cards">
                <div class="card card-1">
                    <div class="card-inner">
                        <h2 className="service-text">Holographic Displays and Assistants</h2>
                        <span class="hover-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            In efficitur dignissim orci, et faucibus erat tincidunt ac.
                            Pellentesque id arcu eleifend massa interdum convallis at a ex.
                            Suspendisse id lacus ac tellus luctus porttitor.</span>
                        <div class="mockup">
                            <img src={holographyImage} alt="Holography" className='mockup-img' />
                        </div>
                    </div>
                </div>
                <div class="card card-2">
                    <div class="card-inner">
                        <h2 className="service-text">AI/ML Solutions</h2>
                        <span class="hover-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            In efficitur dignissim orci, et faucibus erat tincidunt ac.
                            Pellentesque id arcu eleifend massa interdum convallis at a ex.
                            Suspendisse id lacus ac tellus luctus porttitor.</span>
                        <div class="mockup">
                            <img src={AIMLImage} alt="Holography" className='mockup-img' />
                        </div>
                    </div>
                </div>
                <div class="card card-3">
                    <div class="card-inner">
                        <h2 className="service-text">Robotics</h2>
                        <span class="hover-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            In efficitur dignissim orci, et faucibus erat tincidunt ac.
                            Pellentesque id arcu eleifend massa interdum convallis at a ex.
                            Suspendisse id lacus ac tellus luctus porttitor.</span>
                        <div class="mockup">
                            <div class="mockup">
                                <img src={Robotics} alt="Holography" className='mockup-img2' />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card card-4">
                    <div class="card-inner">
                        <h2 className="service-text">Web Development Services</h2>
                        <span class="hover-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            In efficitur dignissim orci, et faucibus erat tincidunt ac.
                            Pellentesque id arcu eleifend massa interdum convallis at a ex.
                            Suspendisse id lacus ac tellus luctus porttitor.</span>
                        <div class="mockup">
                            <img src={Webdev} alt="Holography" className='mockup-img' />
                        </div>
                    </div>
                </div>
                <div class="card card-5">
                    <div class="card-inner">
                        <h2 className="service-text">Cloud Services</h2>
                        <span class="hover-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            In efficitur dignissim orci, et faucibus erat tincidunt ac.
                            Pellentesque id arcu eleifend massa interdum convallis at a ex.
                            Suspendisse id lacus ac tellus luctus porttitor.</span>
                        <div class="mockup">
                            <img src={Cloud} alt="Holography" className='mockup-img' />
                        </div>
                    </div>
                </div>
                <div class="card card-6">
                    <div class="card-inner">
                        <h2 className="service-text">AR/VR/XR/MR Solutions</h2>
                        <span class="hover-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            In efficitur dignissim orci, et faucibus erat tincidunt ac.
                            Pellentesque id arcu eleifend massa interdum convallis at a ex.
                            Suspendisse id lacus ac tellus luctus porttitor.</span>
                        <div class="mockup">
                            <img src={ARVR} alt="Holography" className='mockup-img' />
                        </div>
                    </div>
                </div>
            </div>
            <script src="srv.js"></script>
        </body>
    )
}

export default Services