
import React from 'react';
import data from '../Data/TrafficJSON.json'
import {useState} from 'react';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import '../Styles/TrafficStreet.css'
import LineGraph from './StreetLineChart'


const dataToday = data.Data;

function Body(){


    const [selectedStreet, setSelectedStreet] = useState("11th ave n ganservoort - 12th ave @ 40th st"); //CAMBIAR EL VALOR POR DEFECTO DE ESTA CALLE

    const [condition1, setcondition1]  = useState(true); 


    if(condition1 ){
        return (
            <div className="mainContainer">
                <h3 className="centerTitle"> Visualize traffic per street</h3>

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

                    }>Check Traffic for this Street</Button>{' '}

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