import React, { Component } from 'react';
import TrafficStreet from './Components/TrafficStreet';
import TrafficHour from './Components/TrafficHour'
import Map from './Components/Map'
import 'bootstrap/dist/css/bootstrap.min.css';

class App extends Component {
    render() {
        return (
            <div className="backgroundPic">          
                <div className="container">                  
                    <TrafficHour></TrafficHour>
                    <TrafficStreet></TrafficStreet>
                    <div className="mapContainer">
                        <Map></Map>
                    </div>
                </div>
            </div>
        );
    }
}
 
export default App;


