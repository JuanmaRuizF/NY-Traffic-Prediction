import React,  {useState, useEffect} from 'react';
import '../Styles/Map.css'

function useWindowSize() {
    // Initialize state with undefined width/height so server and client renders match
    // Learn more here: https://joshwcomeau.com/react/the-perils-of-rehydration/
    const [windowSize, setWindowSize] = useState({
      width: undefined,
      height: undefined,
    });
    useEffect(() => {
      // Handler to call on window resize
      function handleResize() {
        // Set window width/height to state
        setWindowSize({
          width: window.innerWidth,
          height: window.innerHeight,
        });
      }
      // Add event listener
      window.addEventListener("resize", handleResize);
      // Call handler right away so state gets updated with initial window size
      handleResize();
      // Remove event listener on cleanup
      return () => window.removeEventListener("resize", handleResize);
    }, []); // Empty array ensures that effect is only run on mount
    return windowSize;
  }



function Map(){
    
    const size = useWindowSize();

    if (size["width"] > 800) {

        return(

            <div>
                <h3 className="centerTitle"> Localización de las calles con mediciones</h3>
                <div className="centradoMapa">
                    <iframe title="mapa" src="https://www.google.com/maps/d/u/0/embed?mid=1GXf-V5fhF0FqSJ4Ogfa4SFCOu5yG0_A0" width="640" height="380"></iframe>
    
                </div>
            </div>
    
        );
    } else {
        console.log("holaaa")
        return(

            <div>
                <h3 className="centerTitle"> Localización de las calles con mediciones</h3>
                <div className="centradoMapa">
                    <iframe title="mapa" src="https://www.google.com/maps/d/u/0/embed?mid=1GXf-V5fhF0FqSJ4Ogfa4SFCOu5yG0_A0" width="340" height="180"></iframe>
    
                </div>
            </div>
    
        );
    
    }
    
}

export default Map;




// function Map(){
    



//       return(

//           <div>
//               <h3 className="centerTitle"> Map of the predicted streets</h3>
//               <div className="centradoMapa">
//                   <iframe className="mapa"title="mapa" src="https://www.google.com/maps/d/u/0/embed?mid=1GXf-V5fhF0FqSJ4Ogfa4SFCOu5yG0_A0" width="640" height="380"></iframe>
  
//               </div>
//           </div>
  
//       );
  

  
// }

// export default Map;