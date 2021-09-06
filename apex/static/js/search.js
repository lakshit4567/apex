// (document).ready( function () {
//         $('#raw_table').DataTable({
//             "pageLength":20,
//             'aoColumnDefs':[{
//                 'bSortable':false,
//                 'aTargets':['nosort'],
//             }],
//             columnDefs:[
//                 {type:'date-dd-mm-yyyy',aTargets:[5]}
//             ],
//             // 'aoColumns':[
//             //     null,
//             //     null,
//             //     null,
//             //     null,
//             //     null,
//             //     null,
//             //     null,
//             //     null,
//             // ],
//             "order":false,
//             "bLengthChange":false,
//             "dom":"<'top'>ct<'top'p><'clear'>"
//             // "aLengthMenu": [[3, 5, 10, 25, -1], [3, 5, 10, 25, "All"]],
//             // "iDisplayLength": 3
//         });
//         $("#filterbox").keyup(function(){
//             DataTable.search(this.value).draw();
//         });
//     } );

function myFunction2() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("Board_Search");
    filter = input.value.toUpperCase();
    table = document.getElementById("Board_table");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[2];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
  

  // $(".serach").on("click", function (e) {
  //   if ($(this).hasClass("prevented")) {
  //     e.preventDefault();
  //     start_date = new Date($("#id_start_date").val());
  //     end_date = new Date($("#id_end_date").val());
  //     console.log(start_date, end_date);

  //     if (start_date && end_date == "Invalid Date") {
  //       alert("PLEASE SELECT START & END DATES");
  //     }

  //     $(this).removeClass("prevented");
  //   }
  // });
