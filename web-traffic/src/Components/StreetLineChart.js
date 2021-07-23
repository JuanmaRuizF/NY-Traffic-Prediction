import React, {useState} from "react";
import { Line } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";
import data from '../Data/TrafficJSON.json'
import Button from 'react-bootstrap/Button'
import TrafficStreet from './TrafficStreet'

const predictions = data.Data
const olderValues = data.RealValues
/*
Devuelve el número de horas coincidentes entre las predicciones y el tráfico. Esto es de utilidad a la hora de generar la gráfica para
ignorar estas horas coincidentes a la hora de mostrar la gráfica. Para ello, recorre los JSON para la calle especificada y almacena las horas 
Esto lo hace con la parte de predicciones y datos reales. Una vez hechos, se comparan ambos array para determinar el número de horas iguales.
Devuelve este número.
*/
function getMatchingHours(props){ 
  var return_number = 0

  var prediction_hours = []
  predictions.map(s => {
    if(s["street"] === props.streetname){
      for (const [key] of Object.entries(s)) {
        if(key !== props.streetname){
          prediction_hours.push(key)
        }
      }
    }
    return null
  })
  var older_value_hours = []
  olderValues.map(s => {
    if(s["street"] === props.streetname){
      for (const [key] of Object.entries(s)) {
        if(key !== props.streetname){
          if(key !== "street"){
            older_value_hours.push(key)
          }
        }
      }
    }
    return null
  })
  for(var index=0; index<older_value_hours.length; index++){
    if(prediction_hours.indexOf(older_value_hours[index]) > -1){
      return_number = return_number + 1
    }
  }


  return return_number 
}

//esta función tiene como objetivo recoger todas las horas que se encuentren en el JSON para la calle seleccionada. Serán utilizadas como eje X en la gráfica
//además, se cambia el formato de la fecha y hora para ser más sencilla de ver
function getLabels(props, matchingHours){
  var labels = []

  olderValues.map(s => {
    if(s["street"] === props.streetname){
      for (const [key] of Object.entries(s).reverse()) {
        if(key !== "street"){
          // labels.push(key.substring(5,16).replace("-","/"))
          labels.push(key.substring(11,16).replace("-","/"))
        }
      }
    }
    return null
  })

  predictions.map(s => {
    if(s["street"] === props.streetname){
      for (const [key] of Object.entries(s).reverse()) {
        if(key !== "street"){
          if(matchingHours>0){
            matchingHours = matchingHours -1
          }else{
          // labels.push(key.substring(5,16).replace("-", "/"))
          labels.push(key.substring(11,16).replace("-", "/"))
          }

        }
        
      }
    }
    return null
  })
  return labels
}

//recoge todos los datos pasados del JSON cuya calle sea igual a la seleccionada en el menú
function getPastValueData(props){
  var pastValueData = []

  olderValues.map(s => {
    if(s["street"] === props.streetname){
      for (const [,value] of Object.entries(s).reverse()) {
        if(value !== props.streetname){
          pastValueData.push(value)
        }
      }
    }
    return null
  })
  return pastValueData
}

//este método hace lo mismo que getPastValueData() pero para los valores del JSON de las predicciones para la calle
//el parámetro lastValue es utilizado para unir el último valor del pasado con el valor de las predicciones
function getPredictionData(props, historicalArray, matchingHours){

  // var predictionData = [null, null, null, null, null, lastValue]
  var numberValues = historicalArray.length -1 
  var predictionData = []
  
  for(var i=0; i<numberValues; i++){
    predictionData.push(null)
  }
  // console.log(predictions)

  predictionData.push(historicalArray[historicalArray.length-1])
  predictions.map(s => {
    if(s["street"] === props.streetname){
      for (const [,value] of Object.entries(s).reverse()) {
        if(value !== props.streetname){
          if(matchingHours>0){
            matchingHours = matchingHours -1
          }else{
            predictionData.push(value)
          }
        }
      }
    }
    return null
  })

  return predictionData
}

//este método muestra la gráfica de la calle seleccionada
function ChartsPage(props){
  
  const [condition1, setcondition1]  = useState(true); //variable de control de renderizado para los componentes


    var matchingHours = getMatchingHours(props)
    var labels = getLabels(props, matchingHours) //listado con las horas que haya en el JSON para la calle seleccionada
    var pastValueData = getPastValueData(props) //datos pasados que haya en el JSON para la calle seleccionada
    var predictionData = getPredictionData(props, pastValueData, matchingHours) //predicciones del JSON para la calle seleccionada. 
                                                                                        // Además, se añade el último valor de los pasados para que las líneas en la gráfica aparezcan unidas

    const [state,] = useState({ //configuración de la gráfica
        dataLine: {
            labels: labels,
            datasets: [
              {
                label: "Valores Previos",
                fill: true,
                lineTension: 0.3,
                backgroundColor: "rgb(93, 173, 226,0.2)",
                borderColor: "rgb(93, 173, 226)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(93, 173, 226)",
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
                backgroundColor: "rgb(246, 99, 25,0.2)",
                borderColor: "rgb(246, 99, 25)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgb(246, 99,25)",
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

      if(condition1){ //renderizado de la gráfica con los valores de la calle seleccionada
        return(
          <>
          <div className="mainContainer">
          <h3 className="centerTitle"> Visualiza el tráfico por calle</h3>
          
          <h4 className="centerTitle">{props.streetname}</h4>
          <MDBContainer>  
              <Line data={state.dataLine} options={{ responsive: true }}/>
          </MDBContainer>

          <p>El eje X muestra el tiempo. Los primeros valores (línea azul) son los valores reales registrados en esa calle para esa hora. Los otros 4 valores (línea naranja) representan las predicciones realizadas por el modelo para las siguientes 4 horas.</p>
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
      }else{  //se renderiza el menú para seleccionar las calles
        return(
          <TrafficStreet></TrafficStreet>
        )
      }
        
      


}

export default ChartsPage