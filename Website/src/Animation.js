import { gsap } from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export const homeAnimation = {
    hidden: { x: -400, opacity: 0 },
    show: { x: 0, opacity: 1 },
};
export const LanderText1 = {
    hidden: {
        left: -400,
        opacity: 0
    },
    show: {
        left: 95,
        opacity: 1
    },
};
export const LanderText2 = {
    hidden: {
        left: 400,
        opacity: 0
    },
    show: {
        left: 95,
        opacity: 1
    },
};
export const homeInfoAnimation = {
    hidden: { x: 100, opacity: 0 },
    show: { x: 0, opacity: 1 },
};

export const navAnimation = {
    hidden: { y: -20, opacity: 0 },
    show: { y: 1, opacity: 1 },
}

export const AboutImgAnim = {
    hidden: { opacity: 0, x: -50 },
    show: {
        opacity: 1,
        x: 1,
        transition: {
            duration: 1,
            ease: "easeOut",
            onStart: () => {
                gsap.fromTo(".image", { opacity: 0, x: -50 }, { opacity: 1, x: 1, duration: 1 });
            }
        }
    }
};


export const AboutTextAnim = {
    hidden: { opacity: 0, x: 50 },
    show: {
        opacity: 1,
        x: -10,
        transition: {
            duration: 1,
            ease: "easeOut",
            onStart: () => {
                gsap.fromTo(".content", { opacity: 0, x: 50 }, { opacity: 1, x: -10, duration: 1 });
            }
        }
    }
};
export const AnimefyImgAnim = {
    hidden: { opacity: 0, x: 50 },
    show: {
        opacity: 1,
        x: 0,
        transition: {
            duration: 1,
            ease: "easeOut",
            onStart: () => {
                gsap.fromTo(".image-animefy", { opacity: 0, x: -50 }, { opacity: 1, x: 1, duration: 1 });
            }
        }
    }
};

export const AnimefyTextAnim = {
    hidden: { opacity: 0, x: -50 },
    show: {
        opacity: 1,
        x: 10,
        transition: {
            duration: 1,
            ease: "easeOut",
            onStart: () => {
                gsap.fromTo(".animefy-content", { opacity: 0, x: -50 }, { opacity: 1, x: -10, duration: 1 });
            }
        }
    }
};






// export const servicesAnimations = {
//     hidden: { y: 200, opacity: 0 },
//     show: { y: 0, opacity: 1 },
// };

// export const portfolioAnimations = {
//     hidden: { scale: 0, opacity: 0 },
//     show: { scale: 1, opacity: 1 },
// };

// export const milestonesAnimations = {
//     hidden: { scale: 0, opacity: 0 },
//     show: { scale: 1, opacity: 1 },
// };

// export const blogsAnimation = {
//     hidden: { y: 200, opacity: 0 },
//     show: { y: 0, opacity: 1 },
// };

// export const videoAnimations = {
//     hidden: { scale: 0, opacity: 0 },
//     show: { scale: 1, opacity: 1 },
// };

// export const pricingAnimation = {
//     hidden: { y: 200, opacity: 0 },
//     show: { y: 0, opacity: 1 },
// };

// export const testimonialsAnimations = {
//     hidden: { scale: 0, opacity: 0 },
//     show: { scale: 1, opacity: 1 },
// };

// export const skillsBarAnimation = {
//     hidden: { y: 0, opacity: 0 },
//     show: { y: 1, opacity: 1 },
// };

// export const contactAnimation = {
//     hidden: { y: 200, opacity: 0 },
//     show: { y: 0, opacity: 1 },
// };

// export const footerTextAnimation = {
//     hidden: { x: -200, opacity: 0 },
//     show: { x: 1, opacity: 1 },
// };