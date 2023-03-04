const ok = document.getElementById("ok");
const findme = document.getElementById("findme");
const header = document.getElementById("htext");
const APIKEY = 'YOUR_API_KEY'
function modify (w) {
    document.getElementById("loc").textContent = "Location : " + w.name
    document.getElementById("lat").textContent = "Latitude : " + w.coord.lat
    document.getElementById("long").textContent = "Longitude: " + w.coord.lon
    document.getElementById("temp").textContent = "Temperature : " + w.main.temp
    document.getElementById("hum").textContent = "Humidity : " + w.main.humidity
    document.getElementById("pre").textContent = "Pressure : " + w.main.pressure
    document.getElementById("weather").textContent = w.weather[0].main + " : " + w.weather[0].description
    document.getElementById("wimg").src = `https://openweathermap.org/img/wn/${w.weather[0].icon}@2x.png`
} 
async function citycall(query){
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?appid=${APIKEY}&q=${query}`);
    if(response.status != 200){
        alert("Server down please come back later. :(");
    }
    else{
        const data = await response.json()
        modify(data);
    }
}
async function latlongcall(lat,long) {
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&appid=${APIKEY}`)
    if(response.status != 200){
        alert("ERROR Processing your request.")
    }
    else{
        const data = await response.json()
        modify(data);
    }
}
latlongcall(0,0);
// header.addEventListener('click',()=>{location.reload()});
header.addEventListener('click',()=>{latlongcall(0,0)});
ok.addEventListener('click',
    async () => {
        latlong = true;
        query = document.getElementById("bar").value;
        if(query){
            citycall(query);
        }
        else{
            alert("No Input has been provided.");
        }
    }
);
findme.addEventListener('click',
    () => {
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    latlongcall(pos.coords.latitude,pos.coords.longitude);
                }
            );
        }else{
            alert("Geolocation is not supported on this browser.");
        }
    }
);