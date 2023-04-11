function validerRechercheParDate() {
    let form = document.forms["search-by-date"];
    let du = form["date-du"].value;
    let au = form["date-au"].value;
    let paras = document.getElementsByTagName("p");
    let validated = true;

    for(let i = 0; i < paras.length; i++) {
        paras[i].innerHTML = "";
    }

    if (du === "") {
        document.getElementById("date-du-err").innerHTML = "Les deux dates sont demandées pour la recherche";
        validated = false;
    }else if (au === "") {
        document.getElementById("date-au-err").innerHTML = "Les deux dates sont demandées pour la recherche";
        validated = false;
    }

    return validated;
}

function soumettreRechercheParDate() {
    if(validerRechercheParDate()) {
        document.forms["search-by-date"].submit();
    }
}

function rechercheAjaxFetch() {
    const PROTOCOL = location.protocol;
    const HOST = location.host;
    const contrevenants_URL = `${PROTOCOL}//${HOST}/api/contrevenants`;
    const searchForm = document.getElementById('form-ajax');
    const resultsBody = document.getElementById('results-body');

    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
          const queryDu = document.getElementById('date-du').value;
          const queryAu = document.getElementById('date-au').value;

          fetch(`${contrevenants_URL}?du=${queryDu}&au=${queryAu}`)
                .then(response => response.json())
                .then(data => {
                    resultsBody.innerHTML = '';
                    data.forEach(contrevenant => {
                        const row = document.createElement('tr');
                        const nameCell = document.createElement('td');
                        const countCell = document.createElement('td');

                        nameCell.textContent = contrevenant.etablissement;
                        countCell.textContent = contrevenant.date_infraction;

                        row.appendChild(nameCell);
                        row.appendChild(countCell);
                        resultsBody.appendChild(row);
                        });
                });

          });
}