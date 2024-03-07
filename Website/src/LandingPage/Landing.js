import React, { useEffect, useRef } from 'react';
import Header from '../Navbar/Header';
import './Landing.css';
import gsap from 'gsap';
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { LanderText1, LanderText2, LanderButton } from "../Animation";
import { useScroll } from "../useScroll";
import { motion } from "framer-motion";

function Lander() {
    const ref1 = useRef();
    const ref2 = useRef();
    const ref4 = useRef();

    const [element, controls] = useScroll();

    useEffect(() => {
        gsap.registerPlugin(ScrollTrigger);
        animateElement1(ref1.current);
        animateElement2(ref2.current);
        animateElement4(ref4.current);
    }, []);

    const animateElement1 = (element) => {
        gsap.fromTo(
            element,
            { x: 0, opacity: 1 }, // start position and opacity
            {
                x: -100, // end position (move to the left)
                opacity: 0, // end opacity (fade out)
                duration: 2,
                ease: "power2.inOut", // easing function
                scrollTrigger: {
                    trigger: element,
                    start: "top top", // start trigger when top of element hits top of viewport
                    end: "bottom top", // end trigger when bottom of element hits top of viewport
                    scrub: true, // smooth animation
                }
            }
        );
    };
    const animateElement2 = (element) => {
        gsap.fromTo(
            element,
            { x: 0, opacity: 1 },
            {
                x: 200,
                opacity: 0,
                duration: 2,
                ease: "power3.inOut",
                scrollTrigger: {
                    trigger: element,
                    start: "top center",
                    end: "bottom top",
                    scrub: true,
                }
            }
        );
    };
    const animateElement4 = (element) => {
        gsap.fromTo(
            element,
            { y: 0, opacity: 1 },
            {
                y: 100,
                opacity: 0,
                duration: 2,
                ease: "power2.inOut",
                scrollTrigger: {
                    trigger: element,
                    start: "top center",
                    end: "bottom top",
                    scrub: true,
                }
            }
        );
    };


    return (
        <section>
            <div className="VWA">
                <div className='main'>
                    <div className="box1">

                    </div>
                    <motion.div className='box2' ref={element}
                        variants={LanderText1}
                        transition={{ delay: 0.1 }}
                        animate={controls}>
                        <div className="Text" ref={ref1}>
                            UNLOCKING<br />THE POTENTIAL
                        </div>
                    </motion.div>
                    <div className='custom-nav'>
                        <div className='container'>
                            <Header />
                        </div>
                    </div>
                    <motion.div className='box3' ref={element}
                        variants={LanderText2}
                        transition={{ delay: 0.1 }}
                        animate={controls}>
                        <div className="PlaceHolder" ref={ref2}>
                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                Cras efficitur dui quis lectus faucibus lacinia non ut lacus.
                                Aenean ipsum diam, dapibus at tortor eget, tincidunt elementum lacus.
                                Etiam libero ex, mattis sed felis nec, varius tincidunt nisl.
                                Aliquam tincidunt justo eu magna ullamcorper consectetur.</p>
                        </div>
                    </motion.div>
                    <div className='box4' ref={ref4}>
                        <button className='Button'>Get Started</button>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Lander;
