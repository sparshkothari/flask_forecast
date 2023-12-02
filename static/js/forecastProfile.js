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
                    forecastEnvironmentNumber: document.getElementById("forecastEnvironment").value,
                    forecastTimeframe: document.getElementById("forecastTimeframe").value
                }
            )
                .done(function (data, status) {
                    let forecastObjDictArray = JSON.parse(data)
                    ForecastProfile.staticVariables(forecastObjDictArray)
                    ForecastProfile.chart(forecastObjDictArray)
                })
                .fail(function (data, status) {
                    let forecastDisplay = document.getElementById("forecastDisplay");
                    forecastDisplay.innerHTML = data.status + "<br>" + data.statusText + "<br>" + data.responseText
                });
        }, false);
    },
    setupRawDataFetch() {
        document.getElementById("viewRawForecastData").addEventListener("click", function () {
            window.location.href = "/forecast_obj_dict_array"
        }, false);
    },
    staticVariables: function (forecastObjDictArray) {
        let staticVariables = document.getElementById("forecastObjArrayStaticVariables");
        staticVariables.innerHTML = ""
        for (let e of forecastObjDictArray) {
            let a = document.createElement("a")
            a.setAttribute("class", "w3-bar-item")
            let aHTML = "";
            for (let [key, value] of Object.entries(e)) {
                if (key !== "water_reserves_data") {
                    aHTML += "<br>" + key + ": " + value
                }
            }
            a.innerHTML = aHTML
            staticVariables.appendChild(a)
        }
    },
    chart: function (forecastObjDictArray) {

        am4core.useTheme(am4themes_animated);

        var chart = am4core.create("forecastChartDiv", am4charts.XYChart);
        chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
        let data = []
        let numberOfDays = parseInt(forecastObjDictArray[0]["duration_number_of_days"])
        for (let i = 0; i < numberOfDays; i++) {
            let dataItem = {}
            dataItem["day"] = i;
            for (let j of forecastObjDictArray) {
                let forecast_data_key = j["forecast_data_key"]
                dataItem[forecast_data_key] = j["water_reserves_data"][i][forecast_data_key]
            }
            data.push(dataItem)
        }
        chart.data = data

        let xAxis = chart.xAxes.push(new am4charts.ValueAxis());
        let yAxis = chart.yAxes.push(new am4charts.ValueAxis());

        xAxis.title.text = "# of Days";
        yAxis.title.text = "Water (cubic inches)";

        for (let j of forecastObjDictArray) {
            let forecast_data_key = j["forecast_data_key"]
            let forecast_environment = j["forecast_environment"]
            var waterSeries = chart.series.push(new am4charts.LineSeries());
            waterSeries.dataFields.valueY = forecast_data_key;
            waterSeries.dataFields.valueX = "day";
            waterSeries.fillOpacity = 0.3;
            waterSeries.fill = chart.colors.next()
            waterSeries.stroke = chart.colors.next()
            waterSeries.name = forecast_environment;
        }


        chart.legend = new am4charts.Legend();
    }

}

ForecastProfile.init()