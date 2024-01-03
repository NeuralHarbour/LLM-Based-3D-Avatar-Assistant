import {BrowserRouter as Router,Routes, Route} from 'react-router-dom';
import Header from './Navbar/Header';
import Content from './Home/Content';
import Footer from './Footer/Footer';
import News from './News/News';
import Products from './products/Products';
import Login from './Login and Signup/Login';
import Register from './Login and Signup/Register';
import Contact from './contact/Contact';
import Usrdashbrd from './Dashboard/Usrdashbrd';
function App() {
  
  return (
    <div className="App">
      <Router>
        <Routes>
        <Route path="/" element={<>
            <Header />
            <Content />
            <News />
            <Products />
            <Contact />
            <Footer />
          </>} />
          <Route path = '/Login' element = {<Login />} />
          <Route path = '/Register' element = {<Register />} />
          <Route path = '/Usrdashbrd' element ={<Usrdashbrd />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
