import pandas as pd

def agrupar_por_sala(df):
    return df.groupby("sala")[["nota1", "nota2", "nota3"]].mean()

def agrupar_por_professor(df):
    return df.groupby("professor")[["nota1", "nota2", "nota3"]].mean()

def calcular_media_professor(df):
    """Calcula a média geral das notas por professor em todas as salas."""
    medias_prof = df.groupby('professor')[['nota1', 'nota2', 'nota3']].mean().reset_index()
    medias_prof['media_professor'] = medias_prof[['nota1', 'nota2', 'nota3']].mean(axis=1).round(1)
    return medias_prof