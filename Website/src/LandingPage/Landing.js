import React, { useEffect, useRef } from 'react';
import Header from '../Navbar/Header';
import './Landing.css';
import gsap from 'gsap';
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { LanderText1, LanderText2, LanderButton, AboutImgAnim, AboutTextAnim, AnimefyImgAnim, AnimefyTextAnim } from "../Animation";
import { useScroll } from "../useScroll";
import { motion } from "framer-motion";
import background from '../Assets/IMG1.png';
gsap.registerPlugin(ScrollTrigger);
function Lander() {
    const ref1 = useRef();
    const ref2 = useRef();
    const ref4 = useRef();
    const containerRef = useRef();

    const [element, controls] = useScroll();
    const [element1, controls1] = useScroll();
    const [element2, controls2] = useScroll();

    useEffect(() => {

        const ctx = gsap.context(() => {
            const section1 = document.getElementById('section1');
            const section2 = document.getElementById('section2');
            const horizontalSections = [section1, section2];

            gsap.to(horizontalSections, {
                xPercent: -100 * (horizontalSections.length - 1),
                ease: "circ.inOut",
                scrollTrigger: {
                    trigger: containerRef.current,
                    pin: true,
                    scrub: 1,
                    snap: 1 / (horizontalSections.length - 1),
                    end: () => "+=" + containerRef.current.offsetWidth
                }
            });
        });

        return () => ctx.revert();
    }, []);
    useEffect(() => {
        animateElement1(ref1.current);
        animateElement2(ref2.current);
        animateElement4(ref4.current);

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
                start: "145% bottom",
                end: "+=40",
                scrub: 1
            }
        });
        gsap.to(".header .letters:last-child", {
            x: () => window.innerWidth * 3,
            scale: 10,
            ease: "power2.inOut",
            scrollTrigger: {
                start: "145% bottom",
                end: "+=40",
                scrub: 1
            }
        });

        gsap.to(".img-holder", {
            rotation: 0,
            clipPath: 'polygon(0% 0%,100% 0%, 100% 100%,0% 100%)',
            ease: "power2.inOut",
            scrollTrigger: {
                start: "145% bottom",
                end: `+=40`,
                scrub: 1
            }
        })
        gsap.to(".img-holder img", {
            scale: 1,
            ease: "power2.inOut",
            scrollTrigger: {
                start: "145% bottom",
                end: `+=40`,
                scrub: 1
            }
        })
    }, []);

    const animateElement1 = (element) => {
        gsap.fromTo(
            element,
            { x: 0, opacity: 1 },
            {
                x: -100,
                opacity: 0,
                duration: 2,
                ease: "power2.inOut",
                scrollTrigger: {
                    trigger: element,
                    start: "top top",
                    end: "bottom top",
                    scrub: true,
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
        <>
            <section className=''>
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
            <main id="container" ref={containerRef}>
                <section id="section1" className='about'>
                    <motion.div className="image" ref={element1}
                        variants={AboutImgAnim}
                        transition={{ delay: 0.1 }}
                        animate={controls1}></motion.div>
                    <motion.div className="content" ref={element1}
                        variants={AboutTextAnim}
                        transition={{ delay: 0.1 }}
                        animate={controls1}>
                        <h2>About Us</h2>
                        <span></span>
                        <p>We at Neural Harbour AI specialize in creating holographic agents, robots, and AI/ML solutions, revolutionizing human-machine interaction. With cutting-edge technology, we enhance communication, automate processes, and deliver actionable insights. We're shaping the future by pushing boundaries and driving innovation across industries.</p>
                        <br />
                        <button className='Button'>Learn More</button>
                    </motion.div>
                </section>
                <section id="section2" className='animefy'>
                    <motion.div className="image-animefy" ref={element2}
                        variants={AnimefyImgAnim}
                        transition={{ delay: 0.1 }}
                        animate={controls2}></motion.div>
                    <div className="animefy-content" ref={element2}
                        variants={AnimefyTextAnim}
                        transition={{ delay: 0.1 }}
                        animate={controls2}>
                        <h2>Animefy</h2>
                        <span></span>
                        <p>Using our Image to Anime Converter, you can transform your favourite moments into stunning anime art! Watch your images come to life with brilliant colours, expressive expressions, and the undeniable charm of anime design. Whether you're an experienced artist or a casual fan, unleash your imagination and elevate your memories to a new level of visual magic. Try it now and experience the world through an anime perspective!</p>
                        <br />
                        <button className='Button'>Try Animefy</button>
                    </div>
                </section>
            </main>
            <section className='product'>
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
            </section>
        </>
    );
}

export default Lander;
