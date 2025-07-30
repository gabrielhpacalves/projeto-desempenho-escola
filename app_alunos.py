import streamlit as st
import pandas as pd
from processamento_alunos import calcular_media_professor
from visualizacao_alunos import grafico_barras_situacao, grafico_media_por_sala, grafico_media_aluno_por_materia, grafico_pizza_situacao_final_alunos
import plotly.express as px
import io
import time

st.set_page_config(page_title="Desempenho de Alunos", layout="wide")
st.title("📚 Análise de Desempenho da Escola")

st.markdown("---")
st.header("📤 Faça o Upload do Arquivo de Dados dos Alunos")

uploaded_file = st.file_uploader("Arraste e solte seu arquivo CSV aqui ou clique para procurar", type=["csv"])

df = None

if uploaded_file is not None:
    with st.spinner('Carregando e processando o arquivo... Por favor, aguarde 5 segundos!'):
        time.sleep(5)
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = ['nome_aluno', 'sala', 'materia', 'professor', 'nota1', 'nota2', 'nota3']
        if not all(col in df.columns for col in required_columns):
            st.error(f"O arquivo CSV deve conter as seguintes colunas: {', '.join(required_columns)}. Por favor, verifique o arquivo e tente novamente.")
            df = None
        
        else:
            df['media_materia'] = df[['nota1', 'nota2', 'nota3']].mean(axis=1).round(1)
            df['media_geral_aluno'] = df[['nota1', 'nota2', 'nota3']].mean(axis=1).round(1)
            df['situacao'] = df['media_geral_aluno'].apply(lambda x: 'Aprovado' if x >= 7 else 'Em risco')

            df_alunos_final_media = df.groupby('nome_aluno')[['nota1', 'nota2', 'nota3']].mean().reset_index()
            df_alunos_final_media['media_final_total'] = df_alunos_final_media[['nota1', 'nota2', 'nota3']].mean(axis=1).round(1)
            df_alunos_final_media['situacao_final'] = df_alunos_final_media['media_final_total'].apply(lambda x: 'Acima da média' if x >= 7 else 'Abaixo da média')
            df_alunos_final_media['media_final_total_str'] = df_alunos_final_media['media_final_total'].apply(lambda x: f"{x:.1f}".replace('.', ','))

            df_media_professor = calcular_media_professor(df)
            df_media_professor['media_professor_str'] = df_media_professor['media_professor'].apply(lambda x: f"{x:.1f}".replace('.', ','))

            top_10_alunos = df_alunos_final_media.sort_values(by='media_final_total', ascending=False).head(10)
            top_10_alunos['ranking'] = range(1, len(top_10_alunos) + 1)
            top_10_alunos['media_final_total_str'] = top_10_alunos['media_final_total'].apply(lambda x: f"{x:.1f}".replace('.', ','))
            
            st.markdown("---")
            st.markdown("## 📊 Visão Geral da Escola")
            col_geral1, col_geral2 = st.columns(2)

            with col_geral1:
                st.subheader("Média de Desempenho por Professor")
                fig_professores = px.bar(
                    df_media_professor.sort_values(by="media_professor", ascending=True),
                    y="professor",
                    x="media_professor",
                    orientation='h',
                    text="media_professor_str",
                    title="Média por Professor (Todas as Salas)"
                )
                fig_professores.update_layout(xaxis_title="Média Geral", yaxis_title="Professor")
                fig_professores.update_xaxes(tickformat=".1f")
                fig_professores.update_traces(textposition='outside')
                st.plotly_chart(fig_professores, use_container_width=True, height=450)

            with col_geral2:
                st.subheader("🏆 Top 10 Alunos da Escola")
                fig_top10 = px.bar(
                    top_10_alunos.sort_values(by='media_final_total', ascending=False),
                    x="nome_aluno",
                    y="media_final_total",
                    orientation='v',
                    text="media_final_total_str",
                    title="Top 10 Alunos (Média Final Total)",
                    color="media_final_total",
                    color_continuous_scale=["blue", "yellow", "hotpink"],
                )
                fig_top10.update_layout(xaxis_title="Aluno", yaxis_title="Média Geral Final")
                fig_top10.update_yaxes(tickformat=".1f")
                fig_top10.update_traces(textposition='outside')
                fig_top10.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig_top10, use_container_width=True, height=450)

            st.markdown("---")

            if 'sala' in df.columns:
                sala = st.selectbox("Escolha uma sala para análise detalhada:", sorted(df["sala"].unique()))

                df_sala = df[df["sala"] == sala]

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📈 Situação Final dos Alunos por Sala")
                    alunos_da_sala_selecionada = df_sala['nome_aluno'].unique()
                    df_situacao_final_sala = df_alunos_final_media[df_alunos_final_media['nome_aluno'].isin(alunos_da_sala_selecionada)]
                    st.plotly_chart(grafico_pizza_situacao_final_alunos(df_situacao_final_sala), use_container_width=True, height=450)

                with col2:
                    st.subheader("📊 Média Geral (Escola)")
                    st.plotly_chart(grafico_media_por_sala(df), use_container_width=True, height=450)

                st.markdown("### 📋 Média Geral Final dos Alunos")

                alunos_da_sala_selecionada = df_sala['nome_aluno'].unique()
                df_para_grafico_final = df_alunos_final_media[df_alunos_final_media['nome_aluno'].isin(alunos_da_sala_selecionada)]

                fig_media_final_alunos = px.bar(
                    df_para_grafico_final.sort_values(by="media_final_total", ascending=False),
                    x="nome_aluno",
                    y="media_final_total",
                    color="situacao_final",
                    color_discrete_map={'Acima da média': 'green', 'Abaixo da média': 'red'},
                    text="media_final_total_str",
                    title=f"Média Geral FINAL dos Alunos da Sala {sala}"
                )
                fig_media_final_alunos.update_layout(xaxis_title="Aluno", yaxis_title="Média Geral Final")
                fig_media_final_alunos.update_yaxes(tickformat=".1f")
                st.plotly_chart(fig_media_final_alunos, use_container_width=True, height=450)

                st.markdown(f"### 📊 Média por Matéria e Professor (Sala {sala})")
                medias_materia_prof = (
                    df_sala.groupby(["materia", "professor"])[["nota1", "nota2", "nota3"]]
                    .mean()
                    .round(1)
                    .reset_index()
                )
                medias_materia_prof["media_geral"] = medias_materia_prof[["nota1", "nota2", "nota3"]].mean(axis=1).round(1)

                medias_materia_prof['situacao'] = medias_materia_prof['media_geral'].apply(lambda x: 'Aprovado' if x >= 7 else 'Em risco')

                st.dataframe(medias_materia_prof[['materia', 'professor', 'media_geral', 'situacao']] \
                    .sort_values(by="materia") \
                    .style.applymap(
                        lambda x: 'background-color: #ffe6e6' if x == 'Em risco' else ('background-color: #e6f7ff' if x == 'Aprovado' else ''),
                        subset=['situacao']
                    )
                    .format(precision=1, decimal=',', thousands='.')
                )

                st.markdown("### 🔍 Consultar desempenho de um aluno")
                alunos_sala = df_sala["nome_aluno"].unique()
                aluno_escolhido = st.selectbox("Selecione um aluno:", sorted(alunos_sala))

                df_aluno = df_sala[df_sala["nome_aluno"] == aluno_escolhido]

                if not df_aluno.empty:
                    st.plotly_chart(grafico_media_aluno_por_materia(df_aluno), use_container_width=True)

                    st.dataframe(df_aluno[['materia', 'professor', 'nota1', 'nota2', 'nota3', 'media_geral_aluno', 'situacao']] \
                        .sort_values(by="materia") \
                        .style.applymap(
                            lambda x: 'background-color: #ffe6e6' if x == 'Em risco' else ('background-color: #e6f7ff' if x == 'Aprovado' else ''),
                            subset=['situacao']
                        )
                        .format(precision=1, decimal=',', thousands='.')
                    )
            else:
                st.warning("O arquivo carregado não contém a coluna 'sala' ou está vazio. Por favor, verifique os dados.")

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}. Por favor, verifique se o arquivo é um CSV válido e se as colunas estão corretas.")
else:
    st.info("Por favor, faça o upload de um arquivo CSV para começar a análise.")