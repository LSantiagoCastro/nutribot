import os
from openai import AzureOpenAI

import os
import openai
import dotenv

dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID")

client = AzureOpenAI(
   base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)

query_prompt_template = """
                        Este es un asesor con ai de ventas de clausulas o seguros de Sura, el objetivo es recomendar un seguro o clausula al cliente de acuerdo a su información:
                        Para hacerlo, analiza la información proporcionada y llena el siguiente json con un string que corresponda al nombre del seguro o clausula. 
                        
                        Las respuestas siempre deben ser en formato de objeto Json, Asegurate de que la salida sea formateada como un objeto json:
                        ```json
                        {{
                            "clausulado_a_recomendar": "string"  // En caso de que no se recomiende, debe ser "sin recomendacion".
                        }}
                        ```
                        
                        
                        """
caracteristicas = {
                                    'sexo': 'F',
                                    'edad': '44',
                                    'rango de edad':'Adulto (40 a 64)',
                                    'nivel de ingresos':'Medio Bajo',
                                    'enfermedades':'leucemia y cancer'
                                }
query_prompt_template_fields =f"""
                                    Dadas las siguientes características del cliente:
                                    
                                    {caracteristicas}
                                    
                                    ¿Cuál de las cláusulas recomiendas? Por favor, asegúrate de que la salida sea un objeto json con la clave "clausulado_a_recomendar" y como valor el respectivo nombre del clausulado a recomendar, o "sin recomendacion" si no se recomienda nada.

                                    Las respuestas siempre deben ser en formato de objeto Json, Asegurate de que la salida sea formateada como un objeto json:
                                    ```json
                                    {{
                                        "clausulado_a_recomendar": "string"  // En caso de que no se recomiende, debe ser "sin recomendacion".
                                    }}
                                    ```

"""
print(query_prompt_template_fields)                   
#                     Contexto:

#                     Como asesor de ventas de seguros, tu objetivo es evaluar la elegibilidad del cliente para las diferentes coberturas del Plan Vive. Para hacerlo, analiza la información proporcionada por el cliente y los documentos relevantes, como el clausulado del Plan Vive, anexos sobre enfermedades graves, cáncer, accidentes personales, gastos de curación, auxilio de exequias, así como también el documento de conocimiento experto y políticas de vida individual.

#                     Información de entrada:

#                     - Puedes recibir preguntas relacionadas con las coberturas.
#                     - También se pueden proporcionar características de un posible cliente, como: nombre, IMC, profesión, estado civil, edad, nivel de ingresos, ocupación, historial de pruebas médicas previas y deportes practicados.

#                     Tareas:
#                     - Determina las coberturas recomendadas para el cliente basándote en su perfil y los documentos disponibles en Azure OpenAI Search.
#                     - Identifica las reglas que un cliente debe cumplir para acceder a las diferentes coberturas.
#                     - Define los rangos de edad para cada cobertura.

#                     Reglas:

#                     - Utiliza Azure AI Search para encontrar las reglas específicas de cada plan de cobertura.
#                     - Considera la edad y ocupación del cliente como criterios prioritarios para determinar las coberturas recomendadas.
#                     - Debes responder siempre en español.
#                     - No inventes reglas, coberturas ni nada que no esté incluido en los documentos.
#                     """


conversation=[{"role": "system", "content": query_prompt_template}]

while True:
    user_input = input("Pregunta:")      
    conversation.append({"role": "user", "content": query_prompt_template_fields})

    response = client.chat.completions.create(
        model=deployment,
        messages=conversation,
        extra_body={
        "dataSources": [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],
                    "key": os.environ["AZURE_AI_SEARCH_API_KEY"],
                    "indexName": os.environ["AZURE_AI_SEARCH_INDEX"]
                }
            }
        ]
    }
 
    )
    # print(response)
    print(response.choices[0].message.content)
    break
    

#    nombre: John Doe, imc: 32.5, profesión: Ingeniero de Software, estado_civil: Casado, edad: 65, nivel_ingresos: Alto, ocupación: A, pruebas_medicas _previas: aceptado, deporte: Correr
