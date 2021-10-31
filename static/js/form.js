$("form[name=signup_form").submit(function(e) {

  var $form = $(this);
  var data = $form.serialize();

  $.ajax({
    url: "/create_user",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      alert("Signup successful : " + JSON.stringify(resp)); 
    },
    error: function(resp) {
      alert("Error : " + JSON.stringify(resp));
    }
  });
  e.preventDefault();
});


$("form[name=search_form").submit(function(e) {

  var $form = $(this);
  var data = $form.serialize();

  $.ajax({
    url: "/search",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      alert("Succesful : " + JSON.stringify(resp));
    },
    error: function(resp) {
      alert("Error : " + JSON.stringify(resp));
    }
  });

  e.preventDefault();
});