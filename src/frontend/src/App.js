import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import FieldManagement from './pages/FieldManagement';
import WeatherForecast from './pages/WeatherForecast';
import IrrigationRecommendations from './pages/IrrigationRecommendations';
import DiseaseAlerts from './pages/DiseaseAlerts';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Container className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/fields" element={<FieldManagement />} />
            <Route path="/weather" element={<WeatherForecast />} />
            <Route path="/irrigation" element={<IrrigationRecommendations />} />
            <Route path="/diseases" element={<DiseaseAlerts />} />
          </Routes>
        </Container>
        <Footer />
      </div>
    </Router>
  );
}

export default App;