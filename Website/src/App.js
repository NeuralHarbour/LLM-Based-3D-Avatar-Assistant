import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Lander from './LandingPage/Landing'
import Login from './Login and Signup/Login';
import Register from './Login and Signup/Register';
import Usrdashbrd from './Dashboard/Usrdashbrd';
import About from './About/about';
import Services from "./Services/Services";
import Contact from "./contact/Contact";
import Footer from "./Footer/Footer";
function App() {

  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<>
            <Lander />
            <About />
            <Services />
            <Contact />
            <Footer />
          </>} />
          <Route path='/Login' element={<Login />} />
          <Route path='/Register' element={<Register />} />
          <Route path='/Usrdashbrd' element={<Usrdashbrd />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
