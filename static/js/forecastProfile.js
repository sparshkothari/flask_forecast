var ForecastProfile = {
    init: function () {
        this.forecastProfile();
    },
    forecastProfile: function () {
        this.setupSimulateForecast()
        this.setupRawDataFetch()
    },
    setupSimulateForecast() {
        document.getElementById("simulateForecast").addEventListener("click", function () {
            $.post("/simulate_forecast",
                {
                    forecastBaseModel: document.getElementById("forecastBaseModel").value,
                    forecastEnvironment: document.getElementById("forecastEnvironment").value,
                    forecastTimeframe: document.getElementById("forecastTimeframe").value
                }
            )
                .done(function (data, status) {
                    let forecastObjDict = JSON.parse(data)
                    ForecastProfile.staticVariables(forecastObjDict)
                    ForecastProfile.chart(forecastObjDict)
                })
                .fail(function (data, status) {
                    let forecastDisplay = document.getElementById("forecastDisplay");
                    forecastDisplay.innerHTML = data.status + "<br>" + data.statusText + "<br>" + data.responseText
                });
        }, false);
    },
    setupRawDataFetch() {
        document.getElementById("viewRawForecastData").addEventListener("click", function () {
            window.location.href = "/forecast_obj_dict"
        }, false);
    },
    staticVariables: function (forecastObjDict) {
        let staticVariables = document.getElementById("forecastObjStaticVariables");

        /*Static Variables*/

        /*Title*/
        let tTitle = document.createElement("p")
        tTitle.setAttribute("style", "font-weight: bold;")
        tTitle.innerHTML = "static variables"

        /*Value*/
        let tValue = document.createElement("p")
        let tValueHTML = "";
        for (let [key, value] of Object.entries(forecastObjDict)) {
            if (key !== "water_reserves_data") {
                tValueHTML += "<br>" + key + ": " + value
            }
        }

        tValue.innerHTML = tValueHTML

        staticVariables.innerHTML = ""
        staticVariables.appendChild(tTitle)
        staticVariables.appendChild(tValue)
    },
    chart: function (forecastObjDict) {

        am4core.useTheme(am4themes_animated);

        var chart = am4core.create("forecastChartDiv", am4charts.XYChart);
        chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
        chart.data = forecastObjDict["water_reserves_data"];

        let xAxis = chart.xAxes.push(new am4charts.ValueAxis());
        let yAxis = chart.yAxes.push(new am4charts.ValueAxis());

        xAxis.title.text = "# of Days";
        yAxis.title.text = "Water (cubic inches)";


        var waterSeries = chart.series.push(new am4charts.LineSeries());
        waterSeries.dataFields.valueY = "water_reserves";
        waterSeries.dataFields.valueX = "day";
        waterSeries.name = "Water Collected";

        chart.legend = new am4charts.Legend();
    }

}

ForecastProfile.init()