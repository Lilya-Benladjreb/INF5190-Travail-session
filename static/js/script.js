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