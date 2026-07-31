# Imagem base leve
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema (ajuste conforme sua necessidade)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de dependências primeiro (melhora o cache do build)
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Porta exposta (ajuste conforme sua aplicação)
EXPOSE 6060

# Comando padrão para rodar a aplicação (ajuste conforme necessário)
CMD ["python","main.py"]