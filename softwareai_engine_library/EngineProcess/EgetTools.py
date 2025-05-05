import requests
import yaml
import time
import json
import os
import zipfile
import importlib

def download_tools_zip(tool_ids: list, extract_dir = os.path.join(os.path.dirname(__file__), 'Functions')) -> bool:
   """
   Faz o download do ZIP contendo os arquivos .py de múltiplas ferramentas.
   Após o download, extrai para a pasta 'Functions'.

   :param tool_ids: Lista com os IDs das ferramentas.
   :param output_path: Caminho de saída do arquivo ZIP.
   :param base_url: URL base da API.
   :return: True se tudo foi bem-sucedido, False caso contrário.
   """
   for i in range(10):
        
    output_path = 'tools_code.zip'
    base_url = 'https://softwareai-library-hub.rshare.io'
    joined_ids = ','.join(tool_ids)
    url = f'{base_url}/api/tool-code/{joined_ids}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)

            # Extrai o ZIP para a pasta Functions
            
            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(output_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            return True

        else:
            print(f"Erro {response.status_code}: {response.json()}")
            time.sleep(5)
            continue

    except Exception as e:
        print(f"Erro durante o download ou extração: {e}")
        time.sleep(5)
        continue

def import_tool(tool_name: str, base_dir = os.path.join(os.path.dirname(__file__), "..", 'Functions')):
    """
    Importa dinamicamente o módulo da ferramenta e retorna o objeto decorado com @function_tool.
    """
    module_path = os.path.join(base_dir, tool_name, f"{tool_name}.py")
    spec = importlib.util.spec_from_file_location(tool_name, module_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Procura por função decorada com @function_tool (tem atributo .name)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, "name") and hasattr(attr, "description"):
                return attr

        raise ImportError(f"Nenhuma função decorada com @function_tool encontrada em {tool_name}.py")
    else:
        raise ImportError(f"Não foi possível importar a ferramenta: {tool_name}")


def Egetoolsv2(functionstools = ['autosave']):
    #    # Define diretório base como o do script
    #    os.chdir(os.path.dirname(__file__))

    # Lista de tools que você deseja baixar
    tools = functionstools

    download_tools_zip(tools, extract_dir = os.path.join(os.path.dirname(__file__), "..", 'Functions'))

    os.remove("tools_code.zip")

    # Importa dinamicamente cada ferramenta
    imported_tools = [import_tool(tool) for tool in tools]
    return imported_tools

def EgetTools(tools_name_str = "autoapprovepullrequest,autochangesrequestedinpullrequest,autoconversationpullrequest"
              
    ):

    def format_tool(tool):
        return {
            "type": "function",
            "function": {
                "name": tool["id"],
                "description": tool["fullDescription"].replace("\n", "").replace("", ""),
                "parameters": tool["parameters"]
            },
            
        }

    tool_ids = [name.strip() for name in tools_name_str.split(',')]

    # Pega ferramentas via API
    response = requests.post('https://softwareai-library-hub.rshare.io/api/get-tools-by-id', json={"tool_ids": tool_ids})
    tools_data = response.json()

    # Formata cada ferramenta no formato de função
    formatted_tools = [format_tool(tool) for tool in tools_data]
    return formatted_tools, json.dumps(formatted_tools, indent=2)


# from softwareai_engine_library.EngineProcess.EgetTools import Egetoolsv2
# Egetoolsv2(functionstools = ['autosave', 'autobuildpdf'])
# tools_name_str = "autosave,send_to_webhook_func,autopullrequest"
# Tools_Name_dict, Tools_Name_str = EgetTools(tools_name_str)
# print(Tools_Name_dict)
# print(Tools_Name_str)
