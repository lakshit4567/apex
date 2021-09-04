var quantity = JSON.parse(document.getElementById("quantity").textContent);
var sale = JSON.parse(document.getElementById("sale").textContent);

var dic_q = JSON.stringify(quantity);
var dic_s = JSON.stringify(sale);

if (dic_q == '{}' && dic_s == "{}"){
  document.getElementById("no_data_uf").innerHTML = "<br><div class='alert alert-light lead'><strong>Note:</strong> No Data Available</div>";
}
else{
// FM Stock Chart

var barChartData = {
    labels: [
      "Round",
      "Square"
    ],
    datasets: [
        {
            label: "UFM Sale",
            backgroundColor: 'rgba(69, 123, 157)',
            borderColor: 'rgba(69, 123, 157, 1)',
            borderWidth: 1,
            data: [sale['Round'], sale['Square'],]
        },
        {
            label: "UFM Quantity",
            backgroundColor: 'rgba(29, 53, 87)',
            borderColor: 'rgba(29, 53, 87, 1)',
            borderWidth: 1,
            data: [quantity['Round'],quantity['Square'], ]
        },
        // {
        //     label: "UFM Sale",
        //     backgroundColor: 'rgba(230, 57, 70)',
        //     borderColor: 'rgba(230, 57, 70, 1)',
        //     borderWidth: 1,
        //     data: [, ,]
        // }
    ],
  };
  
  var chartOptions = {
    responsive: true,
    legend: {
      display: false,
    },
    maintainAspectRatio: "false",
  }
  
  window.onload = function() {
    var ctx = document.getElementById("ufmbar").getContext("2d");
    window.myBar = new Chart(ctx, {
      type: "bar",
      data: barChartData,
      options: chartOptions
    });
  };
}