document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch("http://localhost:8000/alumne/list")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res
            
            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");
                
                //Camp del nom de l'alumne
                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.NomAlumne;
                row.appendChild(nomAluCell);

                // Repetir per tots els altres camps restants que retorna l'endpoint
                
                //Camp del cicle
                const cicleCell = document.createElement("td");
                cicleCell.textContent = alumne.Cicle;
                row.appendChild(cicleCell);

                //Camp del curs
                const cursCell = document.createElement("td");
                cursCell.textContent = alumne.Curs;
                row.appendChild(cursCell);

                //Camp del grup
                const grupCell = document.createElement("td");
                grupCell.textContent = alumne.Grup;
                row.appendChild(grupCell);

                //Camp del nom de l'aula
                const descAulaCell = document.createElement("td");
                descAulaCell.textContent = alumne.DescAula;
                row.appendChild(descAulaCell);

                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});