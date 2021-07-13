import { Bar } from 'react-chartjs-2';
import React, { useState, useEffect } from 'react';
import data from '../Data/TrafficJSON.json';
import TrafficHour from './TrafficHour'
import Button from 'react-bootstrap/Button'
import '../Styles/GraficaCalle.css'


const predictions = data.Data
const olderValues = data.RealValues


function graphData(props){
    var labels_street = []

    predictions.map(s => {
        labels_street.push(s["street"])
        return null;
    })

    var options = Object.values(Object.keys(predictions[0])) 

    var color_street = [];
    var data_street = []

    if (options.indexOf(props.selectedhour) > -1) {
        predictions.map(s => {

            data_street.push(s[props.selectedhour])
            if(s[props.selectedhour] > 0.5){    
                color_street.push('rgba(22, 191, 37, 22)')
            }else{
                color_street.push('rgba(222, 37, 37, 1)')
            }
            return null;
        })
     }else {
        olderValues.map(s => {

            data_street.push(s[props.selectedhour])
            if(s[props.selectedhour] > 0.5){    
                color_street.push('rgba(22, 191, 37, 22)')
            }else{
                color_street.push('rgba(222, 37, 37, 1)')
            }
            return null;
        })
     }



    // console.log(data_street)
    if(data_street.length === 0){
        console.log("valores viejos")
    }

    var return_array = [labels_street, data_street, color_street];

    return return_array;


}



function GraficaHora(props) {
    const [condition1, setcondition1]  = useState(true); 
    const [selectedHour, setSelectedHour] = useState(props)
    useEffect(() =>{
        setSelectedHour(props);
    },[props])
    
    var graph_info = graphData(props)

    const [barData, ] = useState({
        labels: graph_info[0],
        datasets: [
            {
                // label: selectedHour.selectedhour,
                data: graph_info[1],
                backgroundColor: graph_info[2],
                borderWidth: 1
            }
        ]
    });

    const [barOptions, ] = useState({
        indexAxis: 'y',
    // Elements options apply to all of the options unless overridden in a dataset
    // In this case, we are setting the border of each horizontal bar to be 2px wide
        elements: {
            bar: {
            borderWidth: 2,
            },
        },
        responsive: true,
        plugins: {
            legend: {
            display:false
            },
            title: {
            display: true,
            text: 'Hora:  ' + selectedHour.selectedhour.substring(0,16),
            },
        },
    });

    if(condition1){
        return (
            <>
            <h3 className="centerTitle"> Visualiza el tráfico por hora</h3>
            <div className="BarExample">
                <Bar
                    data={barData}  
                    options={barOptions} />
            </div>
            <p>El eje Y muestra todas las calles de las que se tienen mediciones. El eje X representa la velocidad relativa de los coches en esa calle en la hora seleccionada. Por ejemplo, si un automóvil cruza una calle a 30 km/h en una calle
                que tiene una velocidad máxima de 60 km/h, la velocidad relativa será de 0,5. Las barras tienen un color verde cuando la velocidad relativa medida / prevista es igual o superior a 0,5, lo que representa que el estado del tráfico
                es bueno. Todas las calles con velocidad relativa inferior a 0,5 tendrán una barra roja que representa un mal estado del tráfico.
                </p>
            <div className="centrado">
            <Button variant="primary" size="md" onClick={() => 
                setcondition1(false)

                }>Selecciona otra hora</Button>{' '}
            </div>
            </>
        );
    }else{
        return(
            <TrafficHour></TrafficHour>
        )
    }
    // return JSX

}

export default GraficaHora;