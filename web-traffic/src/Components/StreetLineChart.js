import React, {useState} from "react";
import { Line } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";
import data from '../Data/TrafficJSON.json'
import Button from 'react-bootstrap/Button'
import TrafficStreet from './TrafficStreet'

const predictions = data.Data
const olderValues = data.RealValues


function getLabels(props){
  var labels = []

  olderValues.map(s => {
    if(s["street"] === props.streetname){
      for (const [key] of Object.entries(s)) {
        if(key !== "street"){
          labels.push(key.substring(5,16).replace("-","/"))
        }
      }
    }
    return null
  })

  predictions.map(s => {
    if(s["street"] === props.streetname){
      for (const [key] of Object.entries(s)) {
        if(key !== "street"){
          labels.push(key.substring(5,16).replace("-", "/"))
        }
        
      }
    }
    return null
  })
  return labels
}

function getPastValueData(props){
  var pastValueData = []

  olderValues.map(s => {
    if(s["street"] === props.streetname){
      for (const [,value] of Object.entries(s)) {
        if(value !== props.streetname){
          pastValueData.push(value)
        }
      }
    }
    return null
  })
  return pastValueData
}

function getPredictionData(props, lastValue){
  // var predictionData = [null, null, null, null, null]

  var predictionData = [null, null, null, null, null, lastValue]
  predictions.map(s => {
    if(s["street"] === props.streetname){
      for (const [,value] of Object.entries(s)) {
        if(value !== props.streetname){
          predictionData.push(value)
        }
      }
    }
    return null
  })

  return predictionData
}

function ChartsPage(props){
  
  const [condition1, setcondition1]  = useState(true); 
    var labels = getLabels(props)

    var pastValueData = getPastValueData(props)
    var predictionData = getPredictionData(props, pastValueData[pastValueData.length-1])

    const [state,] = useState({
        dataLine: {
            labels: labels,
            datasets: [
              {
                label: "Valores Previos",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(225, 204,230, .3)",
                borderColor: "rgb(199, 142, 44)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(205, 130,1 58)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: pastValueData
              },
              {
                label: "Predicciones",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgba(225, 204,230, .3)",
                borderColor: "rgb(35, 26, 136)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(35, 26, 136)",
                pointBackgroundColor: "rgb(255, 255, 255)",
                pointBorderWidth: 10,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: predictionData
              },

            ]
        }
    });

    console.log(props.streetname)
      if(condition1){
        return(
          <>
          <div className="mainContainer">
          <h3 className="centerTitle"> Visualiza el tráfico por calle</h3>
          
          <h4 className="centerTitle">{props.streetname}</h4>
          <MDBContainer>  
              <Line data={state.dataLine} options={{ responsive: true }}/>
          </MDBContainer>

          <p>El eje X muestra el tiempo. Los 6 primeros valores son los valores reales registrados en esa calle para esa hora. Los otros 4 valores representan las predicciones realizadas por el modelo para las siguientes 4 horas. El modelo utiliza las últimas 12 horas de datos para realizar estas predicciones.</p>
          <p>El eje Y representa la velocidad relativa. Por ejemplo, una velocidad relativa de 0.5 en una calle de un máximo de 100 km/h significa que los coches han viajado por esa calle a una media de 50 km/h. Se considera que el estado del tráfico es malo cuando
            la velocidad relativa es inferior a 0,5</p>      
                <div className="centrado">
                <Button variant="primary" size="md" onClick={() => 
                    setcondition1(false)

                    }>Selecciona otra calle</Button>{' '}
                </div>
            </div>
          </>
        );
      }else{
        return(
          <TrafficStreet></TrafficStreet>
        )
      }
        
      


}

export default ChartsPage