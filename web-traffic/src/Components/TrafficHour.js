import React from "react";
import { useState } from "react";
import Form from "react-bootstrap/Form";
import GraficaHora from "./HourChart";
import Button from "react-bootstrap/Button";
import data from "../Data/TrafficJSON.json";
import "../Styles/TrafficHour.css";

//Estas llamadas sirven para acceder directamente a los datos de Data y RealValues dentro del JSON y no tener que estar repitiendo esta parte del código para cada llamada
const predictions = data.Data;
const olderValues = data.RealValues;

//Como este componente tiene como objetivo mostrar todas las horas disponibles en el JSON, se accede a las fechas y horas que se encuentran en el JSON y se retornan.
//Como en los 2 apartados del JSON hay horas que pueden ser idénticas, el método comprueba esto para evitar añadirlas duplicadas.
function getOptions() {
  var options_predictions = Object.values(Object.keys(predictions[0]));

  var options_older_values = Object.keys(olderValues[0]);
  var return_array = []

  for (var i in options_older_values){
    if(options_older_values[i].localeCompare("street") === 0){
      continue
    }else{
      return_array.push(options_older_values[i])
    }

  }

  for (var j in options_predictions){
    if(options_predictions[j].localeCompare("street") === 0){
      continue
    }else{
      if(return_array.indexOf(options_predictions[j]) !== -1){
      }else{
        return_array.push(options_predictions[j])
      }
    }
  }
  return_array = return_array.sort().reverse()

  return return_array
}

//muestra el menú con todas las horas disponibles para seleccionar la que se desee y el botón con el que generar el gráfico.
function TrafficHour() {

  var options = getOptions(); //se hace la llamada para tener todas las posibles horas

  const [selectedHour, setSelectedHour] = useState(options[0]); //el primer valor será el valor por defecto en el menú desplegable, pero el valor cambiará cuando se seleccione otra opción
  const [condition1, setCondition1] = useState(true); //esta variable controlará si se renderiza este componente o el componente con la gráfica para la hora

  if (condition1) { //por defecto, se carga este componente
    return (
      <div>
        <div>
          <h3 className="centerTitle"> Visualiza el tráfico por hora</h3>
          <Form className="mt-5">
            <Form.Group controlId="exampleForm.SelectCustom">
              <Form.Control
                as="select"
                onChange={(event) => {
                  setSelectedHour(event.target.value);  //el valor de la hora seleccionada cambia al escoger otra opción
                }}
                custom>
                {options.map((s) => ( // se recorre la lista de las posibles opciones y se añaden al menú deplegable. Además, se eliminan los valores para los segundos en el substring  
                  <option key={s} value={s}>   
                    {s.substring(0,16)} 
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
          </Form>
        </div>

        <div className="centrado">
          <Button
            variant="primary"
            size="md"
            onClick={() => setCondition1(false)}  // al presionar el botón significa que se quiere ver la gráfica con el valor para la hora, por lo que se renderizará el otro componente
          >
            Comprueba el tráfico para la hora seleccionada
          </Button>{" "}
        </div>
      </div>
    );
  } else {
    // como se ha presionado el botón y la condición ha cambiado su valor, este componente se renderiza. Además, se le pasa por props el valor de la hora seleccionada, 
    // para así poder generar las gráficas para esa hora
    return (
      <div>
        <GraficaHora selectedhour={selectedHour}></GraficaHora> 
      </div>
    );
  }
}

export default TrafficHour;
