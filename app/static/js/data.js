var x = [];
var y = [];
var chart_data = {
    labels: x,
    datasets: []
};
var progress = document.getElementById('progress_data');
var chartColors= new Array('rgb(255, 159, 64)','rgb(153, 102, 255)','rgb(75, 192, 192)','rgb(255, 99, 132)','rgb(255, 205, 86)','rgb(54, 162, 235)','rgb(201, 203, 207)'); 

var options = {
    maintainAspectRatio: false,
    scales: {
        xAxes: [{
            display: true,
            scaleLabel: {
                display: true,
                labelString: 'DB-Hz'
            },
            gridLines: {
                display: false
            }
        }],
        yAxes: [{
            display: true,
            scaleLabel: {
                display: true,
                labelString: 'V-m/s'
            }

        }]
    },
    title: {
        display: true,
        text: 'Analysis - FFT Example'
    },
};
var animation = {
    duration: 2000,
    onProgress: function (animation) {
        progress.value = animation.currentStep / animation.numSteps;
    },
    onComplete: function () {
        window.setTimeout(function () {
            progress.value = 0;
        }, 2000);
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
    var data = {
        label: 'Original Signal Data',
        borderColor: chartColors[4],
        backgroundColor: chartColors[4],
        fill: false,

        data: y
    };
    chart_data['datasets'] = [data];
    if (!progress.value)
        Chart.Line('canvas_data', {
            options: options,
            data: chart_data
        }
        );
};
var data_init = function () {
    $.post("{{ url_for('data.index') }}", {

    }).done(function (response) {
        x = response['x'];
        y = response['y'];

        chart_data['labels'] = x;
        dash_init();
    }).fail(function () {

    });
}