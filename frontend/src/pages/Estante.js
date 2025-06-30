import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

function Estante() {
    const { logout } = useContext(AuthContext);

    return (
        <div>
            <h1>Minha Estante de Livros</h1>
            <p>Bem-vindo! Aqui você poderá ver e gerenciar seus livros.</p>
            {/* Adicionar a lógica para buscar e criar livros aqui */}
            <button onClick={logout}>Sair (Logout)</button>
        </div>
    );
}

export default Estante;
