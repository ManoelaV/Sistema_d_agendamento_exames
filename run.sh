#!/bin/bash

# Script para executar o Sistema de Agendamento de Exames
# Automaticamente ativa o ambiente virtual e executa o sistema

echo "🏥 Sistema de Agendamento de Exames"
echo "======================================"

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
    
    echo "📥 Instalando dependências..."
    ./venv/bin/pip install -r requirements.txt
    echo "✅ Dependências instaladas!"
fi

# Ativar ambiente virtual e executar
echo "🚀 Iniciando sistema..."
./venv/bin/python main.py
