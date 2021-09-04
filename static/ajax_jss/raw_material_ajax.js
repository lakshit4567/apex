
// toast function
const alert_msg = (head, msg, boot_class) => {
  return `        
        <div class="toast-div ${boot_class}" id="id-toast">
        <div class="toast-header border-bottom">
            <strong class="mr-auto text-dark">${head}</strong>
            <button class=" btn btn-lg pr-lg-2 m-0 py-0 float-right" onclick='this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode); return false;'>
                                &times;</button>
        </div>
        <div class="toast-body border-top px-lg-5 text-center">
        ${msg}
        </div>
    </div>
    <script>
      $('#id-toast').delay(1600).fadeOut();
    </script>
    `;
};


var liveToastBtn = document.getElementById("liveToastBtn");
$("#btnsave").click("#post-form", function () {
  // $("#btnsave").click(function(){
  output = "";
  let raw_date = $("#raw_date").val();
  let raw_thickness = $("#raw_thickness").val();
  let raw_size = $("#raw_size").val();
  let raw_grade = $("#raw_grade").val();
  let raw_weight = $("#raw_weight").val();
  let s_weight = $("#S_Weight").val();
  let raw_vendor = $("#raw_vendor").val();
  let csr = $("input[name=csrfmiddlewaretoken").val();
  // console.log(raw_date);
  // console.log(raw_thickness);
  // console.log(raw_size);
  // console.log(raw_grade);
  // console.log(raw_weight);
  // console.log(s_weight);

  raw_data = {
    r_date: raw_date,
    r_thickness: raw_thickness,
    r_size: raw_size,
    r_grade: raw_grade,
    r_weight: raw_weight,
    sc_weight: s_weight,
    raw_vendor: raw_vendor,
    csrfmiddlewaretoken: csr,
  };
  if (raw_date == "") {
    $("#toast_id").html(
      alert_msg("Error!", "Please input field", "toast-div-danger")
    );
    // $("#msg-raw").html('<div class="mt-2 text- alert alert-danger alert-dismissible fade show" role="alert"><strong>Error!</strong> Please Date field.<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
  } else if(raw_vendor == ""){
    console.log("djkdkk")
    $("#toast_id").html(
      alert_msg("Error!", "Please Enter Vendor", "toast-div-success")
    );  
    // alert_msg("Error!", "Please Enter Vendor", "toast-div-danger")
  }
  
  else if (raw_thickness == "") {
    $("#toast_id").html(
      alert_msg("Error!", "Please input field", "toast-div-danger")
    );
  } else if (raw_size == "") {
    $("#toast_id").html(
      alert_msg("Error!", "Please input field", "toast-div-danger")
    );
  } else if (raw_grade == "") {
    $("#toast_id").html(
      alert_msg("Error!", "Please input field", "toast-div-danger")
    );
  } else if (raw_weight == "") {
    $("#toast_id").html(
      alert_msg("Error!", "Please input field", "toast-div-danger")
    );
  } else if (s_weight == "") {
    $("#toast_id").html(
      alert_msg("Error!", "Please input field", "toast-div-danger")
    );
  } else {
    $.ajax({
      url: "raw_save",
      method: "POST",
      data: raw_data,
      dataType: "json",
      success: function (data) {
        x = data.raw_data1;
        if (data.status == "Save") {
          for (i = 0; i < x.length; i++) {
            output +=
              "<tr><td>" +
              x[i].id +
              "</td><td>" +
              x[i].register_id +
              "</td><td>" +
              x[i].Vendor +
              "</td><td>" +
              x[i].RM_Date +
              "</td><td>" +
              x[i].RM_Thickness +
              "</td><td>" +
              x[i].RM_Size +
              "</td><td>" +
              x[i].RM_Grade +
              "</td><td>" +
              x[i].RM_coilWeight +
              "</td><td>" +
              x[i].RM_scrapWeight +
              "<td class='text-center d-flex justify-content-around'><a class='btn btn-danger btn-sm btn-del' title='delet' id='del' data-sid = " +
              x[i].id +
              "><i class='fa fa-trash'></i> </a></td></tr>";
            // console.log(output);
            $("#toast_id").html(
              alert_msg("Success!", "New Entry Added", "toast-div-success")
            );
          }
          // $("#raw_date").val("");
          $("#raw_thickness").val("");
          $("#raw_size").val("");
          // $("#raw_grade").val("");
          $("#raw_weight").val("");
          $("#S_Weight").val("");
          $("#raw_vendor").val("");
          $("#tbody").html(output);
          // $("#post_form_raw")[0].reset();
          if (data.status == 0) {
            $("#toast_id").html(
              alert_msg("Alert!", "Unable to Add Data", "toast-div-danger")
            );
          }
        }
      },
    });
  }
});
$("#tbody").on("click", ".btn-del", function () {
  // console.log('button selected')
  let id = $(this).attr("data-sid");
  let csr = $("input[name=csrfmiddlewaretoken").val();
  console.log(id);
  mydata = { sid: id, csrfmiddlewaretoken: csr };
  mythis = this;
  $.ajax({
    url: "raw_delete",
    method: "POST",
    data: mydata,
    success: function (data) {
      if (data.status == 1) {
        $("#toast_id").html(
          alert_msg("Success!", "Entry Deleted", "toast-div-danger")
        );
        $(mythis).closest("tr").fadeOut();
      }
    },
  });
});
