create_chart_top(1,{{product_type.pk}});

function create_chart_top(day,pk){
    $.ajax({
        url:"{% url 'create-chart-top' %}",
        type:"POST",
        data:{
        day: day,
        pk: pk
        },
        success:function(data){
            if(data){
                    labels_x = [];
                    info_chart = [];
                    $.each(data.msg,function(index, val){
                        price_all = val['price'];
                        info_chart.push(price_all);
                        weight_all = val['weight']+' کیلوگرم ';
                        labels_x.push(weight_all);
                        });
                    var esm = "onedayprice"+day;
                    var element = document.getElementById(esm);
                    element.height = 300;
                    new Chart(element,{
                        type: "line",
                        data:{
                            labels: labels_x,
                            datasets: [{
                                label: {{product_type.pk}},
                                borderColor: "rgba(113, 76, 190, 0.9)",
                                borderWidth: "1",
                                backgroundColor: "rgba(113, 76, 190, 0.5)",
                                data: info_chart
                            }]
                        },
                        options:{
                            responsive: !0,
                            maintainAspectRatio: !1,
                            tooltips: {mode: "index", intersect: !1},
                            hover: {mode: "nearest", intersect: !0},
                            scales: {
                                xAxes: [{ticks: {fontColor: "#77778e"}, gridLines: {color: "rgba(119, 119, 142, 0.2)"}}],
                                yAxes: [{
                                    ticks: {beginAtZero: !0, fontColor: "#77778e"},
                                    gridLines: {color: "rgba(119, 119, 142, 0.2)"}
                                }]
                            },
                            legend: {labels: {fontColor: "#77778e"}}
                        }
                    })
            }else{
                alert("2")
            }
                    alert(data.result_amar);
                    if(data.result_amar) {
                        $('#price_avg').html('');
                        $('#price_max').html('');
                        $('#price_min').html('');
                        $('#bazar_count').html('');
                        $('#product_type_name').html('');
                        $('#price_avg').html(data.result_amar[0]);
                        $('#price_max').html(data.result_amar[1]);
                        $('#price_min').html(data.result_amar[2]);
                        $('#bazar_count').html(data.result_amar[3]);
                        $('#product_type_name').html(data.result_amar[4]);
                    }
        }
    })
}





