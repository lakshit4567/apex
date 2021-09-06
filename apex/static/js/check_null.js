
console.log("In js")

$(".serach").on("click", function (e) {
  console.log($("#id_start_date")[0].value);
  console.log($("#id_end_date")[0].value);

  if ($("#id_start_date")[0].value && $("#id_end_date")[0].value) {
    console.log("value there");
  } else {
    e.preventDefault();
    alert("NO value");
  }
});
