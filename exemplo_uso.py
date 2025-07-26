"""
Exemplo de uso do Sistema de Agendamento de Exames
"""

import sys
import os

# Adicionar o diretório do projeto ao path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

def test_database_connection():
    """Testar conexão com o banco de dados"""
    print("=== TESTE DE CONEXÃO ===")
    
    try:
        from database import DatabaseConnection
        
        db = DatabaseConnection()
        
        print("Configuração atual:")
        print(f"Host: {db.config['host']}")
        print(f"Database: {db.config['database']}")
        print(f"User: {db.config['user']}")
        print(f"Password: {'*' * len(db.config['password']) if db.config['password'] else 'Vazia'}")
        print()
        
        print("Testando conexão...")
        if db.test_connection():
            print("✅ Conexão estabelecida com sucesso!")
            return True
        else:
            print("❌ Falha na conexão!")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_models():
    """Testar operações básicas do modelo"""
    print("\n=== TESTE DE MODELOS ===")
    
    try:
        from models import ClinicaModel
        
        model = ClinicaModel()
        
        # Testar busca de pacientes
        print("Testando busca de pacientes...")
        pacientes = model.get_pacientes()
        if pacientes:
            print(f"✅ Encontrados {len(pacientes)} pacientes")
            print(f"   Exemplo: {pacientes[0]['nome']} - {pacientes[0]['cpf']}")
        else:
            print("⚠️ Nenhum paciente encontrado")
        
        # Testar busca de exames
        print("Testando busca de exames...")
        exames = model.get_exames()
        if exames:
            print(f"✅ Encontrados {len(exames)} exames")
            print(f"   Exemplo: {exames[0]['nome']} - {exames[0]['tipo']}")
        else:
            print("⚠️ Nenhum exame encontrado")
        
        # Testar agendamentos
        print("Testando busca de agendamentos...")
        agendamentos = model.get_agendamentos()
        if agendamentos:
            print(f"✅ Encontrados {len(agendamentos)} agendamentos")
            print(f"   Exemplo: {agendamentos[0]['paciente_nome']} - {agendamentos[0]['exame_nome']}")
        else:
            print("⚠️ Nenhum agendamento encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos modelos: {e}")
        return False

def launch_gui():
    """Tentar executar a interface gráfica"""
    print("\n=== EXECUTANDO INTERFACE ===")
    
    try:
        print("Tentando carregar interface completa (ttkbootstrap)...")
        from gui_main import ClinicaGUI
        
        app = ClinicaGUI()
        print("✅ Interface completa carregada!")
        print("🚀 Iniciando aplicação...")
        
        app.run()
        
    except ImportError as e:
        print(f"⚠️ ttkbootstrap não disponível: {e}")
        print("Tentando interface simplificada...")
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # Esconder janela principal temporariamente
            
            messagebox.showinfo("Sistema de Agendamento", 
                              "Interface simplificada iniciaria aqui.\n"
                              "Para a versão completa, instale:\n"
                              "pip install ttkbootstrap")
            
            print("✅ Interface simplificada funcionaria!")
            
        except Exception as e2:
            print(f"❌ Erro na interface simplificada: {e2}")
            
    except Exception as e:
        print(f"❌ Erro geral na interface: {e}")

def main():
    """Função principal de exemplo"""
    print("🏥 SISTEMA DE AGENDAMENTO DE EXAMES")
    print("=" * 50)
    
    # Teste 1: Conexão com banco
    if not test_database_connection():
        print("\n❌ FALHA NA CONEXÃO COM O BANCO")
        print("Verifique se:")
        print("- MySQL está rodando")
        print("- Banco 'clinica_exames' existe")
        print("- Execute: mysql -u root -p < trabalhoPBD.sql")
        print("- Configure corretamente em db_config.json")
        return
    
    # Teste 2: Modelos de dados
    if not test_models():
        print("\n❌ FALHA NOS MODELOS DE DADOS")
        print("Certifique-se de que o banco foi criado corretamente")
        return
    
    # Teste 3: Interface gráfica
    print("\n✅ TESTES BÁSICOS PASSARAM!")
    
    resposta = input("\nDeseja executar a interface gráfica? (s/n): ").lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        launch_gui()
    else:
        print("Sistema pode ser executado com: python main.py")

if __name__ == "__main__":
    main()
