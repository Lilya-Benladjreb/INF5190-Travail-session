$(document).ready(function() {
  $('#search-by-date').submit(function(event) {
    event.preventDefault();
    var start_date = $('#du').val();
    var end_date = $('#au').val();
    $.ajax({
      url: "/contrevenants",
      type: "GET",
      data: {du: start_date, au: end_date},
      dataType: "json",
      success: function(response) {
        // display results in a table
        var results = '<table>';
        results += '<tr><th>Nom</th><th>Nombre de contraventions</th></tr>';
        $.each(response, function(index, contrevenant) {
          results += '<tr><td>' + contrevenant.nom + '</td><td>' + contrevenant.nb_poursuite + '</td></tr>';
        });
        results += '</table>';
        $('#results').html(results);
      },
      error: function(xhr, status, error) {
          alert("Une erreur s'est produite: " + error);
      }
    });
  });
});

function submitFormPlainte() {
  const form = document.getElementById('formulaire-plainte');
      form.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const complaintData = {
          etablissement: formData.get('etablissement'),
          adresse: formData.get('adresse'),
          ville: formData.get('ville'),
          dateVisite: formData.get('date-visite'),
          nom_user: formData.get('nom_user'),
          prenom_user: formData.get('prenom_user'),
          descriptionProblem: formData.get('description-problem')
        };

        fetch('/api/post-inspection', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(complaintData)
        })
        .then(response => {
          if (response.ok) {
            alert('{"message": "Demande d\'inspection effectuée avec succès"}');
          } else {
            alert('{"erreur": "Un problème est survenue avec la demande"}');
          }
        })
        .catch(error => {
          alert('{"erreur": "Un problème est survenue avec la demande"}');
        });
      });
}