import React, { useRef, useEffect } from 'react';
import { motion } from "framer-motion";
import './about.css';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger'; // Importing ScrollTrigger
import { AboutImgAnim, AboutTextAnim, AnimefyImgAnim, AnimefyTextAnim } from "../Animation";
import { useScroll } from "../useScroll";
import '../Animefy/Animefy.css';

const About = () => {
    const containerRef = useRef();
    const [element1, controls1] = useScroll();
    const [element2, controls2] = useScroll();

    useEffect(() => {
        gsap.registerPlugin(ScrollTrigger); // Registering ScrollTrigger plugin locally

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

    return (
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
    );
}

export default About;
