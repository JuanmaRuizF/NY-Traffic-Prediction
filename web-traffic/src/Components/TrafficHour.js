import React from "react";
import { useState } from "react";
import Form from "react-bootstrap/Form";
import GraficaHora from "./GraficaHora";
import Button from "react-bootstrap/Button";
import data from "../Data/TrafficJSON.json";
import "../Styles/TrafficHour.css";

const predictions = data.Data;
const olderValues = data.RealValues;

function getOptions() {
  var options_predictions = Object.values(Object.keys(predictions[0]));

  var options_older_values = Object.keys(olderValues[0]);

  for (var i in options_predictions) {
    options_older_values.push(options_predictions[i]);
  }

  var index = options_older_values.indexOf("street");
  while (index > 0) {
    options_older_values.splice(index, 1);
    index = options_older_values.indexOf("street");
  }

  return options_older_values;
}

function TrafficHour() {
  var options = getOptions();
  const [selectedHour, setSelectedHour] = useState(options[0]);

  const [condition1, setCondition1] = useState(true);

  if (condition1) {
    return (
      <div>
        <div>
          <h3 className="centerTitle"> Visualiza el tráfico por hora</h3>
          <Form className="mt-5">
            <Form.Group controlId="exampleForm.SelectCustom">
              <Form.Control
                as="select"
                onChange={(event) => {
                  setSelectedHour(event.target.value);
                }}
                custom
              >
                {options.map((s) => (
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
            onClick={() => setCondition1(false)}
          >
            Comprueba el tráfico para la hora seleccionada
          </Button>{" "}
        </div>
      </div>
    );
  } else {
    console.log({ selectedHour });
    return (
      <div>
        <GraficaHora selectedhour={selectedHour}></GraficaHora>
      </div>
    );
  }
}

export default TrafficHour;
