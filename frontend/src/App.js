import React from 'react';
// Importa as ferramentas de roteamento 
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Importa a nova página da estante
import Estante from './pages/Estante'; 
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* add componente mais bonito */}
        <nav style={{ padding: '16px', backgroundColor: '#f0f0f0' }}>
          <Link to="/" style={{ marginRight: '16px' }}>Home</Link>
          <Link to="/estante">Minha Estante</Link>
        </nav>
        <hr />

        <main style={{ padding: '16px' }}>
          {/* O <Routes> define a área onde as páginas serão trocadas */}
          <Routes>
            {/* Rota da Estante */}
            <Route path="/estante" element={<Estante />} />

            {/* Esta é a rota para a página inicial */}
            <Route path="/" element={<h2>Bem-vindo ao Shelfmine!</h2>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;