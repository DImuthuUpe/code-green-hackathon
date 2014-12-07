// Placeholder for Global Dashboard charts.
$( document ).ready(function() {
	
	
	var PUBNUB_api = PUBNUB.init({
          publish_key: 'pub-c-55cf3b7d-b27b-478a-99f3-158762ffcf86',
          subscribe_key: 'sub-c-1c9e1394-7a15-11e4-82cc-02ee2ddab7fe'
    });
        
    PUBNUB_api.subscribe({
        channel: 'codegreen_channel',
        message: function(m){
            console.log(m);
            var msg = m.country + " saved "+m.amount +" kg amount of Carbon";
            var newMsg = '<li style="height:15px:">'+msg+'</li>'
            var prevHtml =$('#notification_ul').html();
            $('#notification_ul').html(prevHtml+newMsg);
        }
    });
	
	
	var country_carbon_debit_chart = new CanvasJS.Chart("chart-01",
    {
       data: [

        {
            dataPoints: [
                { x: 10, y: 297571, label: "Venezuela"},
                { x: 20, y: 267017,  label: "Saudi" },
                { x: 30, y: 175200,  label: "Canada"},
                { x: 40, y: 154580,  label: "Iran"},
                { x: 50, y: 116000,  label: "Russia"},
                { x: 60, y: 97800, label: "UAE"},
                { x: 70, y: 20682,  label: "US"},
                { x: 80, y: 20350,  label: "China"}
            ]
        }
      ]
    });

    country_carbon_debit_chart.render();
    
    draw_user_action_graph('http://udkkb47b1650.dimuthuupe.koding.io','Cookie1');
    draw_user_carbon_save_graph('http://udkkb47b1650.dimuthuupe.koding.io','Cookie1');
    draw_country_carbon_save_graph('http://udkkb47b1650.dimuthuupe.koding.io','Cookie1');
    
    
    
    
});


function draw_user_action_graph(server,cookie){
    $.ajax({
        contentType: "application/json; charset=utf-8",
                
        data: JSON.stringify({'registration':'Cookie1'}), //get the cookie from browse
        url: server+":8081/user_actions?registration="+cookie,
        type: "GET",
        dataType: 'json',
        success: function (result) {
            var actionResult =[];
            for (var i = 0; i < result.actions.length; i++) {
                var tuple={};
                tuple.y= result.actions[i].count;
                tuple.legendText=result.actions[i].action;
                tuple.indexLabel=result.actions[i].action;
                actionResult[i] = tuple;
                //{  y: 4181563, legendText:"Food", indexLabel: "Food" }
            }
            
            var user_action_pichart = new CanvasJS.Chart("chart-02",
            {
                legend:{
                    verticalAlign: "bottom",
                    horizontalAlign: "center"
                },
                data: [
                {        
                    indexLabelFontSize: 20,
                    indexLabelFontFamily: "Monospace",       
                    indexLabelFontColor: "darkgrey", 
                    indexLabelLineColor: "darkgrey",        
                    indexLabelPlacement: "outside",
                    type: "pie",       
                    showInLegend: true,
                    toolTipContent: "{y} - <strong>#percent%</strong>",
                    dataPoints: actionResult
                }
                ]
            });
            user_action_pichart.render();
            
            console.log(actionResult);
        }
    });
}

function draw_user_carbon_save_graph(server,cookie){
    $.ajax({
        contentType: "application/json; charset=utf-8",
                
        data: JSON.stringify({'registration':'Cookie1'}), //get the cookie from browse
        url: server+":8081/user_time_series?registration="+cookie,
        type: "GET",
        dataType: 'json',
        success: function (result) {
            var consumption =[];
            //console.log(result);
            for (var i = 0; i < result.credit.length; i++) {
                var tuple = {};
                var dates = (result.credit[i].date).split("-");
                tuple.x = new Date(dates[0],dates[1]-1,dates[2]);
                tuple.y = result.debit[i].value-result.credit[i].value;
                consumption[i]=tuple;
                //console.log(result.credit[i].date);
            }
            //console.log(consumption);
            var user_carbon_save_graph = new CanvasJS.Chart("chart-03",
            {

               data: [
                    {        
                    type: "splineArea",
                    color:"#881515",
                    dataPoints: consumption
                    }
              ]
            });
            user_carbon_save_graph.render();
        }
    });
}

function draw_country_carbon_save_graph(server,cookie){
    $.ajax({
        contentType: "application/json; charset=utf-8",
                
        data: JSON.stringify({'registration':'Cookie1'}), //get the cookie from browse
        url: server+":8081/country_time_series?registration="+cookie,
        type: "GET",
        dataType: 'json',
        success: function (result) {
            var consumption =[];
            //console.log(result);
            for (var i = 0; i < result.credit.length; i++) {
                var tuple = {};
                var dates = (result.credit[i].date).split("-");
                tuple.x = new Date(dates[0],dates[1]-1,dates[2]);
                tuple.y = result.debit[i].value-result.credit[i].value;
                consumption[i]=tuple;
                //console.log(result.credit[i].date);
            }
            //console.log(consumption);
            var country_carbon_save_graph = new CanvasJS.Chart("chart-04",
            {

                data: [
                    {        
                    type: "splineArea",
                    color:"#0E75C3",
                    dataPoints:consumption
                    }
                    
                ]
            });
            country_carbon_save_graph.render();
        }
    });
}
