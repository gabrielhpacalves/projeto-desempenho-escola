# Análise de Desempenho Escolar

Este projeto Streamlit permite analisar o desempenho de alunos a partir de um arquivo CSV.

## Funcionalidades
- Upload de arquivo CSV com dados de alunos.
- Visualização da média de desempenho por professor.
- Ranking dos top 10 alunos da escola.
- Análise detalhada por sala, incluindo situação final dos alunos e média por matéria.
- Consulta individual do desempenho de um aluno.

## Como Usar
1. Faça o upload do seu arquivo CSV na interface do Streamlit.
2. Certifique-se de que o CSV contém as colunas necessárias: `nome_aluno`, `sala`, `materia`, `professor`, `nota1`, `nota2`, `nota3`.
3. Explore os gráficos e tabelas gerados automaticamente.

## Estrutura do Projeto
- `app.py`: O arquivo principal da aplicação Streamlit.
- `processamento_alunos.py`: Contém funções para cálculo e processamento de dados dos alunos.
- `visualizacao_alunos.py`: Contém funções para gerar os gráficos utilizando Plotly Express.

## Tecnologias Utilizadas
- Python
- Streamlit
- Pandas
- Plotly Express
