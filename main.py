import pandas as pd
import requests
import json
import openai


#Url para acessar a API do Curso
sdw2023_api_url = "https://sdw-2023-prd.up.railway.app"

#Criando a funçao para fazer as requisições e trazer os usuarios cadastrado na API
def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None


###EXTRACT###INICIO

#Criando um dataFrame do documento CSV
dataFrame = pd.read_csv('SDW2023.csv')

#Extraindo os ids de usuários e transformando em uma lista
user_ids = dataFrame['UserID'].to_list()

#Imprimindo a lista na tela
print(user_ids)

#Fazendo uma requisição para a API e gerar a lista de dados com todos os usuarios cadastrados na API
#Utilizando o conceito de list comprehensions
users = [user for id in user_ids if (user := get_user(id)) is not None]

#Imprimindo os dados
print(json.dumps(users, indent=2))

###EXTRACT###FINAL

###TRANSFORM###INICIO
#UserID
#1
#1187
#1213
#1251
#1254
# Documentação Oficial da API OpenAI: https://platform.openai.com/docs/api-reference/introduction
# Informações sobre o Período Gratuito: https://help.openai.com/en/articles/4936830

# Para gerar uma API Key:
# 1. Crie uma conta na OpenAI
# 2. Acesse a seção "API Keys"
# 3. Clique em "Create API Key"
# Link direto: https://platform.openai.com/account/api-keys

openai.api_key = openai_api_key

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "Você é um especialista em marketing bancário e atualmente atua no banco Santander."
            },
            {
                "role": "user", 
                "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres, a mensagem devera ser persoasiva e possui ao menos 3 linhas)"
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')

for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
            "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
            "description": news
        })

###TRANSFORM###FINAL

###LOAD###INICIO

def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False


for user in users:
    success = update_user(user)
    print(f"User {user['name']} update? {success}")

###LOAD###FINAL
