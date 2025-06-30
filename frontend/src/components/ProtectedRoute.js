import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function ProtectedRoute({ children }) {
    const { isAuthenticated, loading } = useContext(AuthContext);

    if (loading) {
        // Enquanto o AuthContext verifica o token, mostra uma mensagem de carregamento
        return <div>A carregar...</div>;
    }

    if (!isAuthenticated) {
        // Se, após a verificação, não estiver autenticado, redireciona para a página de login
        return <Navigate to="/login" />;
    }

    // Se estiver autenticado, renderiza o componente filho (página protegida)
    return children;
}

export default ProtectedRoute;