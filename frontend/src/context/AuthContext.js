import React, { createContext, useState, useEffect } from 'react';

// Cria o Context com um valor padrão para cobrir a primeira renderização
export const AuthContext = createContext({
    isAuthenticated: false,
    loading: true, // Garante que o estado inicial seja de carregamento
    login: () => {},
    logout: () => {},
    token: null,
});

// Cria o Provedor do Contexto
export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true);

    // Efeito para verificar se já existe um token no localStorage ao iniciar
    useEffect(() => {
        const storedToken = localStorage.getItem('token');
        if (storedToken) {
            setToken(storedToken);
        }
        setLoading(false); // Termina o carregamento após a verificação
    }, []);

    // Função de Login: salva o token no estado e no localStorage
    const login = (newToken) => {
        setToken(newToken);
        localStorage.setItem('token', newToken);
    };

    // Função de Logout: remove o token
    const logout = () => {
        setToken(null);
        localStorage.removeItem('token');
    };

    // Objeto de valor que será compartilhado com todos os componentes filhos
    const value = {
        token,
        isAuthenticated: !!token, // Converte a presença do token em um booleano (true/false)
        loading,
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};