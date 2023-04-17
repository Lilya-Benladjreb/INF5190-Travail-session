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