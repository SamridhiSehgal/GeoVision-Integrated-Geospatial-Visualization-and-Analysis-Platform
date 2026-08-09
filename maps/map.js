// DRDO OFFLINE GIS MAP
// CREATE MAP
const map = L.map("map", {
    zoomControl: true,
    worldCopyJump: true
}).setView([20.5937, 78.9629], 5);
// OFFLINE TILE LAYER
const tileLayer = L.tileLayer(
    "http://localhost:8000/tiles/{z}/{x}/{y}.webp",
    {
        attribution: "Offline",
        minZoom: 0,
        maxZoom: 12,
        tileSize: 256,
        noWrap: true
    }
);
tileLayer.addTo(map);
// SCALE BAR

L.control.scale({
    metric: true,
    imperial: false
}).addTo(map);
// GRID LAYER
const gridLayer = L.layerGroup();
gridLayer.addTo(map);
// TARGET LAYE
const targetLayer = L.layerGroup();
targetLayer.addTo(map);

const sensorLayer = L.layerGroup();
sensorLayer.addTo(map);
const fovLayer = L.layerGroup();
fovLayer.addTo(map);
const staticFovLayers = {};
// DECIMAL TO DMS
function decimalToDMS(value, isLatitude){
    const direction = value >= 0
        ? (isLatitude ? "N" : "E")
        : (isLatitude ? "S" : "W");
    value = Math.abs(value);
    const degree = Math.floor(value);
    const minuteFloat = (value - degree) * 60;
    const minute = Math.floor(minuteFloat);
    const second = ((minuteFloat - minute) * 60).toFixed(2);
    return degree +
        "° " +
        minute +
        "' " +
        second +
        "\" " +
        direction;
}
// MAP CLICK
map.on("click", function(e){
    L.popup()
        .setLatLng(e.latlng)
        .setContent(
            "<b>Latitude</b><br>" +
            e.latlng.lat.toFixed(6)
            +
            "<br><br>"
            +
            "<b>Longitude</b><br>"
            +
            e.latlng.lng.toFixed(6)
            +
            "<hr>"
            +
            decimalToDMS(e.latlng.lat,true)
            +
            "<br>"
            +
            decimalToDMS(e.latlng.lng,false)
        )
        .openOn(map);
});
// GRID SPACING

function getGridSpacing() {
    const zoom = map.getZoom();
    if (zoom <= 2) return 30;            // 30°
    if (zoom <= 4) return 10;            // 10°
    if (zoom <= 6) return 5;             // 5°
    if (zoom <= 8) return 1;             // 1°
    if (zoom <= 10) return 30 / 60;      // 30'
    if (zoom <= 12) return 15 / 60;      // 15'
    if (zoom <= 14) return 5 / 60;       // 5'
    if (zoom <= 16) return 1 / 60;       // 1'
    return 30 / 3600;                    // 30"
}
// DRAW GRID
// DRAW GRID
function drawGrid() {
    gridLayer.clearLayers();
    const step = getGridSpacing();
    const bounds = map.getBounds();
    const south = Math.floor(bounds.getSouth() / step) * step;
    const north = Math.ceil(bounds.getNorth() / step) * step;

    const west = Math.floor(bounds.getWest() / step) * step;
    const east = Math.ceil(bounds.getEast() / step) * step;
    // Latitude Lines
    for (let lat = south; lat <= north; lat += step) {
        L.polyline(
            [
                [lat, west],
                [lat, east]
            ],
            {
                color: "#666",
                weight: 1,
                opacity: 0.6,
                interactive: false
            }
        ).addTo(gridLayer);
        L.marker(
            [lat, west],
            {
                interactive: false,
                icon: L.divIcon({
                    className: "coordinate-label",
                    html: formatGridLabel(lat, true),
                    iconSize: [80, 20]
                })
            }
        ).addTo(gridLayer);
}
    // Longitude Lines
    for (let lon = west; lon <= east; lon += step) {
        L.polyline(
            [
                [south, lon],
                [north, lon]
            ],
            {
                color: "#666",
                weight: 1,
                opacity: 0.6,
                interactive: false
            }
        ).addTo(gridLayer);
        L.marker(
            [south, lon],
            {
                interactive: false,

                icon: L.divIcon({
                    className: "coordinate-label",
                    html: formatGridLabel(lon, false),
                    iconSize: [80, 20]
                })
            }
        ).addTo(gridLayer);
    }
}
map.on("zoomend", drawGrid);
map.on("moveend", drawGrid);
drawGrid();
// FORMAT GRID LABEL
// GRID LABEL FORMAT
function formatGridLabel(value, isLatitude) {
    const dir = value >= 0
        ? (isLatitude ? "N" : "E")
        : (isLatitude ? "S" : "W");
    value = Math.abs(value);
    const deg = Math.floor(value);
    const minFloat = (value - deg) * 60;
    const min = Math.floor(minFloat);
    const sec = Math.round((minFloat - min) * 60);
    const spacing = getGridSpacing();
    if (spacing >= 1) {
        return `${deg}°${dir}`;
    }
    if (spacing >= (1 / 60)) {
        return `${deg}°${String(min).padStart(2,'0')}'${dir}`;
    }
    return `${deg}°${String(min).padStart(2,'0')}'${String(sec).padStart(2,'0')}"${dir}`;
}
// TARGET ICON
function markerIcon(color) {
    return L.divIcon({
        className: "",
        html:
            "<div class='target-icon' style='background:" +
            color +
            ";'></div>",
        iconSize: [14, 14]
    });
}
// LOAD TARGETS (Called from PySide6)
function loadTargets(targets){

    targetLayer.clearLayers();

    if(targets.length === 0)
        return;

    targets.forEach(function(target){

        let marker = L.marker(
            [target.lat, target.lon],
            {
                icon: markerIcon(target.color || "red")
            }
        ).addTo(targetLayer);

        marker.bindPopup(
            "<b>"+target.name+"</b>"
        );

    });

}
let targetMarker = null;
function moveTarget(lat, lon){

    if(targetMarker === null){

        targetMarker = L.marker(
            [lat, lon],
            {
                icon: markerIcon("red")
            }
        ).addTo(targetLayer);

    }
    else{

        targetMarker.setLatLng(
            [lat, lon]
        );

    }

}
// TRAJECTORY LAYER

const trajectoryLayer = L.layerGroup();

trajectoryLayer.addTo(map);

let movingTarget = null;
// LOAD TRAJECTORY (Called from PySide6)

function loadTrajectory(points){
       enableMissionTrail = true;
    console.log("DRAWING TRAJECTORY", points);

    // create visible markers first
    

    // create line

    let trajectoryLine = L.polyline(
        points,
        {
            color: "red",
            weight: 3
        }
    );

    trajectoryLine.addTo(map);

    map.fitBounds(
        trajectoryLine.getBounds()
    );

    console.log("TRAJECTORY DRAW COMPLETE");

}
function drawAnimatedFOV(sensor){
    fovLayer.clearLayers();
    if(
        sensor.heading == null ||
        sensor.fov == null ||
        sensor.range == null
    ){
        console.log("No FOV data");
        return;
    }

    let points=[];

    points.push(
        [
            sensor.lat,
            sensor.lon
        ]
    );

    let start =
        sensor.heading - sensor.fov/2;

    let end =
        sensor.heading + sensor.fov/2;

    let distance =
        sensor.range / 111320;

    for(
        let i=0;
        i<=30;
        i++
    ){

        let angle =
            start +
            (end-start)*i/30;

        let lat =
            sensor.lat +
            distance *
            Math.cos(angle*Math.PI/180);

        let lon =
            sensor.lon +
            distance *
            Math.sin(angle*Math.PI/180);

        points.push(
            [
                lat,
                lon
            ]
        );

    }

    L.polygon(
    points,
    {
        color: "blue",
        weight: 2,
        fillColor: "blue",
        fillOpacity: 0.25
    }
).addTo(fovLayer);

}
function drawStaticFOV(sensor){

    console.log("STATIC FOV DATA:", sensor);

    if(
        sensor.heading == null ||
        sensor.fov == null ||
        sensor.range == null
    ){
        console.log("Static FOV missing data");
        return;
    }

    // remove previous FOV of same sensor
    if(staticFovLayers[sensor.name]){
        map.removeLayer(staticFovLayers[sensor.name]);
    }

    let points=[];

    points.push([
        sensor.lat,
        sensor.lon
    ]);

    let start = sensor.heading - sensor.fov/2;
    let end   = sensor.heading + sensor.fov/2;

    let distance = sensor.range / 111320;

    for(let i=0;i<=30;i++){

        let angle =
            start + (end-start)*i/30;

        let lat =
            sensor.lat +
            distance*Math.cos(angle*Math.PI/180);

        let lon =
            sensor.lon +
            distance*Math.sin(angle*Math.PI/180);

        points.push([
            lat,
            lon
        ]);
    }

    let polygon = L.polygon(
        points,
        {
            color:"green",
            fillColor:"green",
            fillOpacity:0.25,
            weight:2
        }
    ).addTo(map);

    staticFovLayers[sensor.name] = polygon;

}
function loadSensors(sensors){

 

    sensorLayer.clearLayers();
  

    sensors.forEach(function(sensor){
L.marker(
    [sensor.lat, sensor.lon],
    {
        icon: markerIcon("blue")
    }
).addTo(sensorLayer);

        drawStaticFOV(sensor);

    });

}
let fovSensorMarker = null;
let fovTargetMarker = null;

function showFOVSensorTarget(data){

    if(fovSensorMarker == null){

        fovSensorMarker = L.marker(
            [data.sensor_lat,data.sensor_lon],
            {
                icon: markerIcon("blue")
            }
        ).addTo(sensorLayer);

    }
    else{

        fovSensorMarker.setLatLng(
            [data.sensor_lat,data.sensor_lon]
        );

    }


    if(fovTargetMarker == null){

        fovTargetMarker = L.marker(
            [data.target_lat,data.target_lon],
            {
                icon: markerIcon("red")
            }
        ).addTo(targetLayer);

    }
    else{

        fovTargetMarker.setLatLng(
            [data.target_lat,data.target_lon]
        );

    }

}
function updateMovingTarget(lat, lon){

    if(movingTarget == null){

        movingTarget = L.circleMarker(
            [lat, lon],
            {
                radius:8,
                color:"lime",
                fillColor:"lime",
                fillOpacity:1
            }
        ).addTo(map);

    }
    else{

        movingTarget.setLatLng(
            [lat, lon]
        );

    }

}
function createTargetMarker(lat, lon) {

    if (targetMarker === null) {

        targetMarker = L.marker(
            [lat, lon],
            {
                icon: redIcon
            }
        ).addTo(map);

    }
    else {

        targetMarker.setLatLng(
            [lat, lon]
        );

    }
}
function updateMovingSensor(lat, lon){

    if(movingSensor == null){

        movingSensor = L.circleMarker(
            [lat, lon],
            {
                radius:8,
                color:"blue",
                fillColor:"blue",
                fillOpacity:1
            }
        ).addTo(sensorLayer);

    }
    else{

        movingSensor.setLatLng(
            [lat, lon]
        );

    }

}
// ===========================
// PHASE 2.2 MISSION ANIMATION
// ===========================

// ===========================
// PHASE 2.2 MISSION ANIMATION
// ===========================

let missionSensor = null;
let missionTarget = null;

let missionTrail = [];
let missionTrailLine = null;

let enableMissionTrail = false;

function animateMissionTarget(lat, lon){

    if(missionTarget == null){

        missionTarget = L.circleMarker(
            [lat, lon],
            {
                radius:8,
                color:"red",
                fillColor:"red",
                fillOpacity:1
            }
        ).addTo(targetLayer);

    }
    else{

        missionTarget.setLatLng(
            [lat, lon]
        );

    }

    // Draw trail only when trajectory is loaded

    if(enableMissionTrail){

        missionTrail.push(
            [lat, lon]
        );

        if(missionTrailLine == null){

            missionTrailLine = L.polyline(
                missionTrail,
                {
                    color:"red",
                    weight:3
                }
            ).addTo(map);

        }
        else{

            missionTrailLine.setLatLngs(
                missionTrail
            );

        }

    }

}
function animateMissionSensor(lat, lon){

    if(missionSensor == null){

        missionSensor = L.circleMarker(
            [lat, lon],
            {
                radius:8,
                color:"blue",
                fillColor:"blue",
                fillOpacity:1
            }
        ).addTo(sensorLayer);

    }
    else{

        missionSensor.setLatLng(
            [lat, lon]
        );

    }

}
function resetMissionAnimation(){

    if(missionSensor){
        sensorLayer.removeLayer(missionSensor);
        missionSensor = null;
    }

    if(missionTarget){
        targetLayer.removeLayer(missionTarget);
        missionTarget = null;
    }

    if(missionTrailLine){
        map.removeLayer(missionTrailLine);
        missionTrailLine = null;
    }

    missionTrail = [];
}
