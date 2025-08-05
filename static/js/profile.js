let Profile = {
    init: function () {
        this.profile();
    },
    profile: function () {
        this.setupSimulate()
        this.setupRawDataFetch()
    },
    setupSimulate: function () {
        document.getElementById("simulate").addEventListener("click", function () {
            $.post("/simulate",
                {
                    baseModel: document.getElementById("baseModel").value,
                    waveform: document.getElementById("waveform").value,
                    limitBounds: document.getElementById("limitBounds").value
                }
            )
                .done(function (data, status) {
                    data = JSON.parse(data)
                    Profile.staticVariables(data)
                    Profile.chart(data)
                })
                .fail(function (data, status) {
                    let display = document.getElementById("display");
                    display.innerHTML = data.status + "<br>" + data.statusText + "<br>" + data.responseText
                });
        }, false);
    },
    setupRawDataFetch: function () {
        document.getElementById("viewRawData").addEventListener("click", function () {
            window.location.href = "/data"
        }, false);
    },
    staticVariables: function (data) {
        let objDictArray = data[1]
        let staticVariables = document.getElementById("staticVariables");
        staticVariables.innerHTML = ""
        for (let e of objDictArray) {
            let a = document.createElement("a")
            a.setAttribute("class", "w3-bar-item")
            let aHTML = "";
            for (let [key, value] of Object.entries(e)) {
                if (key !== "data" && key!== "wave" && key!== "fft_shifted" && key!== "freq_shifted") {
                    if (typeof(value) === "object"){
                        value = JSON.stringify(value)
                    }
                    aHTML += "<br>" + key + ": " + value
                }
            }
            a.innerHTML = aHTML
            staticVariables.appendChild(a)
        }
    },
    chart: function (data) {
        am4core.useTheme(am4themes_animated);
        let chartVariables = data[0]
        let objDictArray = data[1]
        let spliceData = data[2][0]
        let chartTitle = chartVariables["title"]
        let chartDisplayType = parseInt(document.getElementById("displayType").value);
        let chartDivElementIds = Profile.chartUtils.createChartDivElements(objDictArray.length)

        let xAxisTitleText = chartVariables["xAxisTitleText"]
        let yAxisTitleText = chartVariables["yAxisTitleText"]
        let lineSeriesValueX = chartVariables["lineSeriesValueX"];

        let chartParent;
        if (spliceData) {
            let splicedData = Profile.dataUtils.spliceData(chartVariables, objDictArray)
            chartParent = Profile.chartUtils.createXYValueAxisChart(chartDivElementIds[0], chartTitle, splicedData, xAxisTitleText, yAxisTitleText)
        }else{
            document.getElementById(chartDivElementIds[0]).style.height = "10px"
        }

        for (let [index, j] of objDictArray.entries()) {

            let jData = j["data"]
            let jTitle = j["title"]
            let jXAxisTitleText = j["xAxisTitleText"]
            let jYAxisTitleText = j["yAxisTitleText"]
            let jLineSeriesValueX = j["lineSeriesValueX"];
            let jLineSeriesValueY = j["lineSeriesValueY"]
            let jLineSeriesName = j["lineSeriesName"]
             if (spliceData){
                 Profile.chartUtils.createChartLineSeries(chartParent, lineSeriesValueX, jLineSeriesValueY, jLineSeriesName, chartDisplayType)
            }
            let chartJ = Profile.chartUtils.createXYValueAxisChart(chartDivElementIds[index + 1], jTitle, jData, jXAxisTitleText, jYAxisTitleText)
            Profile.chartUtils.createChartLineSeries(chartJ, jLineSeriesValueX, jLineSeriesValueY, jLineSeriesName, chartDisplayType)

        }
    },
    chartUtils: {
        createXYValueAxisChart: function (divName, chartTitle, data, xAxisTitleText, yAxisTitleText) {
            let chart = am4core.create(divName, am4charts.XYChart);
            chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

            let xAxis = chart.xAxes.push(new am4charts.ValueAxis());
            let yAxis = chart.yAxes.push(new am4charts.ValueAxis());

            xAxis.title.text = xAxisTitleText;
            yAxis.title.text = yAxisTitleText;

            let o = chart.titles.create()
            o.text = chartTitle
            chart.data = data
            chart.legend = new am4charts.Legend();
            return chart;
        },
        createChartLineSeries: function (chart, lineSeriesValueX, lineSeriesValueY, lineSeriesName, chartDisplayType) {
            var lineSeries = chart.series.push(new am4charts.LineSeries());
            lineSeries.dataFields.valueX = lineSeriesValueX;
            lineSeries.dataFields.valueY = lineSeriesValueY;
            lineSeries.name = lineSeriesName;
            if (chartDisplayType === 0) {
                lineSeries.fillOpacity = 0.3;
                lineSeries.fill = am4core.color(Profile.colorKey.nextHexColor())
                lineSeries.stroke = am4core.color(Profile.colorKey.nextHexColor())
                lineSeries.strokeWidth = 1;
            } else if (chartDisplayType === 1) {
                lineSeries.stroke = am4core.color(Profile.colorKey.nextHexColor())
                lineSeries.strokeWidth = 1;
            } else if (chartDisplayType === 2) {
                let nextHextColor = Profile.colorKey.nextHexColor()
                lineSeries.fillOpacity = 0.3;
                lineSeries.fill = am4core.color(nextHextColor)
                lineSeries.stroke = am4core.color(nextHextColor)
                lineSeries.strokeWidth = 1;
            }
        },
        createChartDivElements: function (length) {
            let o = [];
            let columnCount = 2;
            let cellCount = length;

            let divElements = document.getElementById("chartDivRows");
            divElements.innerHTML = "";

            let parentChartDiv = document.createElement("div")
            parentChartDiv.id = "parentChartDiv"
            parentChartDiv.style.height = "600px"
            parentChartDiv.style.width = "100%"
            divElements.appendChild(parentChartDiv)
            o.push(parentChartDiv.id)
            if (cellCount > 1) {
                for (let i = 0; i < cellCount; i = i + columnCount) {

                    if (i % columnCount === 0) {
                        let y = document.createElement("div");
                        y.id = "chartDivRow" + i;
                        y.classList = "w3-row";
                        divElements.appendChild(y);

                        for (let j = 0; j < columnCount; j++) {
                            let u = document.createElement("div");
                            u.classList = "w3-col s" + 12 / columnCount + " w3-center";
                            u.id = "chartDivCol" + (i + j);
                            u.style.height = "600px"
                            y.appendChild(u);
                            o.push(u.id);
                        }
                    }
                }
            }
            return o;
        }
    },
    dataUtils: {
        spliceData: function (chartVariables, objDictArray) {
            let data = []
            let length = objDictArray[0]["data"].length
            let lineSeriesValueX = chartVariables["lineSeriesValueX"]
            for (let i = 0; i < length; i++) {
                let dataItem = {}
                dataItem[lineSeriesValueX] = objDictArray[0]["data"][i][lineSeriesValueX];
                for (let j of objDictArray) {
                    let lineSeriesValueY = j["lineSeriesValueY"]
                    dataItem[lineSeriesValueY] = j["data"][i][lineSeriesValueY]
                }
                data.push(dataItem)
            }
            return data;
        }
    },
    colorKey: {
        key: [
            {name: "Yellow", hexValue: "#FCE883"},
            {name: "Lime", hexValue: "#00FF00"},
            /*{name: "Purple", hexValue: "#800080"},*/
            /*{name: "Magenta", hexValue: "#F664AF"},*/
            /*{name: "Green", hexValue: "#1CAC78"},*/
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

Profile.init()