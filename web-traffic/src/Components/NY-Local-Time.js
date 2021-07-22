import React from 'react';
import '../Styles/AverageTraffic.css'
import data from "../Data/TrafficJSON.json";

//Este componente es informativo. 
//Su objetivo es proporcionar la hora local en nueva York para así poder ver los valores de las gráficas para valores futuros
//El componente consiste en crear una variable de tipo Date que tenga la zona horaria de Nueva York en formato acortado (ej: 8:45 PM)
const predictions = data.Data;
const olderValues = data.RealValues;

//obtener la fecha en YYYY-MM-DD para realizar la comparativa posterior
function formatDate(date) { 
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

//realiza la conversión de la fecha actual al formato necesario para las mediciones
function convertTime(){
    var date_now_NY = new Date().toLocaleString("en-US", {
        timeZone: "America/New_York" ,
        hourCycle: 'h24',
    });
    var hora = date_now_NY.substring(date_now_NY.indexOf(" "),date_now_NY.length-5) + "00:00"
    date_now_NY = formatDate(date_now_NY) + hora
    return date_now_NY
}

//comprueba si la fecha se encuentra dentro de los valores del JSON. Si no se encuentra, se renderizará el componente diciendo "Sin información"
function datos_fecha(fecha_hora_procesada){
    var options_predictions = Object.values(Object.keys(predictions[0]));
    var options_older_values = Object.values(Object.keys(olderValues[0]));

    if(options_predictions.indexOf(fecha_hora_procesada)>-1){
        return true
    }else if(options_older_values.indexOf(fecha_hora_procesada)>-1){
        return true
    }
    return false
}

//si la hora se encuentra entre los valores del JSON, los busca y analiza para comprobar si hay más valores que sean >0.5 (estado del tráfico bueno)
//o si hay más valores con un valor menor a 0.5 (estado del tráfico malo). Esto hará que se renderice el componente mostrando si el tráfico está bien o mal
function traffic_status(time){
    var bad_traffic = 0;
    var good_traffic = 0;

    var options_older_values = Object.values(Object.keys(olderValues[0]));

    if(options_older_values.indexOf(time)>-1){  //primero comprueba en el de valores reales, puesto que son los más fiables
        olderValues.map(s => {  
            if(s[time] > 0.5){    //si el tráfico está bien (>0.5), suma el contador de good_traffic, sino suma en el contador de bad_traffic
                good_traffic = good_traffic +1
            }else{
                bad_traffic = bad_traffic +1
            }
            return null;
        })
    }else{
        predictions.map(s => {  //si no se encuentra en los valores reales la hora, se accede a las predicciones para iterar sobre la hora en cuestión
            if(s[time] > 0.5){    
                good_traffic = good_traffic +1
            }else{
                bad_traffic = bad_traffic +1
            }
            return null;
        })
    }
    if(good_traffic>bad_traffic){
        return true
    }else{
        return false
    }
}


function averageTraffic(){

    var date_now_NY = new Date().toLocaleString("en-US", {  //fecha de Nueva York en el formato adecuado
        timeZone: "America/New_York" ,
        timeStyle: 'short',
        hourCycle: 'h24'
    });

    var fecha_hora_procesada = convertTime()    
    var isFound = datos_fecha(fecha_hora_procesada) //se usa la fecha convertida al formato requerido para buscar si esa hora se encuentra dentro de los valores del JSON

    // var isFound = datos_fecha("2021-07-20 22:00:00")


    if(isFound === false){  //si no se encuentra es que no hay datos para esa hora, por lo que muestra el apartado "Sin información"
        return(
            <div className="mt-5">
                <h2 className="NY-LocalTime">Hora en Nueva York:</h2>
                <h2 className="dateNow">{date_now_NY}</h2>
                <h2 className="dateNow">Estado actual del tráfico:</h2>
                <h3 className="noInformation">Sin Información</h3>
            </div>
        );
    
    }else{
        var goodTraffic = traffic_status(fecha_hora_procesada)  //se busca la hora en cuestión en el JSON para comprobar si hay mlás valores de tráfico bien o mal

        if(goodTraffic === true){
            return(
                <div className="mt-5">
                    <h2 className="NY-LocalTime">Hora en Nueva York:</h2>
                    <h2 className="dateNow">{date_now_NY}</h2>
                    <h2 className="dateNow">Estado actual del tráfico:</h2>
                    <h3 className="goodStatus">Bueno</h3>
                </div>
            );
        }else{
            return(
                <div className="mt-5">
                    <h2 className="NY-LocalTime">Hora en Nueva York:</h2>
                    <h2 className="dateNow">{date_now_NY}</h2>
                    <h2 className="dateNow">Estado actual del tráfico:</h2>
                    <h3 className="badStatus">Malo</h3>
                </div>
            );
        }
    }

}
export default averageTraffic;
