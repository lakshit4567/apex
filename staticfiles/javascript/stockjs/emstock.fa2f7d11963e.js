var cylinder = JSON.parse(document.getElementById("cylinder").textContent);

// console.log(cylinder,'asdnkjasdksadkjas')
var dic_c = JSON.stringify(cylinder);
if(dic_c == '{}'){
    document.getElementById("no_data_em").innerHTML = "<br><div class='alert alert-light lead'><strong>Note:</strong> No Data Available</div>";
}

else{

// EM Stock Chart
var ctx = document.getElementById("embar");
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Cylinder", "Belt", "Fevil", "Cutting Oil", "Cutter", "Polish Wheel", "Matt Wheel", "Buff", "Plastic Roll", "Conjunction Rod", "Powder Box", "Big Carton", "Small Plastic"],
        datasets: [{
            label: 'EM Stocks',
            data: [cylinder['Cylinder'],cylinder['Belt'],cylinder['Fevil'],cylinder['Cutting Oil'],
                    cylinder['Cutter'],cylinder['Polish Wheel'],cylinder['Matt Wheel'],cylinder['Buff'],
                    cylinder['Plastic Roll'],cylinder['Conjunction Rod'],cylinder['Powder Box'],
                    cylinder['Big Carton'], cylinder['Small Plastic']],
            backgroundColor: 'rgba(29, 53, 87, 0.9)',
            borderWidth: 0.3
        }]
    },
    options: {
        // indexAxis: 'y',
        responsive: true,
        legend: {
            display: false,
        }
    }
});
}