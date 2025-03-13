<h1>Análise de Desempenho de Times de Futebol com K-Means</h1>
<p>Este projeto analisa o desempenho de um time de futebol ao longo dos anos, agrupando suas temporadas em clusters com K-Means para identificar padrões de performance.</p>
<hr>

<h3>📌 Funcionalidades</h3>
<ul>
  <li>Carrega dados de jogos a partir de um arquivo CSV.</li>
  <li>Calcula métricas de desempenho do time por temporada (vitórias, gols, taxa de vitórias, etc.).</li>
  <li>Aplica o algoritmo K-Means para agrupar temporadas em 5 clusters.</li>
  <li>Ajusta os clusters para garantir que a melhor temporada esteja no Cluster 1.</li>
  <li>Gera um gráfico para visualização dos clusters.</li>
</ul>
<h3>🛠️ Tecnologias Utilizadas</h3>
<ul>
  <li>Python 3</li>
  <li>Pandas</li>
  <li>Scikit-learn</li>
  <li>Matplotlib</li>
</ul>
<h3>Exemplo de Saída:</h3>
  <br>
<table>
    <tr>
        <th>Season</th>
        <th>Cluster</th>
        <th>WinRate</th>
        <th>GoalDifference</th>
        <th>TotalGoalsScored</th>
    </tr>
    <tr>
        <td>2012</td>
        <td>3</td>
        <td>0.421</td>
        <td>-10</td>
        <td>38</td>
    </tr>
    <tr>
        <td>2019</td>
        <td>1</td>
        <td>0.789</td>
        <td>48</td>
        <td>86</td>
    </tr>
    <tr>
        <td>2022</td>
        <td>2</td>
        <td>0.526</td>
        <td>8</td>
        <td>52</td>
    </tr>
</table>

<hr>
<h3>Autor</h3>
<h4>Lucas Benini de Andrade</h4>
<p>Projeto acadêmico semestral entregue em Dezembro de 2024.</p>
