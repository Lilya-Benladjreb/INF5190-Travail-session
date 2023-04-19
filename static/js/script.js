console.log("JS fonctionne")

function submitFormAjax() {
    console.log("submitFormAjax()")
    const form = document.getElementById('search-by-date');
    const table = document.querySelector('#contrevenants-table');

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const startDate = form.querySelector('#du').value;
        const endDate = form.querySelector('#au').value;


        fetch(`/api/contrevenants?$du=${startDate}&au=${endDate}`)
            .then(response => response.json())
            .then(data => {
                const filteredContrevenants = data;
                const establishments = {};

                filteredContrevenants.forEach(contrevenant => {
                    if (!establishments[contrevenant.etablissement]) {
                        establishments[contrevenant.etablissement] = {
                            nbContraventions: 0
                        };
                    }
                    establishments[contrevenant.etablissement].nbContraventions += 1;
                });

                // clear previous table rows
                table.innerHTML = '';

                // add table headers
                const tableHeaders = `
        <tr>
          <th>Nom de l'établissement</th>
          <th>Nombre de contraventions</th>
        </tr>
      `;
                table.insertAdjacentHTML('beforeend', tableHeaders);

                // add table rows
                Object.keys(establishments).forEach(establishment => {
                    const nbContraventions = establishments[establishment].nbContraventions;
                    const tableRow = `
          <tr>
            <td>${establishment}</td>
            <td>${nbContraventions}</td>
          </tr>
        `;
                    table.insertAdjacentHTML('beforeend', tableRow);
                });
            })
            .catch(error => console.error(error));
    });
    return false;
}

/* Fonction servant à modifier la requete html en json pour l'envoyer à l'API */
function submitFormPlainte() {
    console.log("sumbitFormPlaite()")
    const form = document.getElementById('formulaire-plainte');
    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const complaintData = {
            etablissement: formData.get('etablissement'),
            adresse: formData.get('adresse'),
            ville: formData.get('ville'),
            date_visite: formData.get('date-visite'),
            nom_user: formData.get('nom-user'),
            prenom_user: formData.get('prenom-user'),
            description_problem: formData.get('description-problem')
        };

        const complaintDataJson = JSON.stringify(complaintData);

        console.log(complaintDataJson)

        fetch('http://127.0.0.1:5000/api/post-inspection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=UTF-8'
            },
            body: complaintDataJson
        })
            .then(response => {
                if (response.ok) {
                    alert('{"message": "Demande d\'inspection effectuée avec succès"}');
                } else {
                    alert('{"erreur": "Un problème est survenu avec la demande"}');
                }
            })
    });
    return false;
}