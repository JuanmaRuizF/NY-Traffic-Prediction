import React, { Component } from 'react';
import TrafficStreet from './Components/TrafficStreet';
import TrafficHour from './Components/TrafficHour'
import Map from './Components/Map'
import 'bootstrap/dist/css/bootstrap.min.css';
import LocalTime from './Components/NY-Local-Time';

class App extends Component {
    render() {
        return (
            <div className="backgroundPic">          
                <div className="container">
                    <LocalTime></LocalTime>                  
                    <TrafficHour></TrafficHour>
                    <TrafficStreet></TrafficStreet>
                    <Map></Map>

                </div>
            </div>
        );
    }
}
 
export default App;


