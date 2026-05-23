# Ouropaes Campo CRM - MVP

Sistema de gestao comercial e inteligencia de campo para consultores da Ouropaes.
Este MVP permite registar estabelecimentos, acompanhar a prospeccao no mapa, gerir o CRM e gerar estrategias com apoio de IA.

## Tecnologias
- Front-end: HTML5, CSS3, JavaScript vanilla
- Mapa: Leaflet + OpenStreetMap
- Back-end: Python, FastAPI, Uvicorn
- Banco de dados: SQLite
- IA: integracao com Anthropic Claude API

## Estrutura do projeto
- backend/main.py
- backend/requirements.txt
- backend/reset_db.py
- backend/ouropaes.db
- ouropoes_campo_v4.html
- ouropoes_pitch.html

## Como executar localmente

### 1. Iniciar o servidor backend
Abra um terminal dentro da pasta backend e execute:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

A API fica disponivel em http://localhost:8000 e a documentacao interativa em http://localhost:8000/docs.

### 2. Abrir o front-end
Voce pode abrir o arquivo ouropoes_campo_v4.html diretamente no navegador.
Se preferir um servidor local simples, rode na raiz do projeto:

```bash
python3 -m http.server 8001
```

Depois abra http://localhost:8001/ouropoes_campo_v4.html.

### 3. Limpar a base de dados
Para zerar os registros de teste antes de uma demonstracao:

```bash
cd backend
python3 reset_db.py
```

### 4. Ativar a IA no navegador
O front-end procura a chave da Anthropic em localStorage.
Abra o DevTools do navegador e execute:

```javascript
localStorage.setItem('ANTHROPIC_API_KEY', 'sua-chave')
```

Depois recarregue a pagina e use o botao Gerar com IA.

### 5. Usar o mapa gratuito
O CRM usa Leaflet com OpenStreetMap, sem chave e sem custo.
Se o CDN estiver indisponivel, o sistema cai automaticamente no mapa SVG de fallback para nao quebrar a demonstracao.

## Roteiro rapido de demonstracao
1. Mostrar o mapa e o painel lateral.
2. Criar um novo estabelecimento.
3. Recarregar a pagina e mostrar que o dado persiste.
4. Abrir o item, editar os dados e salvar.
5. Gerar a estrategia com IA, se a chave estiver configurada.
6. Mostrar o dashboard com o resumo comercial.

## Entrega
Para empacotar o projeto, inclua estes itens na entrega final:
- backend/
- ouropoes_campo_v4.html
- ouropoes_pitch.html
- README.md
