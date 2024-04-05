function locomotive() {
    gsap.registerPlugin(ScrollTrigger);

    const locoScroll = new LocomotiveScroll({
        el: document.querySelector("#main"),
        smooth: true,
    });
    locoScroll.on("scroll", ScrollTrigger.update);

    ScrollTrigger.scrollerProxy("#main", {
        scrollTop(value) {
            return arguments.length
                ? locoScroll.scrollTo(value, 0, 0)
                : locoScroll.scroll.instance.scroll.y;
        },

        getBoundingClientRect() {
            return {
                top: 0,
                left: 0,
                width: window.innerWidth,
                height: window.innerHeight,
            };
        },

        pinType: document.querySelector("#main").style.transform
            ? "transform"
            : "fixed",
    });
    ScrollTrigger.addEventListener("refresh", () => locoScroll.update());
    ScrollTrigger.refresh();
}
locomotive();


const canvas = document.querySelector("canvas");
const context = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;


window.addEventListener("resize", function () {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    render();
});

function files(index) {
    var data = `
       ./Frames_Convert/0001.png
       ./Frames_Convert/0002.png
       ./Frames_Convert/0003.png
       ./Frames_Convert/0004.png
       ./Frames_Convert/0005.png
       ./Frames_Convert/0006.png
       ./Frames_Convert/0007.png
       ./Frames_Convert/0008.png
       ./Frames_Convert/0009.png
       ./Frames_Convert/0010.png
       ./Frames_Convert/0011.png
       ./Frames_Convert/0012.png
       ./Frames_Convert/0013.png
       ./Frames_Convert/0014.png
       ./Frames_Convert/0015.png
       ./Frames_Convert/0016.png
       ./Frames_Convert/0017.png
       ./Frames_Convert/0018.png
       ./Frames_Convert/0019.png
       ./Frames_Convert/0020.png
       ./Frames_Convert/0021.png
       ./Frames_Convert/0022.png
       ./Frames_Convert/0023.png
       ./Frames_Convert/0024.png
       ./Frames_Convert/0025.png
       ./Frames_Convert/0026.png
       ./Frames_Convert/0027.png
       ./Frames_Convert/0028.png
       ./Frames_Convert/0029.png
       ./Frames_Convert/0030.png
       ./Frames_Convert/0031.png
       ./Frames_Convert/0032.png
       ./Frames_Convert/0033.png
       ./Frames_Convert/0034.png
       ./Frames_Convert/0035.png
       ./Frames_Convert/0036.png
       ./Frames_Convert/0037.png
       ./Frames_Convert/0038.png
       ./Frames_Convert/0039.png
       ./Frames_Convert/0040.png
       ./Frames_Convert/0041.png
       ./Frames_Convert/0042.png
       ./Frames_Convert/0043.png
       ./Frames_Convert/0044.png
       ./Frames_Convert/0045.png
       ./Frames_Convert/0046.png
       ./Frames_Convert/0047.png
       ./Frames_Convert/0048.png
       ./Frames_Convert/0049.png
       ./Frames_Convert/0050.png
       ./Frames_Convert/0051.png
       ./Frames_Convert/0052.png
       ./Frames_Convert/0053.png
       ./Frames_Convert/0054.png
       ./Frames_Convert/0055.png
       ./Frames_Convert/0056.png
       ./Frames_Convert/0057.png
       ./Frames_Convert/0058.png
       ./Frames_Convert/0059.png
       ./Frames_Convert/0060.png
       ./Frames_Convert/0061.png
       ./Frames_Convert/0062.png
       ./Frames_Convert/0063.png
       ./Frames_Convert/0064.png
       ./Frames_Convert/0065.png
       ./Frames_Convert/0066.png
       ./Frames_Convert/0067.png
       ./Frames_Convert/0068.png
       ./Frames_Convert/0069.png
       ./Frames_Convert/0070.png
       ./Frames_Convert/0071.png
       ./Frames_Convert/0072.png
       ./Frames_Convert/0073.png
       ./Frames_Convert/0074.png
       ./Frames_Convert/0075.png
       ./Frames_Convert/0076.png
       ./Frames_Convert/0077.png
       ./Frames_Convert/0078.png
       ./Frames_Convert/0079.png
       ./Frames_Convert/0080.png
       ./Frames_Convert/0081.png
       ./Frames_Convert/0082.png
       ./Frames_Convert/0083.png
       ./Frames_Convert/0084.png
       ./Frames_Convert/0085.png
       ./Frames_Convert/0086.png
       ./Frames_Convert/0087.png
       ./Frames_Convert/0088.png
       ./Frames_Convert/0089.png
       ./Frames_Convert/0090.png
       ./Frames_Convert/0091.png
       ./Frames_Convert/0092.png
       ./Frames_Convert/0093.png
       ./Frames_Convert/0094.png
       ./Frames_Convert/0095.png
       ./Frames_Convert/0096.png
       ./Frames_Convert/0097.png
       ./Frames_Convert/0098.png
       ./Frames_Convert/0099.png
       ./Frames_Convert/0100.png
       ./Frames_Convert/0101.png
       ./Frames_Convert/0102.png
       ./Frames_Convert/0103.png
       ./Frames_Convert/0104.png
       ./Frames_Convert/0105.png
       ./Frames_Convert/0106.png
       ./Frames_Convert/0107.png
       ./Frames_Convert/0108.png
       ./Frames_Convert/0109.png
       ./Frames_Convert/0110.png
       ./Frames_Convert/0111.png
       ./Frames_Convert/0112.png
       ./Frames_Convert/0113.png
       ./Frames_Convert/0114.png
       ./Frames_Convert/0115.png
       ./Frames_Convert/0116.png
       ./Frames_Convert/0117.png
       ./Frames_Convert/0118.png
       ./Frames_Convert/0119.png
       ./Frames_Convert/0120.png
       ./Frames_Convert/0121.png
       ./Frames_Convert/0122.png
       ./Frames_Convert/0123.png
       ./Frames_Convert/0124.png
       ./Frames_Convert/0125.png
       ./Frames_Convert/0126.png
       ./Frames_Convert/0127.png
       ./Frames_Convert/0128.png
       ./Frames_Convert/0129.png
       ./Frames_Convert/0130.png
       ./Frames_Convert/0131.png
       ./Frames_Convert/0132.png
       ./Frames_Convert/0133.png
       ./Frames_Convert/0134.png
       ./Frames_Convert/0135.png
       ./Frames_Convert/0136.png
       ./Frames_Convert/0137.png
       ./Frames_Convert/0138.png
       ./Frames_Convert/0139.png
       ./Frames_Convert/0140.png
       ./Frames_Convert/0141.png
       ./Frames_Convert/0142.png
       ./Frames_Convert/0143.png
       ./Frames_Convert/0144.png
       ./Frames_Convert/0145.png
       ./Frames_Convert/0146.png
       ./Frames_Convert/0147.png
       ./Frames_Convert/0148.png
       ./Frames_Convert/0149.png
       ./Frames_Convert/0150.png
       ./Frames_Convert/0151.png
       ./Frames_Convert/0152.png
       ./Frames_Convert/0153.png
       ./Frames_Convert/0154.png
       ./Frames_Convert/0155.png
       ./Frames_Convert/0156.png
       ./Frames_Convert/0157.png
       ./Frames_Convert/0158.png
       ./Frames_Convert/0159.png
       ./Frames_Convert/0160.png
       ./Frames_Convert/0161.png
       ./Frames_Convert/0162.png
       ./Frames_Convert/0163.png
       ./Frames_Convert/0164.png
       ./Frames_Convert/0165.png
       ./Frames_Convert/0166.png
       ./Frames_Convert/0167.png
       ./Frames_Convert/0168.png
       ./Frames_Convert/0169.png
       ./Frames_Convert/0170.png
       ./Frames_Convert/0171.png
       ./Frames_Convert/0172.png
       ./Frames_Convert/0173.png
       ./Frames_Convert/0174.png
       ./Frames_Convert/0175.png
       ./Frames_Convert/0176.png
       ./Frames_Convert/0177.png
       ./Frames_Convert/0178.png
       ./Frames_Convert/0179.png
       ./Frames_Convert/0180.png
       ./Frames_Convert/0181.png
       ./Frames_Convert/0182.png
       ./Frames_Convert/0183.png
       ./Frames_Convert/0184.png
       ./Frames_Convert/0185.png
       ./Frames_Convert/0186.png
       ./Frames_Convert/0187.png
       ./Frames_Convert/0188.png
       ./Frames_Convert/0189.png
       ./Frames_Convert/0190.png
       ./Frames_Convert/0191.png
       ./Frames_Convert/0192.png
       ./Frames_Convert/0193.png
       ./Frames_Convert/0194.png
       ./Frames_Convert/0195.png
       ./Frames_Convert/0196.png
       ./Frames_Convert/0197.png
       ./Frames_Convert/0198.png
       ./Frames_Convert/0199.png
       ./Frames_Convert/0200.png
       ./Frames_Convert/0201.png
       ./Frames_Convert/0202.png
       ./Frames_Convert/0203.png
       ./Frames_Convert/0204.png
       ./Frames_Convert/0205.png
       ./Frames_Convert/0206.png
       ./Frames_Convert/0207.png
       ./Frames_Convert/0208.png
       ./Frames_Convert/0209.png
       ./Frames_Convert/0210.png
       ./Frames_Convert/0211.png
       ./Frames_Convert/0212.png
       ./Frames_Convert/0213.png
       ./Frames_Convert/0214.png
       ./Frames_Convert/0215.png
       ./Frames_Convert/0216.png
       ./Frames_Convert/0217.png
       ./Frames_Convert/0218.png
       ./Frames_Convert/0219.png
       ./Frames_Convert/0220.png
       ./Frames_Convert/0221.png
       ./Frames_Convert/0222.png
       ./Frames_Convert/0223.png
       ./Frames_Convert/0224.png
       ./Frames_Convert/0225.png
       ./Frames_Convert/0226.png
       ./Frames_Convert/0227.png
       ./Frames_Convert/0228.png
       ./Frames_Convert/0229.png
       ./Frames_Convert/0230.png
       ./Frames_Convert/0231.png
       ./Frames_Convert/0232.png
       ./Frames_Convert/0233.png
       ./Frames_Convert/0234.png
       ./Frames_Convert/0235.png
       ./Frames_Convert/0236.png
       ./Frames_Convert/0237.png
       ./Frames_Convert/0238.png
       ./Frames_Convert/0239.png
       ./Frames_Convert/0240.png
       ./Frames_Convert/0241.png
       ./Frames_Convert/0242.png
       ./Frames_Convert/0243.png
       ./Frames_Convert/0244.png
       ./Frames_Convert/0245.png
       ./Frames_Convert/0246.png
       ./Frames_Convert/0247.png
       ./Frames_Convert/0248.png
       ./Frames_Convert/0249.png
       ./Frames_Convert/0250.png
       ./Frames_Convert/0251.png
       ./Frames_Convert/0252.png
       ./Frames_Convert/0253.png
       ./Frames_Convert/0254.png
       ./Frames_Convert/0255.png
       ./Frames_Convert/0256.png
       ./Frames_Convert/0257.png
       ./Frames_Convert/0258.png
       ./Frames_Convert/0259.png
       ./Frames_Convert/0260.png
       ./Frames_Convert/0261.png
       ./Frames_Convert/0262.png
       ./Frames_Convert/0263.png
       ./Frames_Convert/0264.png
       ./Frames_Convert/0265.png
       ./Frames_Convert/0266.png
       ./Frames_Convert/0267.png
       ./Frames_Convert/0268.png
       ./Frames_Convert/0269.png
       ./Frames_Convert/0270.png
       ./Frames_Convert/0271.png
       ./Frames_Convert/0272.png
       ./Frames_Convert/0273.png
       ./Frames_Convert/0274.png
       ./Frames_Convert/0275.png
       ./Frames_Convert/0276.png
       ./Frames_Convert/0277.png
       ./Frames_Convert/0278.png
       ./Frames_Convert/0279.png
       ./Frames_Convert/0280.png
       ./Frames_Convert/0281.png
       ./Frames_Convert/0282.png
       ./Frames_Convert/0283.png
       ./Frames_Convert/0284.png
       ./Frames_Convert/0285.png
       ./Frames_Convert/0286.png
       ./Frames_Convert/0287.png
       ./Frames_Convert/0288.png
       ./Frames_Convert/0289.png
       ./Frames_Convert/0290.png
       ./Frames_Convert/0291.png
       ./Frames_Convert/0292.png
       ./Frames_Convert/0293.png
       ./Frames_Convert/0294.png
       ./Frames_Convert/0295.png
       ./Frames_Convert/0296.png
       ./Frames_Convert/0297.png
       ./Frames_Convert/0298.png
       ./Frames_Convert/0299.png
       ./Frames_Convert/0300.png
   `;
    return data.split("\n")[index];
}

const frameCount = 300;

const images = [];
const imageSeq = {
    frame: 1,
};

for (let i = 0; i < frameCount; i++) {
    const img = new Image();
    img.src = files(i);
    images.push(img);
}

gsap.to(imageSeq, {
    frame: frameCount - 1,
    snap: "frame",
    ease: `none`,
    scrollTrigger: {
        scrub: 0.15,
        trigger: `#page>canvas`,
        start: `top top`,
        end: `600% top`,
        scroller: `#main`,
    },
    onUpdate: render,
});

images[1].onload = render;

function render() {
    scaleImage(images[imageSeq.frame], context, 0.75);
}

function scaleImage(img, ctx, scaleFactor) {
    var canvas = ctx.canvas;
    var canvasAspectRatio = canvas.width / canvas.height;
    var imgAspectRatio = img.width / img.height;

    var scaleWidth, scaleHeight;
    if (canvasAspectRatio > imgAspectRatio) {
        scaleWidth = canvas.width * scaleFactor;
        scaleHeight = scaleWidth / imgAspectRatio;
    } else {
        scaleHeight = canvas.height * scaleFactor;
        scaleWidth = scaleHeight * imgAspectRatio;
    }

    var offsetX = (canvas.width - scaleWidth) / 2;
    var offsetY = canvas.height - scaleHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, offsetX, offsetY, scaleWidth, scaleHeight);
}





ScrollTrigger.create({
    trigger: "#page>canvas",
    pin: true,
    // markers:true,
    scroller: `#main`,
    start: `top top`,
    end: `600% top`,
});



gsap.to("#page1", {
    scrollTrigger: {
        trigger: `#page1`,
        start: `top top`,
        end: `bottom top`,
        pin: true,
        scroller: `#main`
    }
})
gsap.to("#page2", {
    scrollTrigger: {
        trigger: `#page2`,
        start: `top top`,
        end: `bottom top`,
        pin: true,
        scroller: `#main`
    }
})
gsap.to("#page3", {
    scrollTrigger: {
        trigger: `#page3`,
        start: `top top`,
        end: `bottom top`,
        pin: true,
        scroller: `#main`
    }
})