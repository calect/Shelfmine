import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

// Importa nossas páginas e componentes
import Login from './pages/Login';
import Register from './pages/Register';
import Estante from './pages/Estante';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Rotas Públicas */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Rota Protegida */}
            <Route 
              path="/estante" 
              element={
                <ProtectedRoute>
                  <Estante />
                </ProtectedRoute>
              } 
            />
            
            {/* Rota Padrão: redireciona para o login */}
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
