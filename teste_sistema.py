#!/usr/bin/env python3
"""
Teste rápido do sistema para verificar se tudo está funcionando
"""

import sys
import os

# Adicionar path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def teste_basico():
    """Teste básico de funcionamento"""
    print("🔧 TESTE BÁSICO DO SISTEMA")
    print("=" * 40)
    
    # Teste 1: Importação dos módulos
    print("1️⃣ Testando importações...")
    try:
        from database import DatabaseConnection
        print("✅ database.py - OK")
        
        from models import ClinicaModel
        print("✅ models.py - OK")
        
        from gui_simples import ClinicaGUISimples
        print("✅ gui_simples.py - OK")
        
        try:
            import ttkbootstrap
            from gui_main import ClinicaGUI
            print("✅ gui_main.py - OK (interface completa disponível)")
            interface_completa = True
        except ImportError:
            print("⚠️ gui_main.py - Não disponível (ttkbootstrap não instalado)")
            interface_completa = False
            
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False
    
    # Teste 2: Conexão com banco
    print("\n2️⃣ Testando conexão com banco...")
    try:
        db = DatabaseConnection()
        print(f"📋 Configuração atual:")
        print(f"   Host: {db.config['host']}")
        print(f"   Database: {db.config['database']}")
        print(f"   User: {db.config['user']}")
        print(f"   Password: {'*' * len(db.config['password']) if db.config['password'] else 'Vazia'}")
        
        if db.test_connection():
            print("✅ Conexão com banco - OK")
            conexao_ok = True
        else:
            print("❌ Conexão com banco - FALHOU")
            print("   Verifique se MySQL está rodando e configuração está correta")
            conexao_ok = False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        conexao_ok = False
    
    # Teste 3: Modelos de dados
    if conexao_ok:
        print("\n3️⃣ Testando modelos de dados...")
        try:
            model = ClinicaModel()
            
            # Testar pacientes
            pacientes = model.get_pacientes()
            print(f"✅ Pacientes: {len(pacientes) if pacientes else 0} encontrados")
            
            # Testar exames
            exames = model.get_exames()
            print(f"✅ Exames: {len(exames) if exames else 0} encontrados")
            
            # Testar agendamentos
            agendamentos = model.get_agendamentos()
            print(f"✅ Agendamentos: {len(agendamentos) if agendamentos else 0} encontrados")
            
            modelos_ok = True
            
        except Exception as e:
            print(f"❌ Erro nos modelos: {e}")
            modelos_ok = False
    else:
        modelos_ok = False
    
    # Teste 4: Interface (sem executar)
    print("\n4️⃣ Testando interface...")
    try:
        if interface_completa:
            app_completa = ClinicaGUI()
            print("✅ Interface completa pode ser criada")
        
        app_simples = ClinicaGUISimples()
        print("✅ Interface simplificada pode ser criada")
        interface_ok = True
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        interface_ok = False
    
    # Resumo
    print("\n" + "=" * 40)
    print("📊 RESUMO DOS TESTES:")
    print(f"   Importações: {'✅ OK' if True else '❌ ERRO'}")
    print(f"   Conexão BD:  {'✅ OK' if conexao_ok else '❌ ERRO'}")
    print(f"   Modelos:     {'✅ OK' if modelos_ok else '❌ ERRO'}")
    print(f"   Interface:   {'✅ OK' if interface_ok else '❌ ERRO'}")
    
    if conexao_ok and modelos_ok and interface_ok:
        print("\n🎉 SISTEMA PRONTO PARA USO!")
        print("   Execute: python main.py")
        return True
    else:
        print("\n⚠️ SISTEMA COM PROBLEMAS")
        if not conexao_ok:
            print("   - Configure o banco de dados")
            print("   - Verifique se MySQL está rodando")
            print("   - Execute o script trabalhoPBD.sql")
        return False

def executar_sistema():
    """Executar o sistema se os testes passarem"""
    if teste_basico():
        resposta = input("\n❓ Deseja executar o sistema agora? (s/n): ").lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            print("\n🚀 Executando sistema...")
            
            try:
                from main import main
                main()
            except Exception as e:
                print(f"❌ Erro ao executar: {e}")
                print("   Tente executar diretamente: python main.py")
    else:
        print("\n🔧 Resolva os problemas antes de executar o sistema")

if __name__ == "__main__":
    executar_sistema()
