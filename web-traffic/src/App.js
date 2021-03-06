import React, { Component } from 'react';
import TrafficStreet from './Components/TrafficStreet';
import TrafficHour from './Components/TrafficHour'
import ComparisonMenu from './Components/ComparisonMenu'
import Map from './Components/Map'
import 'bootstrap/dist/css/bootstrap.min.css';
import LocalTime from './Components/NY-Local-Time';

// Archivo que tiene la estructura básica de la página web. Va llamando a cada uno de los componentes que componen la página web
// Además, añade el fondo de la página web en los estilos.

class App extends Component {
    render() {
        return (
            <div className="backgroundPic">          
                <div className="container">
                    <LocalTime></LocalTime>                  
                    <TrafficHour></TrafficHour>
                    <TrafficStreet></TrafficStreet>
                    <ComparisonMenu></ComparisonMenu>
                    <Map></Map>

                </div>
            </div>
        );
    }
}
 
export default App;


