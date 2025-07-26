#!/usr/bin/env python3
"""
Sistema de Agendamento de Exames - Clínica
Interface Desktop para comunicação com banco de dados MySQL

Autor: Sistema Automatizado
Data: 2025
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Adicionar o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Tentar importar versão completa primeiro
try:
    import ttkbootstrap as ttk_boot
    from gui_main import ClinicaGUI
    interface_completa_disponivel = True
    print("Interface completa disponível!")
except ImportError:
    interface_completa_disponivel = False
    print("ttkbootstrap não encontrado. Usando interface simplificada...")

# Importar versão simplificada (sempre disponível)
from gui_simples import ClinicaGUISimples

def main():
    """Função principal"""
    print("🏥 === Sistema de Agendamento de Exames ===")
    print("Iniciando aplicação...")
    
    app = None
    
    try:
        # Tentar carregar interface completa primeiro
        if interface_completa_disponivel:
            print("Carregando interface completa...")
            app = ClinicaGUI()
            print("✅ Interface completa carregada com sucesso!")
        else:
            # Usar interface simplificada
            print("Carregando interface simplificada...")
            app = ClinicaGUISimples()
            print("✅ Interface simplificada carregada!")
            print("💡 Para interface completa, instale: pip install ttkbootstrap")
        
    except Exception as e:
        print(f"❌ Erro ao carregar interface principal: {e}")
        
        # Fallback para interface simplificada
        if interface_completa_disponivel:
            try:
                print("Tentando interface simplificada como fallback...")
                app = ClinicaGUISimples()
                print("✅ Interface simplificada carregada como fallback!")
            except Exception as e2:
                print(f"❌ Erro crítico: {e2}")
                messagebox.showerror("Erro Fatal", 
                                   f"Não foi possível iniciar a aplicação.\n\n"
                                   f"Erro principal: {e}\n"
                                   f"Erro fallback: {e2}\n\n"
                                   f"Verifique se:\n"
                                   f"- MySQL está rodando\n"
                                   f"- Dependências estão instaladas\n"
                                   f"- Banco foi criado corretamente")
                return
        else:
            print(f"❌ Erro crítico: {e}")
            messagebox.showerror("Erro Fatal", 
                               f"Não foi possível iniciar a aplicação.\n\n"
                               f"Erro: {e}\n\n"
                               f"Verifique se:\n"
                               f"- MySQL está rodando\n"
                               f"- Dependências estão instaladas\n"
                               f"- Banco foi criado corretamente")
            return
    
    # Executar aplicação
    if app:
        try:
            print("🚀 Iniciando interface gráfica...")
            app.run()
        except KeyboardInterrupt:
            print("\n⏹️ Aplicação encerrada pelo usuário.")
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            messagebox.showerror("Erro de Execução", f"Erro durante execução: {e}")
    else:
        print("❌ Nenhuma interface pôde ser carregada!")

if __name__ == "__main__":
    main()
