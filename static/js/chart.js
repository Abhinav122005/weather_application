const canvas = document.getElementById("temperatureChart");

if (canvas) {
    const labels = JSON.parse(canvas.dataset.labels);
    const temperatures = JSON.parse(canvas.dataset.temperatures);

    // Dynamic color based on theme
    const isDarkMode = document.body.classList.contains("dark-mode");
    const gridColor = isDarkMode ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)";
    const textColor = isDarkMode ? "#f8fafc" : "#0f172a";

    const chartInstance = new Chart(canvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Temperature (°C/°F)",
                data: temperatures,
                borderColor: "#6366f1",
                backgroundColor: "rgba(99, 102, 241, 0.2)",
                borderWidth: 3,
                tension: 0.4, // Smooth curves
                fill: true,
                pointBackgroundColor: "#ffffff",
                pointBorderColor: "#6366f1",
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: textColor, font: { family: "'Outfit', sans-serif", size: 14 } }
                }
            },
            scales: {
                x: {
                    grid: { color: gridColor, drawBorder: false },
                    ticks: { color: textColor, font: { family: "'Outfit', sans-serif" } }
                },
                y: {
                    grid: { color: gridColor, drawBorder: false },
                    ticks: { color: textColor, font: { family: "'Outfit', sans-serif" } }
                }
            }
        }
    });

    // Observer to update chart colors when theme changes
    const observer = new MutationObserver(() => {
        const dark = document.body.classList.contains("dark-mode");
        const newGrid = dark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)";
        const newText = dark ? "#f8fafc" : "#0f172a";
        
        chartInstance.options.plugins.legend.labels.color = newText;
        chartInstance.options.scales.x.grid.color = newGrid;
        chartInstance.options.scales.x.ticks.color = newText;
        chartInstance.options.scales.y.grid.color = newGrid;
        chartInstance.options.scales.y.ticks.color = newText;
        chartInstance.update();
    });
    observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
}

/* ================= NEW HIGHLIGHT CHARTS ================= */

// 1. Chances of Rain Chart
const rainCanvas = document.getElementById("rainChart");
if (rainCanvas) {
    const labels = JSON.parse(rainCanvas.dataset.labels || "[]");
    const data = JSON.parse(rainCanvas.dataset.data || "[]");
    
    const isDarkMode = document.body.classList.contains("dark-mode");
    const textColor = isDarkMode ? "#94a3b8" : "#64748b";

    new Chart(rainCanvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Rain %",
                data: data,
                backgroundColor: "#10b981", // Emerald green
                borderRadius: 4,
                barThickness: 12
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: { enabled: true } },
            scales: {
                x: {
                    grid: { display: false, drawBorder: false },
                    ticks: { color: textColor, font: { family: "'Outfit', sans-serif", size: 11 } }
                },
                y: { display: false, min: 0, max: 100 }
            }
        }
    });
}

// 2. AQI Gauge Chart (Half Doughnut)
const aqiCanvas = document.getElementById("aqiChart");
if (aqiCanvas) {
    const aqiVal = parseInt(aqiCanvas.dataset.aqi || 0);
    const maxAqi = 5;
    
    // Determine color based on AQI level
    let aqiColor = "#10b981"; // Good
    if(aqiVal === 2) aqiColor = "#3b82f6";
    if(aqiVal === 3) aqiColor = "#f59e0b";
    if(aqiVal >= 4) aqiColor = "#ef4444";

    new Chart(aqiCanvas, {
        type: "doughnut",
        data: {
            labels: ["AQI", ""],
            datasets: [{
                data: [aqiVal, Math.max(0, maxAqi - aqiVal)],
                backgroundColor: [aqiColor, "rgba(255, 255, 255, 0.1)"],
                borderWidth: 0,
                borderRadius: [10, 0]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            circumference: 180,
            rotation: 270,
            cutout: "85%",
            plugins: { legend: { display: false }, tooltip: { enabled: false } }
        }
    });
}

// 3. Wind Visual Chart (Stylized bars)
const windCanvas = document.getElementById("windChart");
if (windCanvas) {
    // Decorative wave pattern
    const windData = [2, 3, 5, 8, 12, 8, 5, 3, 2];
    
    new Chart(windCanvas, {
        type: "bar",
        data: {
            labels: ["", "", "", "", "", "", "", "", ""],
            datasets: [{
                data: windData,
                backgroundColor: (context) => {
                    const idx = context.dataIndex;
                    return (idx === 4) ? "#10b981" : "rgba(148, 163, 184, 0.5)";
                },
                borderRadius: 5,
                barThickness: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: { enabled: false } },
            scales: {
                x: { display: false },
                y: { display: false, min: 0, max: 15 }
            }
        }
    });
}