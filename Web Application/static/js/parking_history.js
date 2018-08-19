$(function() {

  $("#historyForm input").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
      // additional error messages or events
    },
    submitSuccess: function($form, event) {
      event.preventDefault(); // prevent default submit behaviour
      // get values from FORM
      var currentHolderH = $("input#currentHolderH").val();
      var carpark = $("select#carparkOptions").val();
        
      $this = $("#sendIDCButton");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
      $.ajax({
        url: "/parkinghistory",
        type: "POST",
        data: {
          currentholderH: currentHolderH,
          carpark: carpark
        },
        cache: false,
        success: function(result) {
          $('#success2').html("<div class='alert alert-success'>");
          $('#success2 > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success2 > .alert-success')
            .append(result);
          $('#success2 > .alert-success')
            .append('</div>');
          //clear all fields
          $('#historyForm').trigger("reset");
        },
        error: function() {
          // Fail message
          $('#success2').html("<div class='alert alert-danger'>");
          $('#success2 > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success2 > .alert-danger').append($("<strong>").text("Sorry, it seems that the flask server is not responding. Please try again later!"));
          $('#success2 > .alert-danger').append('</div>');
          //clear all fields
          $('#historyForm').trigger("reset");
        },
        complete: function() {
          setTimeout(function() {
            $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
          }, 1000);
        }
      });
    },
    filter: function() {
      return $(this).is(":visible");
    },
  });

  $("a[data-toggle=\"tab\"]").click(function(e) {
    e.preventDefault();
    $(this).tab("show");
  });
});

/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
  $('#success2').html('');
});
