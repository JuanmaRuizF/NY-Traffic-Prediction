import React from 'react';
import '../Styles/AverageTraffic.css'

//Este componente es informativo. 
//Su objetivo es proporcionar la hora local en nueva York para así poder ver los valores de las gráficas para valores futuros
//El componente consiste en crear una variable de tipo Date que tenga la zona horaria de Nueva York en formato acortado (ej: 8:45 PM)


function averageTraffic(){

    var date_now_NY = new Date().toLocaleString("en-US", {
        timeZone: "America/New_York" ,
        timeStyle: 'short',
    });

    return(
        <div className="mt-5">
            <h2 className="NY-LocalTime">Hora en Nueva York:</h2>
            <h2 className="dateNow">{date_now_NY}</h2>

        </div>
    );

}
export default averageTraffic;