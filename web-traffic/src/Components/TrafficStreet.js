
import React from 'react';
import data from '../Data/TrafficJSON.json'
import {useState} from 'react';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import '../Styles/TrafficStreet.css'
import LineGraph from './StreetLineChart'


const dataToday = data.Data;

function getData(){
    
    var return_array = []
    dataToday.map(s => (
        return_array.push(s["street"])
    ))
    return return_array
}

function Body(){

    var options = getData()

    const [selectedStreet, setSelectedStreet] = useState(options[0]); //CAMBIAR EL VALOR POR DEFECTO DE ESTA CALLE

    const [condition1, setcondition1]  = useState(true); 


    if(condition1 ){
        return (
            <div className="mainContainer">
                <h3 className="centerTitle"> Visualiza el tráfico por calle</h3>

                <Form className="mt-5">
                    <Form.Group controlId="exampleForm.SelectCustom">
                        <Form.Control as="select" onChange={ (event) =>{
                            setSelectedStreet(event.target.value)
                            // console.log(event.target.value)
                            // console.log(selectedStreet)
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
        
    }else {
        console.log({selectedStreet})
        return(
            <div>

                <LineGraph streetname={selectedStreet}></LineGraph>
            </div>


            // <GraficaCalle streetname={selectedStreet}></GraficaCalle>
        )
    

        
    }

}

export default Body;