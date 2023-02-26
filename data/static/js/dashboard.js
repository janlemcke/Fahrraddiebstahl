function drawComparisonLines(data) {
    let graphGradient = document.getElementById("performaneLine").getContext('2d');
    let graphGradient2 = document.getElementById("performaneLine").getContext('2d');
    const chart = Chart.getChart(graphGradient);
    if (chart) {
        chart.destroy();
    }
    let saleGradientBg = graphGradient.createLinearGradient(5, 0, 5, 100);
    saleGradientBg.addColorStop(0, 'rgba(26, 115, 232, 0.18)');
    saleGradientBg.addColorStop(1, 'rgba(26, 115, 232, 0.02)');
    let saleGradientBg2 = graphGradient2.createLinearGradient(100, 0, 50, 150);
    saleGradientBg2.addColorStop(0, 'rgba(0, 208, 255, 0.19)');
    saleGradientBg2.addColorStop(1, 'rgba(0, 208, 255, 0.03)');
    const comparisonData = {
        labels: ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
        datasets: [{
            label: 'Aktuelle Woche',
            data: data["last_data"],
            backgroundColor: saleGradientBg,
            borderColor: '#1F3BB3',
            borderWidth: 1.5,
            fill: true,
            pointBorderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 2,
            pointBackgroundColor: '#1F3BB3',
            pointBorderColor: '#fff',
        }, {
            label: 'Letzte Woche',
            data: data["current_data"],
            backgroundColor: saleGradientBg2,
            borderColor: '#52CDFF',
            borderWidth: 1.5,
            fill: true,
            pointBorderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 2,
            pointBackgroundColor: '#52CDFF',
            pointBorderColor: '#fff',
        }]
    };
    const comparisonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    display: true,
                    drawBorder: false,
                    color: "#F0F0F0",
                    zeroLineColor: '#F0F0F0',
                },
                ticks: {
                    count: 5,
                    callback: function(value, index, ticks) {
                        return Chart.Ticks.formatters.numeric.apply(this, [value, index, ticks]) + " €";
                    }
                }
            },
            x: {
                grid: {
                    display: false,
                    drawBorder: false,
                },
            },
        },
        elements: {
            line: {
                // makes line curvy
                tension: 0.4,
            }
        },
        plugins: {
            legend: false,
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.parsed.y + " €";
                    }
                }
            }
        }
    };
    new Chart(graphGradient, {
        type: 'line',
        data: comparisonData,
        options: comparisonOptions
    });

    document.getElementById("damagePerHourCurrentLabel").textContent = data["labels"][0];
    document.getElementById("damagePerHourLastLabel").textContent = data["labels"][1];
}

function drawDamageValuePerHourLines(data) {
    let graphGradient = document.getElementById("damageValuePerHour").getContext('2d');
    let graphGradient2 = document.getElementById("damageValuePerHour").getContext('2d');
    const chart = Chart.getChart(graphGradient);
    if (chart) {
        chart.destroy();
    }
    let saleGradientBg = graphGradient.createLinearGradient(5, 0, 5, 100);
    saleGradientBg.addColorStop(0, 'rgba(26, 115, 232, 0.18)');
    saleGradientBg.addColorStop(1, 'rgba(26, 115, 232, 0.02)');
    let saleGradientBg2 = graphGradient2.createLinearGradient(100, 0, 50, 150);
    saleGradientBg2.addColorStop(0, 'rgba(0, 208, 255, 0.19)');
    saleGradientBg2.addColorStop(1, 'rgba(0, 208, 255, 0.03)');

    const dataToPlot = {
        labels: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"],
        datasets: [{
            label: 'Aktuelle Woche',
            data: data["last_data"],
            backgroundColor: saleGradientBg,
            borderColor: '#1F3BB3',
            borderWidth: 1.5,
            fill:true,
            pointBorderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 2,
            pointBackgroundColor: '#1F3BB3',
            pointBorderColor: '#fff',
        }, {
            label: 'Letzte Woche',
            data: data["current_data"],
            backgroundColor: saleGradientBg2,
            borderColor:'#52CDFF',
            borderWidth: 1.5,
            fill:true,
            pointBorderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 2,
            pointBackgroundColor: '#52CDFF',
            pointBorderColor: '#fff',
        }]
    };
    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    display: true,
                    drawBorder: false,
                    color: "#F0F0F0",
                    zeroLineColor: '#F0F0F0',
                },
                ticks: {
                    count: 5,
                    callback: function(value, index, ticks) {
                        return Chart.Ticks.formatters.numeric.apply(this, [value, index, ticks]) + " €";
                    }
                }
            },
            x: {
                grid: {
                    display: false,
                    drawBorder: false,
                },
            },
        },
        elements: {
            line: {
                // makes line curvy
                tension: 0.4,
            }
        },
        plugins: {
            legend: false,
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.parsed.y + " €";
                    }
                }
            }
        }
    };
    new Chart(graphGradient, {
        type: 'line',
        data: dataToPlot,
        options: options,
    });

    document.getElementById("damagePerHourCurrentLabel").textContent = data["labels"][0];
    document.getElementById("damagePerHourLastLabel").textContent = data["labels"][1];
}

function onDateChangeDamagePerHour(select_element) {
    const comparison_type = select_element.value;
    fetch('/api/damageValuePerHour/' + comparison_type)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            drawDamageValuePerHourLines(data);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function onDateChangeDamageComparison(select_element) {
    const comparison_type = select_element.value;
    fetch('/api/damageComparison/' + comparison_type)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            drawComparisonLines(data);
        })
        .catch(function (error) {
            console.log(error);
        });
}

