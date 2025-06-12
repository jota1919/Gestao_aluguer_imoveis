# 🏡 Gestão de Aluguer de Imóveis - Grupo 6

Este projeto é uma aplicação web desenvolvida em Flask que permite a visualização de imóveis para aluguer, com acesso a dados em tempo real através de uma folha de cálculo Google Sheets. 
Inclui uma área pública e uma área privada com filtros, análises e gráficos.

👥 Autores
Este projeto foi desenvolvido no âmbito da unidade curricular de Metedologias Ágeis.

Catarina Silva
Ana Martins
Daniel Teixeira da Silva
João Pedro Pinto Costa 

## 🔍 Funcionalidades

### Área Pública
- Visualização de imóveis disponíveis com:
  - Mapa interativo (Folium)
  - Lista de imóveis com localização, descrição e preço por noite
- Aviso visível de que os dados apresentados são fictícios
- Rodapé com links para este repositório e relatório de desenvolvimento

### Área Privada (acesso com senha)
- Acesso via `/login` com palavra passe definida no código (`SENHA_PRIVADA`)
- Filtros avançados por:
  - Localização
  - Preço mínimo e máximo
  - Nome ou email do cliente
  - Email do cliente nas reservas
- Tabelas detalhadas de:
  - Clientes
  - Reservas
  - Imóveis
- Gráficos analíticos:
  - Reservas por mês 
  - Distribuição de reservas por imóvel
- Nota visível de que os dados apresentados são fictícios
- Rodapé com links úteis

---

## 🗂 Estrutura das Google Sheets

O projeto está ligado a uma Google Sheet com várias folhas:

### 1. Imóveis
| Localização | Preço/Noite (€) | Descrição | Latitude | Longitude |
|-------------|------------------|------------|----------|-----------|

### 2. Clientes
| Nome | Email | Telefone | NIF |
|------|-------|----------|-----|

### 3. Reservas
| Email_Cliente | Imóvel (chave) | Data Início | Data Fim | Custo (€) |
|---------------|----------------|-------------|----------|------------|

> 🔐 O campo "Imóvel (chave)" deve ser uma chave coerente que identifique o imóvel nas reservas (ex: `Lisboa - T2 com varanda`).
> 
> 📎 Links Úteis
> Página Render: https://mads-grupo6.onrender.com
> 
> Relatório de desenvolvimento: https://docs.google.com/document/d/1EfGj96c80u3TvtORRgec7DPwNJGGw42VOKWmxS5EKz4/edit?tab=t.0
