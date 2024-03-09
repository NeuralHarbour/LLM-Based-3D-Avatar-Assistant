import React, { useEffect } from 'react';
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import background from '../Assets/IMG1.png';
import './productshow.css';

const Prouductshow = () => {
    useEffect(() => {

        const contentHolderHeight = document.querySelector(".content-holder").offsetHeight;
        const imgHolderHeight = window.innerHeight;
        const additionalScrollHeight = window.innerHeight;

        const totalBodyHeight = contentHolderHeight + imgHolderHeight + additionalScrollHeight;

        document.body.style.height = `${totalBodyHeight}px`;

        ScrollTrigger.create({
            trigger: ".website-content",
            start: "-0.1% top",
            onEnter: () => {
                gsap.set(".website-content", { position: 'absolute', top: '195%' });
            },
            onLeaveBack: () => {
                gsap.set(".website-content", { position: 'sticky', top: '0' });
            }
        });

        gsap.to(".header .letters:first-child", {
            x: () => -window.innerWidth * 3,
            scale: 10,
            ease: "power2.inOut",
            scrollTrigger: {
                start: "140% top",
                end: "+=100",
                scrub: 1
            }
        });
        gsap.to(".header .letters:last-child", {
            x: () => -window.innerWidth * 3,
            scale: 10,
            ease: "power2.inOut",
            scrollTrigger: {
                start: "140% top",
                end: "+=100",
                scrub: 1
            }
        });
    }, []);

    return (
        <div className='bx'>
            <div className='header'>
                <div className='letters'>
                    <div>P</div>
                    <div>R</div>
                    <div>O</div>
                    <div>D</div>
                </div>
                <div className='letters'>
                    <div>U</div>
                    <div>C</div>
                    <div>T</div>
                    <div>S</div>
                </div>
            </div>
            <div className="website-content">
                <div className="img-holder">
                    <img src={background} alt="" />
                </div>
                <div className="content-holder">
                    <div className="row">
                        <h1>Products</h1>
                    </div>
                    <div className="row">
                        <div className='img-prod'>
                            <img src="https://placehold.co/600x400" alt="" />
                        </div>
                    </div>
                    <div className="row">
                        <div className='img-prod'>
                            <img src="https://placehold.co/600x400" alt="" />
                        </div>
                    </div>
                    <div className="row">
                        <div className='img-prod'>
                            <img src="https://placehold.co/600x400" alt="" />
                        </div>
                    </div>
                    <div className="row">
                        <p>Lorem Ipsum Dolor Sit Amet</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Prouductshow;
