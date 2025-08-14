// Card que representa um livro, com capa, titulo e autor
import React from 'react';
import './ItemCard.css'; //para estilizar mais pra frente

// Recebendo um obj 'Livro' como propriedade
function ItemCard({ livro }) {
    return (
        <div className="item-card">
            {/* Capa do livro */}
            {/* <img src={livro.capa} alt={livro.titulo} /> */}
            <h4>{livro.title}</h4>
            <p>{livro.author}</p>
            {/* Botões de ação posteriores */}
            <button>Deletar</button>
        </div>    
    );    
}

export default ItemCard;