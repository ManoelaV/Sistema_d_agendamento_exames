@echo off
echo ===============================================
echo  Sistema de Agendamento de Exames - Setup
echo ===============================================
echo.

echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado! 
    echo Instale Python 3.7+ em https://python.org
    pause
    exit /b 1
)
echo Python OK!
echo.

echo [2/4] Instalando dependencias...
pip install mysql-connector-python==8.2.0
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar mysql-connector-python
    pause
    exit /b 1
)

pip install ttkbootstrap==1.10.1
if %errorlevel% neq 0 (
    echo AVISO: ttkbootstrap nao instalado, usando interface simplificada
)
echo.

echo [3/4] Verificando MySQL...
echo Certifique-se de que:
echo - MySQL esta rodando
echo - Usuario root tem acesso
echo - Banco 'clinica_exames' foi criado com trabalhoPBD.sql
echo.

echo [4/4] Configuracao pronta!
echo.
echo ===============================================
echo  Para executar o sistema:
echo  python main.py
echo ===============================================
echo.
pause
