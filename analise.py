import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Função para calcular o desempenho de um time
def calculate_team_performance(data, team, start_year, end_year):
    """
    Calcula métricas de desempenho para um time em um período específico.
    
    Parâmetros:
        data (pd.DataFrame): O dataframe contendo os dados de jogos.
        team (str): O nome do time a ser analisado.
        start_year (int): Ano inicial do período.
        end_year (int): Ano final do período.
    
    Retorna:
        pd.DataFrame: DataFrame com métricas de desempenho por temporada.
    """
    # Filtrar os dados pelo time e período
    filtered_data = data[
        ((data['Home'] == team) | (data['Away'] == team)) & 
        (data['Season'] >= start_year) & (data['Season'] <= end_year)
    ].copy()  # Fazer uma cópia explícita para evitar o aviso

    # Criar colunas para desempenho
    filtered_data.loc[:, 'Victory'] = (
        ((filtered_data['Home'] == team) & (filtered_data['HG'] > filtered_data['AG'])) |
        ((filtered_data['Away'] == team) & (filtered_data['AG'] > filtered_data['HG']))
    ).astype(int)
    filtered_data.loc[:, 'GoalsScored'] = (
        filtered_data['HG'].where(filtered_data['Home'] == team, filtered_data['AG'])
    )
    filtered_data.loc[:, 'GoalsConceded'] = (
        filtered_data['AG'].where(filtered_data['Home'] == team, filtered_data['HG'])
    )

    # Agrupar por temporada
    performance = filtered_data.groupby('Season').agg(
        Victories=('Victory', 'sum'),
        TotalGoalsScored=('GoalsScored', 'sum'),
        TotalGoalsConceded=('GoalsConceded', 'sum'),
        Matches=('Victory', 'count')
    ).reset_index()
    performance['WinRate'] = performance['Victories'] / performance['Matches']
    performance['GoalDifference'] = performance['TotalGoalsScored'] - performance['TotalGoalsConceded']
    return performance

# Função para agrupar o desempenho usando K-means
def cluster_performance(performance):
    """ 
    Agrupa o desempenho usando K-means em 5 clusters, garantindo que o melhor grupo seja o cluster 1.
    """
    scaler = MinMaxScaler()
    features = performance[['WinRate', 'GoalDifference', 'TotalGoalsScored']]
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)  # n_init melhora estabilidade
    performance['Cluster'] = kmeans.fit_predict(scaled_features)

    # Reordenar os clusters para garantir que o melhor desempenho seja o cluster 1
    cluster_means = performance.groupby('Cluster')[['WinRate', 'GoalDifference', 'TotalGoalsScored']].mean()
    sorted_clusters = cluster_means.sort_values(by=['WinRate', 'GoalDifference', 'TotalGoalsScored'], ascending=False)
    
    cluster_mapping = {old: new for new, old in enumerate(sorted_clusters.index, start=1)}
    performance['Cluster'] = performance['Cluster'].map(cluster_mapping)

    return performance

# Carregar o arquivo CSV
file_path = 'BRA.csv'
data = pd.read_csv(file_path)

# Ajustar os tipos de colunas relevantes
data['Season'] = pd.to_numeric(data['Season'], errors='coerce')
data['HG'] = pd.to_numeric(data['HG'], errors='coerce')
data['AG'] = pd.to_numeric(data['AG'], errors='coerce')

# Valores fixos para teste
team = "Flamengo RJ"  # Nome do time fixo
start_year = 2012   # Ano inicial fixo
end_year = 2024     # Ano final fixo

# Calcular desempenho e agrupar
performance = calculate_team_performance(data, team, start_year, end_year)

if performance.empty:
    print(f"Nenhum dado encontrado para o time {team} entre {start_year} e {end_year}.")
else:
    clustered_performance = cluster_performance(performance)
    print(f"\nDesempenho do time {team} entre {start_year} e {end_year} agrupado em clusters:")
    print(clustered_performance[['Season', 'Cluster', 'WinRate', 'GoalDifference', 'TotalGoalsScored']])
    
    # Scatter plot para visualização dos clusters
    plt.figure(figsize=(10, 7))
    for cluster in clustered_performance['Cluster'].unique():
        cluster_data = clustered_performance[clustered_performance['Cluster'] == cluster]
        plt.scatter(cluster_data['WinRate'], cluster_data['GoalDifference'], label=f'Cluster {cluster}', s=100, alpha=0.7)

    plt.title(f'Distribuição de Clusters para o Time {team} ({start_year}-{end_year})')
    plt.xlabel('Taxa de Vitórias (WinRate)')
    plt.ylabel('Diferença de Gols (GoalDifference)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()
