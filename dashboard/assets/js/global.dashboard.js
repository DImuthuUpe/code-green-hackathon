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
	
	
	
    
    draw_user_action_graph('http://umkkeb295ebf.madytyoo.koding.io','Cookie1');
    draw_user_carbon_save_graph('http://umkkeb295ebf.madytyoo.koding.io','Cookie1');
    draw_country_carbon_save_graph('http://umkkeb295ebf.madytyoo.koding.io','Cookie1');
    draw_country_savings('http://umkkeb295ebf.madytyoo.koding.io','Cookie1');
    
    
    
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
            
            //console.log(actionResult);
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

function draw_country_savings(server,cookie){
    $.ajax({
        contentType: "application/json; charset=utf-8",
                
        data: JSON.stringify({'registration':'Cookie1'}), //get the cookie from browse
        url: server+":8081/top_countries",
        type: "GET",
        dataType: 'json',
        success: function (result) {
            var set1 =[];
            var set2 =[];
            //console.log(result);
            // { x: 10, y: 297571, label: "Venezuela"}
            for (var i = 0; i < result.savings.length; i++) {
                var tuple1 = {};
                tuple1.x = (i+1)*1;
                tuple1.y = result.savings[i].savings;
                tuple1.label=result.savings[i].country;
                set1[i]=tuple1;
                
                var tuple2 = {};
                tuple2.x = (i+1)*1;
                tuple2.y = result.ratios[i].ratio;
                tuple2.label=result.ratios[i].country;
                set2[i]=tuple2;
                //console.log(result.credit[i].date);
            }
            
            
            
            var country_carbon_savings_chart = new CanvasJS.Chart("chart-01",
            {
                data: [
                    {
                        name: "Ratio (Carbon per capita / Average savings per person)",
                        showInLegend: "true",
                        dataPoints: set2
                    }
                ]
            });
        
            country_carbon_savings_chart.render();
            
            var country_carbon_savings_chart2 = new CanvasJS.Chart("chart-05",
            {
                data: [
                    {
                        name: "Total Carbon Savings",
                        showInLegend: "true",
                        dataPoints: set1
                    }
                ]
            });
        
            country_carbon_savings_chart2.render();
            
            
            
        }
    });
}
