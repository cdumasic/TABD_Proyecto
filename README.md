# 🧠 Buscador Semántico de Propuestas Políticas

Este proyecto permite buscar propuestas políticas similares usando técnicas de búsqueda semántica con embeddings y ChromaDB. Incluye:

- Backend con FastAPI
- Frontend con Streamlit
- Base de datos vectorial local con ChromaDB

---

## ⚙️ Requisitos

- Python 3.10+
- pip

---

## 🧪 Instalación local

### Configuración del Entorno Local
Para ejecutar el proyecto de forma local, siga los siguientes pasos:
#### Paso 1: Clonar el Repositorio

~~~ 
git clone https://github.com/cdumasic/TABD_Proyecto.git 
git checkout main
~~~ 

#### Paso 2: Creación del entorno virtual 
~~~ 
python -m venv venv
~~~ 

Para activar el entorno virtual
En Windows:
~~~ 
venv\Scripts\activate
~~~ 
En Linux

~~~ 
source venv/bin/activate
~~~

#### Paso 3: Instalar Dependencias
Navegue al directorio del proyecto y ejecute:
~~~ 
pip install -r requirements.txt
~~~ 
#### Paso 4: Cargar la Base de Datos
Navegue al directorio del proyecto y ejecute:
~~~ 
python vectorizar_guardar.py
~~~ 
#### Paso 5: Ejecución del BackEnd
Abra una nueva terminal y ejecute:
~~~ 
cd backend
uvicorn main:app --reload
~~~ 
#### Paso 6: Ejecución del FrontEnd
Abra una nueva terminal y ejecute:
~~~ 
cd frontend
streamlit run buscador_semantico.py
~~~ 
### Verificación del Despliegue Local
Una vez iniciada la aplicación se le enviará al navegador predeterminado sino verifique que la aplicación funcione correctamente accediendo a la URL proporcionada en la consola. La aplicación debe cargar sin errores y mostrar la interfaz de usuario esperada sino recargue la página
