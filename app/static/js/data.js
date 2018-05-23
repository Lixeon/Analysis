var x = [];
var t=[];
var y1 = [];
var y2 = [];
var y1f = [];
var y2f = [];
var trigger_b  = true;
var chart_data = {
    labels: x,
    datasets: []
};
var progress = document.getElementById('progress_data');
var chartColors = new Array('rgb(54, 162, 235)', 'rgb(255, 205, 86)','rgb(255, 159, 64)','rgb(153, 102, 255)','rgb(75, 192, 192)','rgb(255, 99, 132)','rgb(201, 203, 207)'); 

var options = {
    maintainAspectRatio: false,
    scales: {
        xAxes: [{
            display: true,
            scaleLabel: {
                display: true,
                labelString: 'f[Hz]'
            },
            distribution: 'series',
            ticks: {
                source: 'labels'
            },
            gridLines: {
                display: false
            },
        }],
        yAxes: [
            {
                display: true,
                position: 'left',
                id: 'speed-axis',
                scaleLabel: {
                    display: true,
                    labelString: 'speed[RPM]'
                },
            },
            {
                display: true,
                position: 'right',
                id: 'vibration-axis',
                scaleLabel: {
                    display: true,
                    labelString: 'vibration[mm/s^2]'
                },
                gridLines: {
                    drawOnChartArea: false, // only want the grid lines for one axis to show up
                },
            }]
    },
    title: {
        display: true,
        text: 'Analysis - FFT Example'
    },
};
var animation = {
    duration: 500,
    onProgress: function (animation) {
        progress.value = animation.currentStep / animation.numSteps;
        trigger_b=false;
    },
    onComplete: function () {
        window.setTimeout(function () {
            progress.value = 0;
            trigger_b = true;
        }, 500);
    }
};
var set_act=function($item){
    var nav_list=$('.cl');
    for(var i=0;i< nav_list.length;i++)
        if($(nav_list[i]).hasClass('active')){
                $(nav_list[i]).removeClass('active');
            break;
    }
    if($item.hasClass('cl') && !$item.hasClass('active') )
        $item.addClass('active');
};
var dash_init = function () {
    var data1 = {
        label: 'Speed Signal Data',
        borderColor: chartColors[0],
        backgroundColor: chartColors[0],
        fill: false,
        pointRadius: 0,
        lineTension: 0,
        borderWidth: 2,
        data: y1,
        yAxisID:'speed-axis',
    }; 
    var data2 = {
        label: 'Vibration Signal Data',
        borderColor: chartColors[1],
        backgroundColor: chartColors[1],
        fill: false,
        pointRadius: 0,
        lineTension: 0,
        borderWidth: 2,
        data: y2,
        yAxisID:'vibration-axis',
    }; 
    if (trigger_b ){
        chart_data['datasets'] = [data1,data2];
        Chart.Line('canvas_data', {
            options: options,
            data: chart_data
        }
        );
    };
    
};
