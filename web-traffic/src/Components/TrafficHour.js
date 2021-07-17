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
function getOptions() {
  var options_predictions = Object.values(Object.keys(predictions[0]));

  var options_older_values = Object.keys(olderValues[0]);


  for (var i in options_predictions) {
    options_older_values.push(options_predictions[i]);  //se añaden las horas 
  }

  //en este momento se han añadido todas las horas a la lista, pero hay 2 instancias en las que aparece "street", por lo que hay que eliminarlas
  var index = options_older_values.indexOf("street");
  while (index > 0) {
    options_older_values.splice(index, 1); 
    index = options_older_values.indexOf("street"); //este sirve para comprobar el segundo "street" que hay
  }

  return options_older_values;  //se devuelve la lista con las posibles horas
}


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
                  setSelectedHour(event.target.value);  //el valor de la hora seleccionada cambia al escoger otro
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
