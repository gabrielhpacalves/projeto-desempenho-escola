import plotly.express as px

def grafico_barras_situacao(df):
    contagem = df["situacao"].value_counts().reset_index()
    contagem.columns = ["situacao", "quantidade"]
    
    color_map = {'Aprovado': 'blue', 'Em risco': 'red'}
    fig = px.bar(contagem, x="situacao", y="quantidade", color="situacao",
                 text="quantidade",
                 color_discrete_map=color_map,
                 title="Situação dos Alunos na Sala")
    
    fig.update_yaxes(tickformat=".0f")
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    return fig

def grafico_media_por_sala(df):
    medias = df.groupby("sala")[["nota1", "nota2", "nota3"]].mean().reset_index()
    medias["media_geral"] = medias[["nota1", "nota2", "nota3"]].mean(axis=1)
    
    medias['media_geral_str'] = medias['media_geral'].apply(lambda x: f"{x:.1f}".replace('.', ','))

    fig = px.bar(
        medias.sort_values(by="media_geral", ascending=True),
        y="sala",
        x="media_geral",
        orientation='h',
        color="sala",
        text="media_geral_str",
        title="Média Geral de Desempenho por Sala"
    )
    
    fig.update_layout(xaxis_title="Média Geral", yaxis_title="Sala")
    fig.update_xaxes(tickformat=".1f")
    fig.update_traces(textposition='outside')
    return fig

def grafico_media_aluno_por_materia(df_aluno):
    df_aluno['situacao_materia'] = df_aluno['media_materia'].apply(lambda x: 'Aprovado' if x >= 7 else 'Em risco')
    
    df_aluno['media_materia_str'] = df_aluno['media_materia'].apply(lambda x: f"{x:.1f}".replace('.', ','))

    color_map = {'Aprovado': 'blue', 'Em risco': 'red'}
    fig = px.bar(df_aluno.sort_values(by="media_materia", ascending=False),
                 x="materia",
                 y="media_materia",
                 color="situacao_materia",
                 color_discrete_map=color_map,
                 text="media_materia_str",
                 title=f"Média do Aluno {df_aluno['nome_aluno'].iloc[0]} por Matéria")
    
    fig.update_layout(xaxis_title="Matéria", yaxis_title="Média por Matéria")
    fig.update_yaxes(tickformat=".1f")
    fig.update_traces(textposition='outside')
    return fig

def grafico_pizza_situacao_final_alunos(df_situacao_final_sala):
    contagem = df_situacao_final_sala["situacao_final"].value_counts().reset_index()
    contagem.columns = ["situacao_final", "quantidade"]
    
    color_map = {'Acima da média': 'green', 'Abaixo da média': 'red'}
    fig = px.pie(contagem, 
                 values="quantidade", 
                 names="situacao_final", 
                 color="situacao_final",
                 color_discrete_map=color_map,
                 title="Situação Final dos Alunos na Sala",
                 hole=0.3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig