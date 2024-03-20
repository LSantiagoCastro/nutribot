import os
from openai import AzureOpenAI
import openai
import dotenv

dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT_COMPLETIONS")
api_key = os.environ.get("AZURE_OPENAI_API_KEY_COMPLETION")
deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_ID")

client = AzureOpenAI(
  azure_endpoint = "https://ai-openai-00.openai.azure.com/", 
  api_key=os.getenv("AZURE_OPENAI_API_KEY_COMPLETION"),  
  api_version="2024-02-15-preview"
)


query_prompt_template = """
                        Esta es una IA llamada Nutribot, que tiene la tarea de indagar informacion del usuario como peso, altura, habitos y lo que la ia considere 
                        necesario para realizar el plan de alimentacion nutritiva para la semana, detalladamente cada receta para desayuno, 
                        almuerzo y cena de toda la semana. 
"""
conversation=[{"role": "system", "content": query_prompt_template}]

while True:
    user_input = input("You:")
    user_input_prompt_template = f"""
                        Esta es una conversacion entre una IA muy amigable 🥰 llamada Nutribot y un humano, Nutribot tiene la tarea de indagar informacion del usuario como peso, altura, habitos y lo que la ia considere 
                        necesario para realizar el plan de alimentacion nutritiva para la semana, detalladamente cada receta para desayuno, almuerzo y cena de toda la semana. 
                        
                        Historial de mensajes de la conversacion:
                        {str(conversation)}
                        
                        humano:
                        {str(user_input)}
                        
"""
    
    if 'salir' in str(user_input):
        break
    
    conversation.append({"role": "user", "content": user_input_prompt_template})

    completion = client.chat.completions.create(
    model="gpt-35-turbo-16k", # model = "deployment_name"
    messages = conversation,
    temperature=0.1,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )

    # print(completion)
    print('ai: ',completion.choices[0].message.content,'\n')
    



