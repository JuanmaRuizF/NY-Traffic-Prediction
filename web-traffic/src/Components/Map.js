import React,  {useState, useEffect} from 'react';
import '../Styles/Map.css'

//este método tiene como origen el siguiente enlace: https://usehooks.com/useWindowSize/
//sirve para controlar el tamaño de la pantalla. Será utilizado para, dependiendo del tamaño del dispositivo, hacer que el mapa se vea en pequeño o grande
function useWindowSize() {
    const [windowSize, setWindowSize] = useState({
      width: undefined,
      height: undefined,
    });
    useEffect(() => {
      function handleResize() {
        setWindowSize({
          width: window.innerWidth,
          height: window.innerHeight,
        });
      }
      window.addEventListener("resize", handleResize);
      handleResize();
      return () => window.removeEventListener("resize", handleResize);
    }, []); 
    return windowSize;
  }


//este componente es informativo. Muestra un mapa creado en Google My Maps con la localización de las calles de medición.
//hace uso del método useWindowSize() para renderizar mapa en menor tamaño si el tamaño de la pantalla es menor a 800px
function Map(){
    const size = useWindowSize();
    if (size["width"] > 800) {
        return(
            <div>
                <h3 className="centerTitle"> Localización de las calles con mediciones</h3>
                <div className="centradoMapa">
                    <iframe title="mapa" src="https://www.google.com/maps/d/u/0/embed?mid=1GXf-V5fhF0FqSJ4Ogfa4SFCOu5yG0_A0" width="640" height="380"></iframe>
                </div>

                <div className="centradoMapa">
                  <a href="https://github.com/JuanmaRuizF/NY-Traffic-Prediction">
                    <img src="https://image.flaticon.com/icons/png/512/25/25231.png" alt="Github Link" width="40" height="40"></img>
                  </a>
                  <h6>Juan Manuel Ruiz Fránquiz</h6>
                </div>
            </div>
    
        );  
    } else {
        return(

            <div>
                <h3 className="centerTitle"> Localización de las calles con mediciones</h3>
                <div className="centradoMapa">
                    <iframe title="mapa" src="https://www.google.com/maps/d/u/0/embed?mid=1GXf-V5fhF0FqSJ4Ogfa4SFCOu5yG0_A0" width="340" height="180"></iframe>
    
                </div>

                <div className="centradoMapa">
                  <a href="https://github.com/JuanmaRuizF/NY-Traffic-Prediction">
                    <img src="https://image.flaticon.com/icons/png/512/25/25231.png" alt="Github Link" width="40" height="40"></img>
                  </a>
                  <h6>Juan Manuel Ruiz Fránquiz</h6>
                </div>
            </div>
    
        );
    
    }
    
}

export default Map;


