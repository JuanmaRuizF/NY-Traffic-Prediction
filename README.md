## Requisitos

El proyecto consta de 2 módulos que requieren tener una serie de librerías/herramientas instaladas para poder ser ejecutadas. En caso de no tener estos requisitos instalados, no se podrá ejecutar el proyecto.

### Realtime Predictions

Este es el módulo para la obtención de datos, análisis y procesamiento de los datos, creación de los modelos predictivos y generación de predicciones en tiempo real. Todo el módulo está desarrollado en Python, por lo que el primer requisito es tener Python 3> instalado. Si el proyecto es ejecutado desde Visual Studio Code, se deberá tener instalada la extensión de Python para el editor de código. 

Además, se hace uso de las siguientes librerías de Python. La instalación se puede hacer con "pip", por lo que deberá ser instalado también:
- pip install pandas 
- pip install matplotlib
- pip install sodapy
- pip install IPython
- pip install tensorflow

Al instalar pandas se instala automáticamente Numpy, dateutil y pytz, por lo que no será necesario instalarlas por separado.

#### Método de ejecución del módulo

1. Abrir la consola de comandos
2. Navegar hacia el módulo: "cd localizacion_proyecto/NY-Traffic-Prediction/Realtime Predictions"
3. Dependiendo de la forma en la que se quiera ejecutar el proyecto (desde la consola o VSC):
  - Consola: "python main.py"
  - VSC: "code ." y presionar el botón para ejecutar el proyecto en Visual Studio Code

### web-traffic

Este módulo es la página web. Está hecha en React, por lo que se deberá tener React instalado (esto incluye instalar node.js y npm). Una vez se cuente con lo necesario para ejecutar un proyecto en React, seguir los siguientes pasos:

1. Abrir la consola de comandos
2. Navegar hacia el módulo: "cd localizacion_proyecto/NY-Traffic-Prediction/web-traffic"

Si no se ha ejecutado nunca esta parte del proyecto deberá instalarse los módulos de npm necesarios para mostrar la página web: 
- npm install
- npm start

Si ya se encuentran estos módulos instalados:
- npm start

Al ejecutar el comando "npm start" la página web se mostrará en el http://localhost:3000/
