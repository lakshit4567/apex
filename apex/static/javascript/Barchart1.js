$(".pagination").addClass("justify-content-center");
var rw_month = JSON.parse(document.getElementById("rw_month").textContent);
var rw_s_month = JSON.parse(document.getElementById("rw_s_month").textContent);
var fm_w = JSON.parse(document.getElementById("fm_w").textContent);
var fm_s = JSON.parse(document.getElementById("fm_s").textContent);

var empty_dic_month = JSON.stringify(rw_month)
var empty_dic_s_month = JSON.stringify(rw_s_month)
var empty_dic_fm_w = JSON.stringify(fm_w)
var empty_dic_fm_s = JSON.stringify(fm_s)

if ( empty_dic_month == "{}" && empty_dic_s_month == '{}' ){
    document.getElementById("no_data_rm_o").innerHTML = "<h5>Raw Material Monthly Data</h5><br><div class='alert alert-light lead'><strong>Note:</strong> No Data Available</div>";
}
else{
//First Chart
var speedCanvas = document.getElementById("speedChart");

var dataFirst = {
    label: "Raw Material Weight",
    data: [rw_month['01'],rw_month['05'], rw_month['10'], rw_month['15'], rw_month['20'], rw_month['25'], rw_month['30']],
    lineTension: 0,
    fill: false,
    borderColor: "rgba(29, 53, 87)"
};

var dataSecond = {
    label: "Raw Material ScrapWeight",
    data: [rw_s_month['01'], rw_s_month['05'], rw_s_month['10'], rw_s_month['15'], rw_s_month['20'], rw_s_month['25'], rw_s_month['30']],
    lineTension: 0,
    fill: false,
    borderColor: "rgba(230, 57, 70)"
};

var speedData = {
labels: ["1", "5", "10", "15", "20", "25", "30"],
datasets: [dataFirst, dataSecond]
};

var chartOptions = {
legend: {
    display: true,
    position: 'top',
    labels: {
    boxWidth: 80,
    fontColor: 'black'
    }
}
};

var lineChart = new Chart(speedCanvas, {
type: 'line',
data: speedData,
options: chartOptions
});
}

if (empty_dic_fm_w == '{}' && empty_dic_fm_s == '{}'){
    document.getElementById("no_data_fm_o").innerHTML = "<h5>Finish Material Monthly Data</h5><br><div class='alert alert-light lead'><strong>Note:</strong> No Data Available</div>";
}
else{
    let currentDate = new Date();
    let cDay = currentDate.getDate()

    console.log(fm_w['01'],'############')
    if (fm_w['01']== undefined){
        fm_w['01'] = 0
        fm_s['01']=0
    }
// second graph
var speedCanvas = document.getElementById("speedChart1");

var dataFirst = {
    label: "Finish Material Weight",
    data: [fm_w['01'], fm_w['05'], fm_w['10'], fm_w['15'], fm_w['20'], fm_w['25'], fm_w['30']],
    lineTension: 0,
    fill: false,
    borderColor: "rgba(29, 53, 87)"
};

var dataSecond = {
    label: "Finish Material ScrapWeight",
    data: [fm_s['01'], fm_s['05'], fm_s['10'], fm_s['15'], fm_s['20'], fm_s['25'], fm_s['30']],
    lineTension: 0,
    fill: false,
    borderColor: "rgba(230, 57, 70)"
};

var speedData = {
labels: ["1", "5", "10", "15", "20", "25", "30"],
datasets: [dataFirst, dataSecond]
};

var chartOptions = {
legend: {
    display: true,
    position: 'top',
    labels: {
    boxWidth: 80,
    fontColor: 'black'
    }
}
};

var lineChart = new Chart(speedCanvas, {
type: 'line',
data: speedData,
options: chartOptions
});
}