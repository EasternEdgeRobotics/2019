var GRAPH_MAX_DATA = 200;

class Graph{
    constructor(id, canvasID, color = "#ffffff"){
        var numOfLines = 1;
        let ctx = document.getElementById(canvasID).getContext("2d");
        
        this.color = color;
        this._id = id;
        this._data = [];
        this._chart = new Chart(ctx,
        {
            type: 'line',
            data: {
                labels: [],
                datasets:[]
            },
            options:{
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true,
                            max: 50,
                            fontColor: color
                        },
                        gridLines: {
                            //display: false,
                            color: color,
                        },
                        scaleLabel:{
                            display: false
                        }
                    }],
                    xAxes: [{
                        gridLines: {
                            display: false,
                        },
                        scaleLabel:{
                            display: false
                        }
                    }]
                },
                animation: false,
                // responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                tooltips: {
                    enabled: false
                }
            }
            
        });

        for(let i = 0 ; i < numOfLines ; i++){
            this._chart.data.datasets.push({
                label: "",
                data: [],
                pointRadius: 0,
                borderColor: this.color,
                borderWidth: 5,
                fill: false
            });
            this._chart.update();
        }
    }

    get id(){
        return this._id;
    }

    addData(num){
        if(this._chart.data.datasets[0].data.length >= GRAPH_MAX_DATA){
            this._chart.data.datasets[0].data.shift();
            this._chart.data.labels.shift();
        }
        this._chart.data.datasets[0].data.push(num);
        this._chart.data.labels.push("");
        
        this._chart.update();
    }
}