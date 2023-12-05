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
                    forecastTimeframe: document.getElementById("forecastTimeframe").value
                }
            )
                .done(function (data, status) {
                    let forecastData = JSON.parse(data)
                    ForecastProfile.staticVariables(forecastData)
                    ForecastProfile.chart(forecastData)
                })
                .fail(function (data, status) {
                    let forecastDisplay = document.getElementById("forecastDisplay");
                    forecastDisplay.innerHTML = data.status + "<br>" + data.statusText + "<br>" + data.responseText
                });
        }, false);
    },
    setupRawDataFetch() {
        document.getElementById("viewRawForecastData").addEventListener("click", function () {
            window.location.href = "/forecast_data"
        }, false);
    },
    staticVariables: function (forecastData) {
        let forecastObjDictArray = forecastData[1]
        let staticVariables = document.getElementById("forecastObjArrayStaticVariables");
        staticVariables.innerHTML = ""
        for (let e of forecastObjDictArray) {
            let a = document.createElement("a")
            a.setAttribute("class", "w3-bar-item")
            let aHTML = "";
            for (let [key, value] of Object.entries(e)) {
                if (key !== "data") {
                    aHTML += "<br>" + key + ": " + value
                }
            }
            a.innerHTML = aHTML
            staticVariables.appendChild(a)
        }
    },
    chart: function (forecastData) {
        am4core.useTheme(am4themes_animated);
        let forecastChartVariables = forecastData[0]
        let forecastObjDictArray = forecastData[1]
        let chartTitle = forecastChartVariables["title"]
        let chartDisplayType = parseInt(document.getElementById("forecastDisplayType").value);
        let chartDivElementIds = ForecastProfile.createChartDivElements(forecastObjDictArray.length)

        let mergedData = ForecastProfile.spliceForecastArrayData(forecastChartVariables, forecastObjDictArray)
        let xAxisTitleText = forecastChartVariables["xAxisTitleText"]
        let yAxisTitleText = forecastChartVariables["yAxisTitleText"]
        let chartParent = ForecastProfile.createXYValueAxisChart(chartDivElementIds[0], mergedData, xAxisTitleText, yAxisTitleText)
        let chartParentTitle = chartParent.titles.create()
        chartParentTitle.text = chartTitle
        chartParent.legend = new am4charts.Legend();

        for (let [index, j] of forecastObjDictArray.entries()) {
            let lineSeriesValueX = forecastChartVariables["lineSeriesValueX"];
            let lineSeriesValueY = j["lineSeriesValueY"]
            let lineSeriesName = j["lineSeriesName"]
            ForecastProfile.createChartLineSeries(chartParent, lineSeriesValueX, lineSeriesValueY, lineSeriesName, chartDisplayType)
            if (forecastObjDictArray.length > 1) {
                let jData = j["data"]
                let jLineSeriesValueX = lineSeriesValueX
                let jLineSeriesValueY = lineSeriesValueY
                let jLineSeriesName = lineSeriesName
                let chartJ = ForecastProfile.createXYValueAxisChart(chartDivElementIds[index + 1], jData, xAxisTitleText, yAxisTitleText)
                ForecastProfile.createChartLineSeries(chartJ, jLineSeriesValueX, jLineSeriesValueY, jLineSeriesName, chartDisplayType)
                let chartJTitle = chartJ.titles.create()
                chartJTitle.text = chartTitle
                chartJ.legend = new am4charts.Legend()
            }
        }
    },
    createXYValueAxisChart: function (divName, data, xAxisTitleText, yAxisTitleText) {
        let chart = am4core.create(divName, am4charts.XYChart);
        chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
        let xAxis = chart.xAxes.push(new am4charts.ValueAxis());
        let yAxis = chart.yAxes.push(new am4charts.ValueAxis());

        chart.data = data
        xAxis.title.text = xAxisTitleText;
        yAxis.title.text = yAxisTitleText;
        return chart;
    },
    createChartLineSeries: function (chart, lineSeriesValueX, lineSeriesValueY, lineSeriesName, chartDisplayType) {
        var lineSeries = chart.series.push(new am4charts.LineSeries());
        lineSeries.dataFields.valueX = lineSeriesValueX;
        lineSeries.dataFields.valueY = lineSeriesValueY;
        if (chartDisplayType === 0) {
            lineSeries.fillOpacity = 0.3;
            lineSeries.fill = am4core.color(ForecastProfile.colorKey.nextHexColor())
            lineSeries.stroke = am4core.color(ForecastProfile.colorKey.nextHexColor())
            lineSeries.strokeWidth = 1;
        } else if (chartDisplayType === 1) {
            lineSeries.stroke = am4core.color(ForecastProfile.colorKey.nextHexColor())
            lineSeries.strokeWidth = 1;
        } else if (chartDisplayType === 2) {
            let nextHextColor = ForecastProfile.colorKey.nextHexColor()
            lineSeries.fillOpacity = 0.3;
            lineSeries.fill = am4core.color(nextHextColor)
            lineSeries.stroke = am4core.color(nextHextColor)
            lineSeries.strokeWidth = 1;
        }
        lineSeries.name = lineSeriesName;
    },
    createChartDivElements: function (length) {
        let o = [];
        let columnCount = 2;
        let cellCount = length;

        let divElements = document.getElementById("forecastChartDivRows");
        divElements.innerHTML = "";

        let parentChartDiv = document.createElement("div")
        parentChartDiv.id = "parentForecastChartDiv"
        parentChartDiv.style.height = "600px"
        parentChartDiv.style.width = "100%"
        divElements.appendChild(parentChartDiv)
        o.push(parentChartDiv.id)
        if (cellCount > 1) {
            for (let i = 0; i < cellCount; i = i + columnCount) {

                if (i % columnCount === 0) {
                    let y = document.createElement("div");
                    y.id = "dashDivRow" + i;
                    y.classList = "w3-row";
                    divElements.appendChild(y);

                    for (let j = 0; j < columnCount; j++) {
                        let u = document.createElement("div");
                        u.classList = "w3-col s" + 12 / columnCount + " w3-center";
                        u.id = "forecastChartDivCol" + (i + j);
                        u.style.height = "600px"
                        y.appendChild(u);
                        o.push(u.id);
                    }
                }
            }
        }
        return o;
    },
    spliceForecastArrayData: function (chartVariables, objDictArray) {
        let data = []
        let axisDataPoints = parseInt(chartVariables["axis_data_points"])
        let lineSeriesValueX = chartVariables["lineSeriesValueX"]
        for (let i = 0; i < axisDataPoints; i++) {
            let dataItem = {}
            dataItem[lineSeriesValueX] = i;
            for (let j of objDictArray) {
                let lineSeriesValueY = j["lineSeriesValueY"]
                dataItem[lineSeriesValueY] = j["data"][i][lineSeriesValueY]
            }
            data.push(dataItem)
        }
        return data;
    },
    colorKey: {
        key: [
            /*{name: "Yellow", hexValue: "#FCE883"},*/
            {name: "Lime", hexValue: "#00FF00"},
            {name: "Purple", hexValue: "#800080"},
            {name: "Magenta", hexValue: "#F664AF"},
            {name: "Green", hexValue: "#1CAC78"},
            {name: "Red", hexValue: "#EE204D"},
            {name: "Cyan", hexValue: "#00D7AF"},
            {name: "DarkOrchid", hexValue: "#9932CC"},
            {name: "DarkMagenta", hexValue: "#8B008B"}
        ],
        counterKey: [],
        nextHexColor: function () {
            let keyIndex;
            let color;
            let hexVal;
            if (this.counterKey.length === 0) {
                this.counterKey = this.key.slice()
            }
            keyIndex = parseInt(Math.random() * this.counterKey.length)
            color = this.counterKey.splice(keyIndex, 1)[0]
            hexVal = color.hexValue
            return hexVal
        }
    }
}

ForecastProfile.init()