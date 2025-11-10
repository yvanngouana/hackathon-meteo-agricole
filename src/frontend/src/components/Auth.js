import React, { useState, createContext, useContext, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

// Contexte d'authentification
const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

// Composant de connexion
export const Login = () => {
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Ici, tu devras implémenter l'appel à ton API backend
      // Par exemple: const response = await axios.post('/api/auth/login', credentials);
      // Pour l'instant, on simule une connexion réussie
      console.log('Tentative de connexion avec:', credentials);
      
      // Simuler une réponse d'API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mise à jour du contexte d'authentification
      const userData = {
        id: 1,
        email: credentials.email,
        name: 'Agriculteur',
        role: 'farmer'
      };
      
      localStorage.setItem('user', JSON.stringify(userData));
      localStorage.setItem('token', 'fake-jwt-token');
      
      // Redirection vers le dashboard
      navigate('/');
    } catch (err) {
      setError('Email ou mot de passe incorrect');
      console.error('Erreur de connexion:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="d-flex align-items-center justify-content-center" style={{ minHeight: '100vh' }}>
      <Col md={6} lg={4}>
        <Card className="shadow">
          <Card.Body className="p-4">
            <div className="text-center mb-4">
              <h3 className="fw-bold text-success">Météo Agricole</h3>
              <p className="text-muted">Connectez-vous à votre compte</p>
            </div>
            
            {error && <Alert variant="danger">{error}</Alert>}
            
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3" controlId="formEmail">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={credentials.email}
                  onChange={handleInputChange}
                  placeholder="votre@email.com"
                  required
                />
              </Form.Group>

              <Form.Group className="mb-4" controlId="formPassword">
                <Form.Label>Mot de passe</Form.Label>
                <Form.Control
                  type="password"
                  name="password"
                  value={credentials.password}
                  onChange={handleInputChange}
                  placeholder="Mot de passe"
                  required
                />
              </Form.Group>

              <Button 
                variant="success" 
                type="submit" 
                className="w-100 py-2"
                disabled={loading}
              >
                {loading ? 'Connexion...' : 'Se connecter'}
              </Button>
            </Form>
            
            <div className="text-center mt-3">
              <small className="text-muted">
                Pas encore de compte ? <a href="/register">S'inscrire</a>
              </small>
            </div>
          </Card.Body>
        </Card>
      </Col>
    </Container>
  );
};

// Composant d'inscription
export const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Ici, tu devras implémenter l'appel à ton API backend
      // Par exemple: await axios.post('/api/auth/register', formData);
      console.log('Tentative d\'inscription avec:', formData);
      
      // Simuler une réponse d'API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mise à jour du contexte d'authentification
      const newUser = {
        id: 2,
        email: formData.email,
        name: formData.name,
        role: 'farmer'
      };
      
      localStorage.setItem('user', JSON.stringify(newUser));
      localStorage.setItem('token', 'fake-jwt-token');
      
      // Redirection vers le dashboard
      navigate('/');
    } catch (err) {
      setError('Erreur lors de l\'inscription');
      console.error('Erreur d\'inscription:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="d-flex align-items-center justify-content-center" style={{ minHeight: '100vh' }}>
      <Col md={6} lg={4}>
        <Card className="shadow">
          <Card.Body className="p-4">
            <div className="text-center mb-4">
              <h3 className="fw-bold text-success">Météo Agricole</h3>
              <p className="text-muted">Créez votre compte</p>
            </div>
            
            {error && <Alert variant="danger">{error}</Alert>}
            
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3" controlId="formName">
                <Form.Label>Nom complet</Form.Label>
                <Form.Control
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Votre nom"
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formEmail">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="votre@email.com"
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formPassword">
                <Form.Label>Mot de passe</Form.Label>
                <Form.Control
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Mot de passe"
                  required
                />
              </Form.Group>

              <Form.Group className="mb-4" controlId="formConfirmPassword">
                <Form.Label>Confirmer le mot de passe</Form.Label>
                <Form.Control
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  placeholder="Confirmer le mot de passe"
                  required
                />
              </Form.Group>

              <Button 
                variant="success" 
                type="submit" 
                className="w-100 py-2"
                disabled={loading}
              >
                {loading ? 'Création du compte...' : 'S\'inscrire'}
              </Button>
            </Form>
            
            <div className="text-center mt-3">
              <small className="text-muted">
                Vous avez déjà un compte ? <a href="/login">Se connecter</a>
              </small>
            </div>
          </Card.Body>
        </Card>
      </Col>
    </Container>
  );
};

// Composant de fournisseur d'authentification
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    // Vérifier si un utilisateur est déjà connecté au chargement
    const user = JSON.parse(localStorage.getItem('user'));
    const token = localStorage.getItem('token');
    
    if (user && token) {
      setCurrentUser(user);
    }
    
    setLoading(false);
  }, []);

  const login = (userData, token) => {
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', token);
    setCurrentUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setCurrentUser(null);
  };

  const value = {
    currentUser,
    login,
    logout
  };

  if (loading) {
    return <div>Chargement...</div>;
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook pour protéger les routes
export const useAuthStatus = () => {
  const [loggedIn, setLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setLoggedIn(true);
    }
    setLoading(false);
  }, []);
  
  return { loggedIn, loading };
};