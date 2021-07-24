## Requisitos

El proyecto consta de 2 módulos que requieren tener una serie de librerías/herramientas instaladas para poder ser ejecutadas. En caso de no tener estos requisitos instalados, no se podrá ejecutar el proyecto.

### Realtime Predictions

Este es el módulo para la obtención de datos, análisis y procesamiento de los datos, creación de los modelos predictivos y generación de predicciones en tiempo real. Todo el módulo está desarrollado en Python, por lo que el primer requisito es tener Python 3> instalado. Si el proyecto es ejecutado desde Visual Studio Code, se deberá tener instalada la extensión de Python para el editor de código. 

Además, se hace uso de las siguientes librerías de Python. La instalación se puede hacer con "pip", por lo que deberá ser instalado también:
- pip install pandas 
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

El módulo para la recolección de datos en tiempo real será utilizado hasta que se cierre la consola en la que se está ejecutando.

Si el módulo devuelve un error se debe a que se ha llegado al límite de solicitudes mensuales para la API de clima. Esto no debería ocurrir de forma individual, pero si hay mucha gente utilizando el proyecto sí que podría llegar a darse esta situación. Para solucionarlo, se debe registrar para obtener una nueva clave gratuita de visual-crossing y añadir en los siguientes directorios:

- línea 14 y/o 16 de /NY-Traffic-Prediction/Realtime Predictions/realtime_apis/api_weather.py
- línea 15 de /NY-Traffic-Prediction/Realtime Predictions/historical_apis/historical_api_weather.py

Las claves se obtienen del siguiente enlace: https://rapidapi.com/visual-crossing-corporation-visual-crossing-corporation-default/api/visual-crossing-weather/ . Se debe registrar en la página y en la parte de "Pricing" seleccionar la opción "Basic". Una vez suscrito en la API, en el menú de "endpoints" de la página web aparece la clave generada.

Es importante tener en cuenta que durante la primera ejecución del main.py se puede demorar sobre 30 minutos, ya que necesita descargar todos los datos históricos, preprocesarlos y crear los modelos para cada una de las calles. Para visualizar las primeras predicciones y valores obtenidos en tiempo real también hay que esperar un poco, ya que necesita hacer varias peticiones de horas pasadas para generar las predicciones.

A la hora de realizar la descarga de datos históricos, puede darse el caso en el que la API de tráfico no funcione/haya sufrido una caída. No es algo que suela ocurrir, pero cuando pasa, la ejecución de la descarga automática se detiene. Si esto ocurre antes de que aparezca el mensaje de confirmación de la finalización de descarga de datos históricos, se deben realizar las siguientes acciones:

- eliminar todos los archivos dentro de /RealtimePredictions/data/historical_data/data_without_merge/air_quality_historical
- eliminar todos los archivos dentro de /RealtimePredictions/data/historical_data/data_without_merge/traffic_historical
- eliminar todos los archivos dentro de /RealtimePredictions/data/historical_data/data_without_merge/weather_historical
- eliminar la carpeta /RealtimePredictions/data/historical_data/merge_historical/2019_2020_2021

Una vez realizado, se puede volver a ejecutar la descarga de los datos. 

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
