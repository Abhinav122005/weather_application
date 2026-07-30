const mapElement = document.getElementById("map");

if (mapElement && window.L) {
    const lat = parseFloat(mapElement.dataset.lat);
    const lon = parseFloat(mapElement.dataset.lon);
    const city = mapElement.dataset.city;

    if (Number.isFinite(lat) && Number.isFinite(lon)) {
        const map = L.map("map").setView([lat, lon], 11);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "&copy; OpenStreetMap contributors",
            maxZoom: 19,
        }).addTo(map);

        L.marker([lat, lon])
            .addTo(map)
            .bindPopup(`<b>${city}</b>`)
            .openPopup();
    }
}
