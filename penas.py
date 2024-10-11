import requests

def get_page_html(url):
    try:
        res = requests.get(url)
        res.raise_for_status()  # Levanta um erro para códigos de status HTTP de erro
        return res.text
    except requests.exceptions.RequestException as e:
        print(f'Erro ao acessar {url}: {e}')

# Exemplo de uso
url = 'https://www.beforward.jp/pt/mitsubishi/rosa/bt708798/id/8101296/'
html_content = get_page_html(url)
print(html_content)
