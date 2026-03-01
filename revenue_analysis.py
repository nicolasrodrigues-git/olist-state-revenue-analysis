# ================================================
# Projeto: Análise de Receita por Estado (Modular)
# ================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Funções úteis
# -------------------------------

def load_data(path):
    """Carrega o CSV e retorna DataFrame"""
    df = pd.read_csv(path)
    return df

def inspect_data(df):
    """Mostra primeiras linhas, info, describe e nulos"""
    print("=== Primeiras linhas ===")
    print(df.head(), "\n")
    print("=== Info ===")
    print(df.info(), "\n")
    print("=== Estatísticas descritivas ===")
    print(df.describe(), "\n")
    print("=== Valores nulos ===")
    print(df.isnull().sum(), "\n")

def compute_stats(df):
    """Calcula total, média, mediana, top e bottom 5"""
    total = df['revenue'].sum()
    mean = df['revenue'].mean()
    median = df['revenue'].median()
    print(f"Receita total: R$ {total:,.2f}")
    print(f"Média de receita por estado: R$ {mean:,.2f}")
    print(f"Mediana de receita por estado: R$ {median:,.2f}\n")
    
    print("Top 5 estados por receita:")
    print(df.head(5), "\n")
    print("Bottom 5 estados por receita:")
    print(df.tail(5), "\n")

def create_colors(df):
    """Cria cores graduais com viridis"""
    return plt.cm.viridis(df['revenue'] / df['revenue'].max())

def plot_bar_vertical(df, colors, save_path=None):
    plt.figure(figsize=(12,6))
    plt.bar(df["customer_state"], df["revenue"], color=colors)
    plt.xticks(rotation=90)
    plt.title("Receita por Estado (Vertical)")
    plt.xlabel("Estado")
    plt.ylabel("Receita")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_bar_horizontal(df, colors, save_path=None):
    plt.figure(figsize=(10,8))
    plt.barh(df["customer_state"], df["revenue"], color=colors)
    plt.xlabel("Receita")
    plt.ylabel("Estado")
    plt.title("Receita por Estado (Horizontal)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_pie_top(df, top_n=5, save_path=None):

    # Trabalhar com cópia para evitar modificar o df original
    df_copy = df.copy()
    df_copy['perc_contribution'] = (
        df_copy['revenue'] / df_copy['revenue'].sum() * 100
    )

    top_states = df_copy.head(top_n)

    print(f"Top {top_n} estados com percentual de contribuição:")
    print(top_states[['customer_state', 'revenue', 'perc_contribution']], "\n")

    plt.figure(figsize=(8, 8))
    plt.pie(
        top_states['revenue'],
        labels=top_states['customer_state'],
        autopct='%1.1f%%',
        colors=plt.cm.viridis(
            top_states['revenue'] / top_states['revenue'].max()
        )
    )

    plt.title(f"Top {top_n} Estados - Participação na Receita")

    if save_path:
        plt.savefig(save_path)

    plt.show()
    
# -------------------------------
# Execução do projeto
# -------------------------------

# Caminho para os dados
data_path = "data/processed/abc_state_revenue.csv"

# Criar pasta de relatórios caso não exista
report_dir = "reports"
os.makedirs(report_dir, exist_ok=True)

# 1️⃣ Carregar dados
df = load_data(data_path)

# 2️⃣ Inspecionar dados
inspect_data(df)

# 3️⃣ Ordenar por receita decrescente
df = df.sort_values(by="revenue", ascending=False)

# 4️⃣ Criar cores graduais
colors = create_colors(df)

# 5️⃣ Estatísticas
compute_stats(df)

# 6️⃣ Gráficos
plot_bar_vertical(df, colors, save_path=os.path.join(report_dir, "bar_vertical.png"))
plot_bar_horizontal(df, colors, save_path=os.path.join(report_dir, "bar_horizontal.png"))
plot_pie_top(df, top_n=5, save_path=os.path.join(report_dir, "top5_pie.png"))


# -------------------------------
# Gerar tabelas prontas para README
# -------------------------------

# Certifique-se que df já está ordenado por revenue decrescente
top_5 = df.head(5).copy()
bottom_5 = df.tail(5).copy()

# Percentual de contribuição para top 5
top_5['perc_contribution'] = top_5['revenue'] / df['revenue'].sum() * 100

# Criar strings em formato de tabela Markdown
top_5_table = ""
for idx, row in top_5.iterrows():
    top_5_table += f"| {row['customer_state']} | R$ {row['revenue']:,.2f} | {row['perc_contribution']:.1f}% |\n"

bottom_5_table = ""
for idx, row in bottom_5.iterrows():
    bottom_5_table += f"| {row['customer_state']} | R$ {row['revenue']:,.2f} |\n"

print("=== Tabela Top 5 pronta para README ===")
print(top_5_table)
print("=== Tabela Bottom 5 pronta para README ===")
print(bottom_5_table)
