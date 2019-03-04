class Graph{
    constructor(id, canvasID, color = "#ffffff", max = 100, labels = []){
        let ctx = document.getElementById(canvasID).getContext("2d");

        this.color = color;
        this._id = id;
        this._data = [];
        this._max = max;
        this._function = function(){};
        this._chart = new Chart(ctx,
        {
            type: 'line',
            data: {
                labels: labels,
                datasets: []
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
                animation:{
                    duration: 0
                },
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

        /*for(let i = 0 ; i < numOfLines ; i++){
            this._chart.data.datasets.push({
                label: "",
                data: [],
                pointRadius: 0,
                borderColor: this.color,
                borderWidth: 5,
                fill: false
            });
            this._chart.update();
        }*/
    }

    get id(){
        return this._id;
    }

    line(lineObj){
        this._chart.data.datasets.push(lineObj);

        this._chart.update();
        return this;
    }

    maxPoints(max){
        if(max == undefined)
            return this._max;
        this._max = max;
        return this;
    }

    run(f){
        if(f instanceof Function){
            this._function = f;
            this._function();
        }
        return this;
    }

    delete(f){
        if(f instanceof Function){
            this._delete = f;
        }else if(f == undefined && this._delete instanceof Function){
            this._delete();
        }
        return this;
    }

    addData(num, label, graph){
        if(this._chart.data.datasets[graph].data.length >= this._max){
            this._chart.data.datasets[graph].data.shift();
            this._chart.data.labels.shift();
        }
        this._chart.data.datasets[graph].data.push(num);
        this._chart.data.labels.push(label);

        this._chart.update();
    }
}