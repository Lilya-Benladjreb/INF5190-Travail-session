console.log("JS fonctionne")

async function handleSearchFormSubmit( event ) {
    event.preventDefault();

    const dateDebut = document.getElementById( "du" ).value;
    const dateFin = document.getElementById( "au" ).value;
    let xhr = new XMLHttpRequest();

    try {
        xhr.open( 'GET', "/api/contrevenants?du=${dateDebut}&au=${dateFin}" );
        xhr.onload = function() {
            if ( xhr.status === 200 ) {
                let resultats = JSON.parse( xhr.responseText );
                let valeursIndex6 = [];

                for ( let i = 0; i < resultats.length; i++ ) {
                    valeursIndex6.push( resultats[ i ][ 6 ] );
                }

                let occurences = {};

                for ( let i = 0; i < valeursIndex6.length; i++ ) {
                    let valeur = valeursIndex6[i];
                    if ( occurences[ valeur ] === undefined ) {
                        occurences[ valeur ] = 1;
                    } else {
                        occurences[ valeur ]++;
                    }
                }
                afficherResultats( occurences );
            } else {
                console.log( 'Erreur ' + xhr.status );
            }
        };
        xhr.send();
    } catch ( error ) {
        console.error( "Erreur lors de la récupération des données :", error );
    }
}

const inputSearchForm = document.getElementById( "search-by-date" );

if( inputSearchForm ) {
    document.getElementById( "search-by-date" ).
    addEventListener( "submit", handleSearchFormSubmit );
}

function afficherResultats( resultats ) {

    let tableResultats = document.createElement( "table" );
    let tbodyResultats = document.createElement( "tbody" );
    let trHeader = document.createElement( "tr" );
    let thValeur = document.createElement( "th" );
    let thOccurrences = document.createElement( "th" );

    thValeur.innerText = "Établissement";
    thOccurrences.innerText = "Nombre d'infractions";

    trHeader.appendChild( thValeur );
    trHeader.appendChild( thOccurrences );
    tbodyResultats.appendChild( trHeader );

    for ( let valeur in resultats ) {

        let trOccurrence = document.createElement( "tr" );
        let tdValeur = document.createElement( "td" );
        let tdOccurrences = document.createElement( "td" );

        tdValeur.innerText = valeur;
        tdOccurrences.innerText = resultats[ valeur ];

        trOccurrence.appendChild( tdValeur );
        trOccurrence.appendChild( tdOccurrences );

        tbodyResultats.appendChild( trOccurrence );
    }

    tableResultats.appendChild( tbodyResultats );
    let divResultats = document.getElementById( "resultats" );
    divResultats.innerHTML = "";
    divResultats.appendChild( tableResultats );

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