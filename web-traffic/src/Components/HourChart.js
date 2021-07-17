import { Bar } from 'react-chartjs-2';
import React, { useState, useEffect } from 'react';
import data from '../Data/TrafficJSON.json';
import TrafficHour from './TrafficHour'
import Button from 'react-bootstrap/Button'
import '../Styles/GraficaCalle.css'

//nuevamente se declaran las variables para acceder a las partes del JSON y no tener que estar escribiéndolo constantemente
const predictions = data.Data
const olderValues = data.RealValues


//el componente recibe por props el valor seleccionado en el menú
//este método tiene como objetivo tener todos los valores necesarios para aplicar al gráfico
function graphData(props){
    var labels_street = []

    //se añaden todos los nombres de las calles para utilizarlas como valores para el eje Y
    predictions.map(s => {
        labels_street.push(s["street"])
        return null;
    })

    //la siguiente parte busca 2 cosas:
    // 1) obtener todos los valores de la velocidad relativa
    // 2) dependiendo si ese valor es mayor o menor que 0.5, su color será rojo o verde.
    var options = Object.values(Object.keys(predictions[0])) 
    var color_street = [];
    var data_street = []

    if (options.indexOf(props.selectedhour) > -1) {     //si la hora seleccionada se encuentra en el conjunto de predictions
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
        olderValues.map(s => {  //si la hora seleccionada se encuentra en el conjunto de valores reales.

            data_street.push(s[props.selectedhour])
            if(s[props.selectedhour] > 0.5){    
                color_street.push('rgba(22, 191, 37, 22)')
            }else{
                color_street.push('rgba(222, 37, 37, 1)')
            }
            return null;
        })
     }


     //se retorna un array cuyos valores serán los obtenidos en el método
    var return_array = [labels_street, data_street, color_street];

    return return_array;


}


//este componente muestra la gráfica para la hora seleccionada por el usuario que es recibida por parámetros
function GraficaHora(props) {
    const [condition1, setcondition1]  = useState(true); //misma condición que en el otro componente, comprueba si se debe renderizar este componente o el otro
    const [selectedHour, setSelectedHour] = useState(props)
    useEffect(() =>{
        setSelectedHour(props);
    },[props])
    
    var graph_info = graphData(props)   //los datos generados por el método co la información para hacer la gráfica

    const [barData, ] = useState({  //se crea la gráfica utilizando los valores de la hora
        labels: graph_info[0],
        datasets: [
            {
                data: graph_info[1],
                backgroundColor: graph_info[2],
                borderWidth: 1
            }
        ]
    });
    //más configuración de la gráfica
    const [barOptions, ] = useState({
        indexAxis: 'y',
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

    if(condition1){ //si se cumple la condición de que este es el componente a mostrar, se renderiza la gráfica con la información de la hora seleccionada
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
        // si se ha presionado el botón de cargar el otro componente, se carga el del menú de selección
        return(
            <TrafficHour></TrafficHour>
        )
    }

}

export default GraficaHora;