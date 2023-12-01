var WaterForecast = {
    init: function () {
        this.waterForecast();
    },
    waterForecast: function () {
        this.waterForecastSetupSimulateForecast()
        this.waterForecastSetupRawDataFetch()
    },
    waterForecastSetupSimulateForecast() {
        document.getElementById("simulateWaterForecast").addEventListener("click", function () {
            $.post("/simulate_water_forecast",
                {
                    waterForecastModel: document.getElementById("waterForecastModel").value,
                    waterForecastTimeframe: document.getElementById("waterForecastTimeframe").value

                }
            )
                .done(function (data, status) {
                    let waterForecastObjDict = JSON.parse(data)
                    WaterForecast.waterForecastObjStaticVariables(waterForecastObjDict)
                    WaterForecast.waterForecastObjGraph(waterForecastObjDict)
                })
                .fail(function (data, status) {
                    console.log(data)
                    console.log(status)
                    let waterForecastDisplay = document.getElementById("waterForecastDisplay");
                    waterForecastDisplay.innerHTML = data.status + "<br>" + data.statusText + "<br>" + data.responseText
                });
        }, false);
    },
    waterForecastSetupRawDataFetch() {
        document.getElementById("viewRawWaterForecastData").addEventListener("click", function () {
            window.location.href = "/water_forecast_obj_dict"
        }, false);
    },
    waterForecastObjStaticVariables: function (waterForecastObjDict) {
        let waterObjStaticVariables = document.getElementById("waterObjStaticVariables");

        /*Static Variables*/

        /*Title*/
        let tTitle = document.createElement("p")
        tTitle.setAttribute("style", "font-weight: bold;")
        tTitle.innerHTML = "static variables"

        /*Value*/
        let tValue = document.createElement("p")
        let tValueHTML = "";
        for (let [key, value] of Object.entries(waterForecastObjDict)) {
            if (key !== "water_reserves_data") {
                tValueHTML += "<br>" + key + ": " + value
            }
        }

        tValue.innerHTML = tValueHTML

        waterObjStaticVariables.innerHTML = ""
        waterObjStaticVariables.appendChild(tTitle)
        waterObjStaticVariables.appendChild(tValue)
    },
    waterForecastObjGraph: function (waterForecastObjDict) {

        am4core.useTheme(am4themes_animated);

        var chart = am4core.create("waterForecastChartDiv", am4charts.XYChart);
        chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
        chart.data = waterForecastObjDict["water_reserves_data"];

        let xAxis = chart.xAxes.push(new am4charts.ValueAxis());
        let yAxis = chart.yAxes.push(new am4charts.ValueAxis());

        xAxis.title.text = "# of Days";
        yAxis.title.text = "Water (cubic inches)";


        var series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.valueY = "water_reserves";
        series.dataFields.valueX = "day";
        series.name = "Water Collected";

        chart.legend = new am4charts.Legend();
    }

}

WaterForecast.init()