(function () {
  "use strict";
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  // let div = document.getElementsByClassName("container")[0]
  // document.getElementById("form").submit()
  // div.className="loader-container"
  // div.innerHTML = "<div class='loader'></div>"
  var forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }else{
            let div = document.getElementsByClassName("container")[0]
            document.getElementById("form").submit()
            div.classList.remove("container","margin")
            div.classList.add("loader-container")
            div.innerHTML = "<div class='loader'></div>"
        }
        form.classList.add("was-validated");
      },
      false
    );
  });
})();
