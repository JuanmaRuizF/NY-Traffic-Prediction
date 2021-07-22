
import React from 'react';
import data from '../Data/TrafficJSON.json'
import {useState} from 'react';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import '../Styles/TrafficStreet.css'
import ComparisonMap from './ComparisonMap'


const dataToday = data.Data;

//este método recoge todas las posibles calles que haya en el JSON
function getData(){
    var return_array = []
    dataToday.map(s => (
        return_array.push(s["street"])
    ))
    return return_array
}

function ComparisonMenu(){
    var options = getData()
    const [selectedStreet, setSelectedStreet] = useState(options[0]); //variable que almacenará la calle seleccionada. Por defecto tiene el valor de la primera calle que se muestra en el menú
    const [condition1, setcondition1]  = useState(true); //variable para controlar si este es el componente a renderizar o debe renderizar el componente de la gráfica. 


    if(condition1 ){    //condición por defecto, se carga el componente con el menú para seleccionar la calle en la que se desea mirar el tráfico
        return (
            <div className="mainContainer">
                <h3 className="centerTitle"> Comparativa de los valores reales y predicciones por calle</h3>

                <Form className="mt-5">
                    <Form.Group controlId="exampleForm.SelectCustom">
                        <Form.Control as="select" onChange={ (event) =>{
                            setSelectedStreet(event.target.value)
                        }} custom>
                            {dataToday.map(s => (
                                    <option key={s["street"]} value={s["street"]}>{s["street"]}</option>
                            ))}
                            
    
                        </Form.Control>
                    </Form.Group>
                </Form>

                <div className="centrado">
                    <Button variant="primary" size="md" onClick={() => 
                    setcondition1(false)
                    }>Comprueba el tráfico para esta calle</Button>{' '}
                </div>
            </div>

        );
        
    }else { //se ha seleccionado el botón de ver el gráfico, por lo que se llama al componente pasándole en props el nombre de la calle seleccionada
        return(
            <div>
                <ComparisonMap streetname={selectedStreet}></ComparisonMap>
            </div>
        )
    }

}

export default ComparisonMenu;