import React, {useState} from "react";
import { Line,Bar  } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";
import data from '../Data/TrafficJSON.json'
import Button from 'react-bootstrap/Button'
import ComparisonMenu from './ComparisonMenu'
import { render } from "@testing-library/react";

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

  var numberValues = historicalArray.length - matchingHours 
  var predictionData = []
  
  for(var i=0; i<numberValues; i++){
    predictionData.push(null)
  }


  predictions.map(s => {
    if(s["street"] === props.streetname){
      for (const [,value] of Object.entries(s).reverse()) {
        if(value !== props.streetname){
          if(matchingHours>0){
            matchingHours = matchingHours -1
            predictionData.push(value)
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

function error_data(pastValueData, predictionData){
  var error_array = []
  var append_error = null

  for(var i=0;i<pastValueData.length;i++){
      if(pastValueData[i] !== null && predictionData[i] !== null){
        append_error = Math.abs(pastValueData[i] - predictionData[i])
        error_array.push(append_error)
      }else{
        error_array.push(null)
      }
  }

  return error_array
}
//este método muestra la gráfica de la calle seleccionada
function ComparisonMap(props){
  
  const [condition1, setcondition1]  = useState(true); //variable de control de renderizado para los componentes


    var matchingHours = getMatchingHours(props)
    var labels = getLabels(props, matchingHours) //listado con las horas que haya en el JSON para la calle seleccionada
    var pastValueData = getPastValueData(props) //datos pasados que haya en el JSON para la calle seleccionada
    var predictionData = getPredictionData(props, pastValueData, matchingHours) //predicciones del JSON para la calle seleccionada. 
    var error_values = error_data(pastValueData,predictionData)

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
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgb(0, 0, 0)",
                pointHoverBorderColor: "rgba(220, 220, 220, 1)",
                pointHoverBorderWidth: 2,
                pointRadius: 7,
                pointStyle: 'crossRot',
                pointBorderWidth:5,
                pointHitRadius: 10,
                data: predictionData
              },

            ]
        },
        barChartOptions: {
          legend: false,
          responsive: true,
          maintainAspectRatio: true,
        }
    });


    const[state1,] = useState({
      dataBar: {
        labels: labels,
        datasets: [
          {
            label: "Error absoluto",
            data: error_values,
            backgroundColor: [
              "rgba(255, 134,159,0.4)"
            ],
            borderWidth: 2,
            borderColor: [
              "rgba(255, 134, 159, 1)"
            ]
          }
        ]
      },
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
      }
    })


      if(condition1){ //renderizado de la gráfica con los valores de la calle seleccionada

        return(
          <>

          <div className="mainContainer">
          <h3 className="centerTitle">Comparativa de los valores reales y predicciones por calle</h3>
          
          <h4 className="centerTitle">{props.streetname}</h4>
          <MDBContainer>  
              <Line data={state.dataLine} options={{ responsive: true}}/>

          </MDBContainer>
          <h4 className="centerTitle">Error de las predicciones</h4>
          <MDBContainer> 
            <Bar data={state1.dataBar} options={state1.barChartOptions} />
          </MDBContainer>
          <p>El eje X muestra el tiempo. La línea azul muestra los valores reales medidos a lo largo del tiempo. La línea naranja muestra las predicciones que ha ido haciendo el modelo. De este modo, se puede comprobar cómo de acertadas estaban las predicciones con respecto a los valores reales.</p>
          <p>El eje Y representa la velocidad relativa. Por ejemplo, una velocidad relativa de 0.5 en una calle de un máximo de 100 km/h significa que los coches han viajado por esa calle a una media de 50 km/h. Se considera que el estado del tráfico es malo cuando
            la velocidad relativa es inferior a 0,5</p>    
          <p>La gráfica del error de las predicciones muestra el error absoluto para aquellas predicciones que tengan también el valor real para esa hora.</p>  
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
          <ComparisonMenu></ComparisonMenu>
        )
      }
        
      


}

export default ComparisonMap