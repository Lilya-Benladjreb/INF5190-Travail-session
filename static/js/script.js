
/* Fonction servant à modifier la requete html en json pour l'envoyer à l'API */
function submitFormPlainte() {
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
            .catch(error => {
              alert('{"erreur": "Un problème est survenu avec la demande"}');
            });
      });
      return false ;
}