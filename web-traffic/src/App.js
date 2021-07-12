import React, { Component } from 'react';
import TrafficStreet from './Components/TrafficStreet';
import AverageTraffic from './Components/averageTraffic';
import TrafficHour from './Components/TrafficHour'
import Map from './Components/Map'
import 'bootstrap/dist/css/bootstrap.min.css';

class App extends Component {
    render() {
        return (
            <div className="backgroundPic">
                {/* <Header></Header> */}
            

                <div className="container">
                    <AverageTraffic></AverageTraffic>
                    
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


