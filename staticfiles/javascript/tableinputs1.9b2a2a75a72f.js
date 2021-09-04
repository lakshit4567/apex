function addField(argument) {
  console.log("button")
  
  if ($("#raw_table tbody").length == 0) {

    $("#raw_table").append("<tbody></tbody>");
  }
  // Append product to the table
  $("#raw_table tbody").append(
    "<form method='post' id='raw_form'>"+
    "{% csrf_token %}" +
    "<tr>"+
        "<td>" +  + "</td>" + 
        "<td>" +  + "</td>" +
        "<td>" + "<input class='form-control' type='date' name='raw_Date' id='raw_date' required>" + "</td>" +
        "<td>" + "<input class='form-control' type='text' name='raw_thickness' id='raw_thickness' required>" + "</td>" +
        "<td>" + "<input class='form-control' type='text' name='raw_size' id='raw_size required>" + "</td>" +
        "<td>" + "<input class='form-control' type='text' name='raw_grade' id='raw_grade' required>" + "</td>" +
        "<td>" + "<input class='form-control' type='text' name='raw_weight' id='raw_weight' required>" + "</td>" +
        "<td>" + "<input class='form-control' type='text' name='Sc_weight' id='S_Weight' required>" + "</td>" +    
        "<td>" + 
            "<input class='p-2 float-right btn btn-sm btn-primary border rounded-left rounded-right text-uppercase' type='button' value='Save' id='btnsave'>"  + 
        "</td>"+
    "</tr>" +
    "</form>"
  );
  
}

function deleteRow() {
  $("#del").parents("tr").remove();
}

// function productAddToTable() {
//   // First check if a <tbody> tag exists, add one if not
//   if ($("#productTable tbody").length == 0) {
//     $("#productTable").append("<tbody></tbody>");
//   }
//   // Append product to the table
//   $("#productTable tbody").append(
//     "<tr>" +
//       "<td>" +
//       $("#productname").val() +
//       "</td>" +
//       "<td>" +
//       $("#introdate").val() +
//       "</td>" +
//       "<td>" +
//       $("#url").val() +
//       "</td>" +
//       "</tr>"
//   );
// }
