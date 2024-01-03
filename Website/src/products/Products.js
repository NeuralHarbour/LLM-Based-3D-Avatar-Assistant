import React from 'react'
import './products.css'
const Products = () => {
  return (
    <section sec = "" class='sd' style = {{backgroundColor:'skyblue'}}>
        <div className='sd InnerContain'>
            <div className='sd InnerContain2'>
                <h2 className='sd heading'>PRODUCTS</h2>
                <p className='txt2 sd para'>Here are our products available for purchase and download</p>
            </div>
            <div className='boxes'>
                <div className='container'>
                    <div className='wrapper'>
                        <div className='banner'></div>
                            <h1>HOLOGRAM BOX</h1>
                            <p className='txt'>Lorem ipsum dolor sit amet</p>
                    </div>
                    <div className='buttonwrapper'>
                        <button className='btn outline'>
                            DETAILS
                        </button>
                        <button className='btn fill'>
                            BUY NOW
                        </button>
                    </div>     
                </div>
                <div className='container'>
                    <div className='wrapper'>
                        <div className='banner'></div>
                            <h1>MOBILE APP</h1>
                            <p className='txt'>Lorem ipsum dolor sit amet</p>
                    </div>
                    <div className='iconwrapper'>
                        <i class="fab fa-google-play icon"></i>
                        <i class="fab fa-app-store icon"></i>
                    </div>     
                </div>
            </div>
        </div>
    </section>
  )
}

export default Products