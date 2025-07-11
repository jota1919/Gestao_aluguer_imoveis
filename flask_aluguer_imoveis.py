# -*- coding: utf-8 -*-
"""Flask_aluguer_imoveis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D50-mXNvTvJWAtUOULfViqFOIe5D64Aa
"""

#!pip install pyngrok flask
#!pip install folium
#!pip install gspread
#!ngrok authtoken 2xaXwGP2RC9L0F4Ejti15YRP4Io_7msuBBpvFpd7o71Hpyk7t

from flask import Flask, request, render_template_string, redirect, url_for
# from pyngrok import ngrok
import gspread
import pandas as pd
from google.auth import default
import folium

# Autenticação Google
import gspread
import os
import json
from google.oauth2.service_account import Credentials


scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Cria as credenciais
service_account_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)

# Autentica o gspread
client = gspread.authorize(credentials)


SHEET_ID = "1c0iF-CUNAgAHKCxIOGEPIJqtYTE96I6KZGAmzEIVzr8"  
sh = client.open_by_key(SHEET_ID)






# Flask
app = Flask(__name__)
port = 5000
#public_url = ngrok.connect(port)
#print(f"Aplicação a rodar em: {public_url}")

SENHA_PRIVADA = "1234"

# Função para gerar o mapa
def gerar_mapa(df_imoveis):
    mapa = folium.Map(location=[38.7169, -9.1399], zoom_start=6)
    for _, row in df_imoveis.iterrows():
        try:
            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
            popup = f"{row['Descrição']}<br>{row['Preço/Noite (€)']}€/noite"
            folium.Marker([lat, lon], popup=popup).add_to(mapa)
        except:
            continue
    return mapa._repr_html_()





TEMPLATE_BASE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>{{ titulo }}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        .table th, .table td {
            text-align: center;
            vertical-align: middle;
        }
        body {
            margin: 20px;
        }
        .nav-buttons {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ titulo }}</h1>
        <div class="nav-buttons">
            {% if titulo != "Área Privada - Login" %}
                <a class="btn btn-primary" href="/">Início</a>
            {% endif %}
            {% if titulo == "Imóveis Disponíveis" %}
                <a class="btn btn-secondary" href="/login">Área Privada</a>
            {% endif %}
        </div>
        <hr>
        {{ conteudo|safe }}
            <hr>
        <footer class="text-center mt-4 mb-2">
            <p>
                <a href="https://docs.google.com/document/d/1EfGj96c80u3TvtORRgec7DPwNJGGw42VOKWmxS5EKz4/edit?tab=t.0" target="_blank">Relatório</a> |
                <a href="https://github.com/jota1919/Gestao_aluguer_imoveis" target="_blank">GitHub</a>
            </p>
        </footer>
    </div>
</body>
</html>
"""



@app.route("/")
def home():
    df_imoveis = pd.DataFrame(sh.worksheet("Imoveis").get_all_records())
    mapa_html = gerar_mapa(df_imoveis)
    tabela_html = df_imoveis[["Localização", "Preço/Noite (€)", "Descrição"]].to_html(
        classes='table table-bordered table-hover', index=False, border=0
    )
    conteudo = f"""
    <div class="alert alert-warning" role="alert">
        <strong>Nota:</strong> Os dados apresentados são <u>fictícios</u> e utilizados apenas para fins demonstrativos.
    </div>
    <div id="map-container" style="height: 300px; overflow: hidden; margin-bottom: 20px;">
        {mapa_html}
    </div>
    <div class="tabela-wrapper">
        <h2>Lista de Imóveis</h2>
        <div style="max-height: 300px; overflow-y: auto;">
            {tabela_html}
        </div>
    </div>
    
    """
    return render_template_string(TEMPLATE_BASE, titulo="Imóveis Disponíveis", conteudo=conteudo)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == SENHA_PRIVADA:
            return redirect(url_for("privado"))
        else:
            return render_template_string(TEMPLATE_BASE, titulo="Login", conteudo="<p>Senha incorreta!</p>")
    conteudo = """
    <form method="POST" class="mt-4">
        <input type="password" name="senha" class="form-control mb-2" placeholder="Digite a senha">
        <button type="submit" class="btn btn-primary">Entrar</button>
    </form>
    """
    return render_template_string(TEMPLATE_BASE, titulo="Login - Área Privada", conteudo=conteudo)

import unicodedata

def normalizar(texto):
    if not isinstance(texto, str):
        texto = str(texto)
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()


import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime

@app.route("/privado", methods=["GET", "POST"])
def privado():
    # Atualiza os dados mais recentes da sheet
    df_imoveis = pd.DataFrame(sh.worksheet("Imoveis").get_all_records())
    df_clientes = pd.DataFrame(sh.worksheet("Clientes").get_all_records())
    df_reservas = pd.DataFrame(sh.worksheet("Reservas").get_all_records())

    df_imoveis_filt = df_imoveis.copy()
    df_clientes_filt = df_clientes.copy()
    df_reservas_filt = df_reservas.copy()

    if request.method == "POST":
        local = request.form.get("local")
        preco_min = request.form.get("preco_min")
        preco_max = request.form.get("preco_max")
        nome_cliente = request.form.get("nome_cliente")
        email_cliente = request.form.get("email_cliente")
        email_reserva = request.form.get("email_reserva")

        if local:
            df_imoveis_filt = df_imoveis_filt[df_imoveis_filt["Localização"].apply(
                lambda x: local.lower() in normalizar(x))]
        if preco_min:
            df_imoveis_filt = df_imoveis_filt[df_imoveis_filt["Preço/Noite (€)"] >= float(preco_min)]
        if preco_max:
            df_imoveis_filt = df_imoveis_filt[df_imoveis_filt["Preço/Noite (€)"] <= float(preco_max)]

        if nome_cliente:
            df_clientes_filt = df_clientes_filt[df_clientes_filt["Nome"].apply(
                lambda x: nome_cliente.lower() in normalizar(x))]
        if email_cliente:
            df_clientes_filt = df_clientes_filt[df_clientes_filt["Email"].str.contains(email_cliente, case=False)]

        if email_reserva and "Email_Cliente" in df_reservas_filt.columns:
            df_reservas_filt = df_reservas_filt[df_reservas_filt["Email_Cliente"].astype(str).str.contains(email_reserva, case=False, na=False)]

    # ---------- GERAÇÃO DOS GRÁFICOS ----------

    def gerar_grafico_base64(fig):
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode()

    # Prepara dados
    df_reservas["Data Início"] = pd.to_datetime(df_reservas["Data Início"])
    df_reservas["Data Fim"] = pd.to_datetime(df_reservas["Data Fim"])
    df_reservas["Dias Ocupados"] = (df_reservas["Data Fim"] - df_reservas["Data Início"]).dt.days + 1


    # 2. Reservas por mês
    df_reservas["AnoMes"] = df_reservas["Data Início"].dt.to_period("M").astype(str)
    reservas_mes = df_reservas.groupby("AnoMes").size()

    fig2, ax2 = plt.subplots()
    reservas_mes.plot(kind="bar", ax=ax2, color='#003366')
    ax2.set_title("Reservas por Mês")
    ax2.set_ylabel("Nº de Reservas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    grafico2 = gerar_grafico_base64(fig2)
    plt.close(fig2)

    # 3. Reservas por imóvel
    reservas_imovel = df_reservas["Imóvel (chave)"].value_counts()

    fig3, ax3 = plt.subplots()
    reservas_imovel.plot(kind="pie", autopct='%1.1f%%', startangle=90, ax=ax3)
    ax3.set_ylabel("")
    ax3.set_title("Distribuição de Reservas por Imóvel")
    plt.tight_layout()
    grafico3 = gerar_grafico_base64(fig3)
    plt.close(fig3)

    # ---------- HTML ----------

    filtros_html = """
    <form method="POST" class="mb-4">
        <h4>Filtros de Imóveis</h4>
        <div class="row mb-3">
            <div class="col-md-3"><input type="text" name="local" class="form-control" placeholder="Localização"></div>
            <div class="col-md-2"><input type="number" step="0.01" name="preco_min" class="form-control" placeholder="Preço Mínimo"></div>
            <div class="col-md-2"><input type="number" step="0.01" name="preco_max" class="form-control" placeholder="Preço Máximo"></div>
        </div>
        <h4>Filtros de Clientes</h4>
        <div class="row mb-3">
            <div class="col-md-3"><input type="text" name="nome_cliente" class="form-control" placeholder="Nome do Cliente"></div>
            <div class="col-md-3"><input type="text" name="email_cliente" class="form-control" placeholder="Email"></div>
        </div>
        <h4>Filtros de Reservas</h4>
        <div class="row mb-3">
            <div class="col-md-3"><input type="text" name="email_reserva" class="form-control" placeholder="Email do Cliente"></div>
        </div>
        <div class="row mb-3">
            <div class="col-md-2">
                <button type="submit" class="btn btn-primary w-100">Filtrar</button>
            </div>
            <div class="col-md-2">
                <a href="/privado" class="btn btn-secondary w-100">Repor</a>
            </div>
        </div>
    </form>
    """

    # Tabelas
    tabela_clientes = df_clientes_filt.to_html(classes='table table-striped', index=False)
    tabela_reservas = df_reservas_filt.to_html(classes='table table-striped', index=False)
    tabela_imoveis = df_imoveis_filt.to_html(classes='table table-striped', index=False)

    # Conteúdo HTML final
    conteudo = f"""
    <div class="alert alert-warning" role="alert">
    <strong>Nota:</strong> Os dados apresentados são <u>fictícios</u> e utilizados apenas para fins demonstrativos.
    </div>
    {filtros_html}
   
    
    <h2>Clientes</h2>
    {tabela_clientes}
    <h2>Reservas</h2>
    {tabela_reservas}
    <h2>Imóveis - Detalhes</h2>
    {tabela_imoveis}

     <h2>Gráficos de Análise</h2>
    <div class="row">
        <div class="col-md-6"><img src="data:image/png;base64,{grafico2}" class="img-fluid"></div>
        <div class="col-md-6"><img src="data:image/png;base64,{grafico3}" class="img-fluid"></div>
    </div>
    """

    return render_template_string(TEMPLATE_BASE, titulo="Área Privada", conteudo=conteudo)





#app.run(port=port)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Usa a porta do Render ou 10000 por padrão
    app.run(host="0.0.0.0", port=port)

