import React from 'react';
import data from '../Data/TrafficJSON.json'
import '../Styles/AverageTraffic.css'

const dataToday = data.Today;
function averageTraffic(){



    var date_now_NY = new Date().toLocaleString("en-US", {
        timeZone: "America/New_York" ,
        timeStyle: 'short',
    });

    var hora="";

    // if(date_now_NY.length > 7){
    //     if(date_now_NY.substring(6,8) === "AM"){
    //         hora = date_now_NY.substring(0,2)
    //     }else{
    //         hora = parseInt(date_now_NY.substring(0,2)) + 12
    //     }
    // }else{
    //     if(date_now_NY.substring(5,7) === "AM"){
            // hora = date_now_NY.substring(0,1)
    //     }else{
    //         hora = parseInt(date_now_NY.substring(0,1)) + 12
    //     }
    // }


    // console.log(hora);

    
    var n2 = 0;
    var n1 = 0;

    // for(var i=0; i<dataToday.length; i+=1){
    //     // console.log(dataToday[i][hora])
    //     if(dataToday[i][hora]===1.0){
    //         n1=n1+1;
    //     }else{
    //         n2=n2+1;
    //     }
    // }

    if(n1>n2){
        n1 = 0;
        n2 = 0;
        return(
            <div className="mt-5">
                <h2 className="NY-LocalTime">New York local time:</h2>
                <h2 className="dateNow">{date_now_NY}</h2>
                {/* <h2 className="NY-LocalTime">Overall Status of Traffic Now:</h2>
                <h2 className="goodStatus">Good</h2> */}
            </div>
        );
    }else{
        n1 = 0;
        n2 = 0;
        return(
            <div className="mt-5">
                <h2 className="NY-LocalTime">New York local time:</h2>
                <h2 className="dateNow">{date_now_NY}</h2>
                {/* <h2 className="NY-LocalTime">Overall Status of Traffic Now:</h2>
                <h2><span className="badStatus">Bad</span></h2> */}
            </div>
        );

    }
        


}
export default averageTraffic;