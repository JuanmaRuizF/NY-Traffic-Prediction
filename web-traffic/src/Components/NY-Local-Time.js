import React from 'react';
import '../Styles/AverageTraffic.css'


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