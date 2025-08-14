import React from "react";
import ItemCard from "../components/ItemCard";
import './Estante.css';

//DATA MOCKADA
const mockLivros = [
    { id: 1, title: "Duna", author: "Frank Herbert" },
    { id: 2, title: "1984", author: "George Orwell" },
    { id: 3, title: "O Senhor dos Anéis", author: "J.R.R. Tolkien" },
    { id: 4, title: "A Revolução dos Bichos", author: "George Orwell" },
    { id: 5, title: "O Hobbit", author: "J.R.R. Tolkien" },
    ];

function Estante() {
    return (
        <div className="estante">
            <h2>Biblioteca</h2>
            <div className="grid-de-livros">
                {mockLivros.map( livro => (
                    <ItemCard key={livro.id} livro={livro} />
                ))}
            </div>
        </div>
    );
}   
export default Estante;