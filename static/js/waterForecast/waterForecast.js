var WaterForecast = {
    init: function () {
        this.waterForecast();
    },
    getWaterForecastObjLocalKey: function () {
        return "waterForecastObjDictString"
    },
    waterForecast: function () {
        document.getElementById("simulateWaterForecast").addEventListener("click", function () {
            $.post("/simulate_water_forecast",
                {
                    waterForecastModel: document.getElementById("waterForecastModel").value
                }
            )
                .done(function (data, status) {
                    console.log(data)
                })
                .fail(function () {
                    // window.location.href = "/view_error"
                });

            $.get("/water_forecast_obj_dict")
                .done(function (data, status) {
                    if (typeof (data) !== "string") {
                        data = JSON.stringify(data, null, 2);
                    }
                    localStorage.setItem(WaterForecast.getWaterForecastObjLocalKey(), data);
                })
                .fail(function () {
                    // window.location.href = "/view_error"
                });
            WaterForecast.waterForecastObjStaticVariables()
            WaterForecast.waterForecastObjGraph()
        }, false);

    },
    waterForecastObjStaticVariables: function () {
        let waterForecastObjDict = JSON.parse(localStorage.getItem(WaterForecast.getWaterForecastObjLocalKey()))
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
    waterForecastObjGraph: function () {
        let waterForecastObjDict = JSON.parse(localStorage.getItem(WaterForecast.getWaterForecastObjLocalKey()))

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