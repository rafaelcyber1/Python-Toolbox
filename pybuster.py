import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import random

# Lista de proxies para usar
PROXIES_LIST = [
    'http://173.249.23.14:80',
    'http://8.221.138.111:80',
    'http://8.221.139.222:8008',
    'http://47.91.109.17:8008',
    'http://195.54.171.228:25124',
    'http://160.86.242.23:8080',
    'http://45.119.133.218:3128',
    'http://35.185.196.38:3128',
    'http://68.183.149.126:11010',
    'http://20.44.189.184:3129',
    'http://4.234.52.159:8080',
    'http://4.159.24.156:8080',
    'http://203.115.101.55:80'
]

class ProxyChainAdapter(HTTPAdapter):
    def __init__(self, proxies_list, *args, **kwargs):
        self.proxies_list = proxies_list
        super(ProxyChainAdapter, self).__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        proxy = random.choice(self.proxies_list)
        request.proxies = {
            'http': proxy,
            'https': proxy
        }
        return super(ProxyChainAdapter, self).send(request, **kwargs)

def check_directory(url, directory, proxies_list=None):
    session = requests.Session()
    
    if proxies_list:
        adapter = ProxyChainAdapter(proxies_list)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
    else:
        session.proxies = {}

    try:
        response = session.get(url + directory)
        if response.status_code == 200:
            print(f'[+] Diretório encontrado: {url}{directory}')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao acessar {url}{directory}: {e}')

def main():
    use_proxies = input("Deseja usar proxies? (s/n): ").strip().lower()

    if use_proxies not in ['s', 'n']:
        print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")
        return

    # Inicializa a lista de proxies
    proxies_list = None

    if use_proxies == 's':
        proxy_choice = input("Digite o proxy a ser usado (ou deixe em branco para usar um proxy aleatório): ").strip()
        if proxy_choice:
            proxies_list = [proxy_choice]
        else:
            proxies_list = PROXIES_LIST

    url = input("Digite a URL para o pybuster: ").strip()
    wordlist_path = input("Digite o caminho para o arquivo de lista de palavras: ").strip()

    try:
        with open(wordlist_path, 'r') as file:
            directories = file.read().splitlines()

        for directory in directories:
            check_directory(url, directory, proxies_list)

    except FileNotFoundError:
        print(f'Arquivo {wordlist_path} não encontrado.')

if __name__ == "__main__":
    main()
