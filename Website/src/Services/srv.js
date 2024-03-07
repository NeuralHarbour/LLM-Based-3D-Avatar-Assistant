
import { gsap } from "gsap";
import { ScrollScene } from 'scrollscene';


// Register gsap effect
// --------------------------------
gsap.registerEffect({
    name: "scaleDown",
    effect: (targets, config) => {
        return gsap.to(targets, {
            ease: config.ease,
            scale: .7,
            y: -20,
        });
    },
    defaults: {
        ease: 'power1.out'
    },
    extendTimeline: true
});


// Creating a card scene
// --------------------------------
function CreateCardsScene(el) {
    return new ScrollScene({
        triggerElement: el.nextElementSibling,
        offset: -150,
        triggerHook: .5,
        gsap: {
            timeline: stackedCardsTl(el),
        },
        duration: '100%',
    })
}

// Scale down timeLine
// --------------------------------
function stackedCardsTl(el) {
    const timeline = gsap.timeline({ paused: true });
    timeline
        .addLabel('in')
        .scaleDown(el)
    return timeline;
}


// Creating scens and binding tweens to all cards
// ------------------------------------------------
function stackedCards(cardClassName) {
    const cards = document.querySelectorAll(cardClassName);
    for (let index = 0; index < cards.length - 1; index++) {
        CreateCardsScene(cards[index]);
    }
}


// Stacked cards init
// -----------------------------
stackedCards('.card');