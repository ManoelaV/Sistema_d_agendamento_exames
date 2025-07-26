import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
import json
from models import ClinicaModel

class ClinicaGUISimples:
    """Interface simplificada usando apenas tkinter padrão"""
    
    def __init__(self):
        self.model = ClinicaModel()
        
        # Criar janela principal
        self.root = tk.Tk()
        self.root.title("Sistema de Agendamento de Exames - Clínica")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Verificar conexão inicial
        if not self.test_connection():
            self.show_config_dialog()
        
        # Criar interface
        self.create_interface()
        
    def test_connection(self):
        """Testa conexão com o banco"""
        try:
            return self.model.test_connection()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar: {e}")
            return False
    
    def show_config_dialog(self):
        """Diálogo de configuração do banco"""
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuração do Banco de Dados")
        config_window.geometry("450x300")
        config_window.configure(bg='#f0f0f0')
        config_window.grab_set()
        
        # Título
        title_label = tk.Label(config_window, text="Configuração do Banco de Dados", 
                              font=("Arial", 14, "bold"), bg='#f0f0f0')
        title_label.pack(pady=15)
        
        # Frame principal
        frame = tk.Frame(config_window, bg='#f0f0f0')
        frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        # Carregar configuração atual
        current_config = self.model.db.config
        
        # Campos
        tk.Label(frame, text="Host:", bg='#f0f0f0', font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
        host_var = tk.StringVar(value=current_config.get("host", "localhost"))
        host_entry = tk.Entry(frame, textvariable=host_var, width=35, font=("Arial", 10))
        host_entry.grid(row=0, column=1, pady=8, padx=(10, 0))
        
        tk.Label(frame, text="Database:", bg='#f0f0f0', font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
        db_var = tk.StringVar(value=current_config.get("database", "clinica_exames"))
        db_entry = tk.Entry(frame, textvariable=db_var, width=35, font=("Arial", 10))
        db_entry.grid(row=1, column=1, pady=8, padx=(10, 0))
        
        tk.Label(frame, text="Usuário:", bg='#f0f0f0', font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8)
        user_var = tk.StringVar(value=current_config.get("user", "root"))
        user_entry = tk.Entry(frame, textvariable=user_var, width=35, font=("Arial", 10))
        user_entry.grid(row=2, column=1, pady=8, padx=(10, 0))
        
        tk.Label(frame, text="Senha:", bg='#f0f0f0', font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=8)
        pass_var = tk.StringVar(value=current_config.get("password", ""))
        pass_entry = tk.Entry(frame, textvariable=pass_var, show="*", width=35, font=("Arial", 10))
        pass_entry.grid(row=3, column=1, pady=8, padx=(10, 0))
        
        # Botões
        button_frame = tk.Frame(frame, bg='#f0f0f0')
        button_frame.grid(row=4, column=0, columnspan=2, pady=25)
        
        def test_config():
            self.model.db.update_config(host_var.get(), db_var.get(), user_var.get(), pass_var.get())
            if self.model.test_connection():
                messagebox.showinfo("Teste de Conexão", "✅ Conexão estabelecida com sucesso!")
            else:
                messagebox.showerror("Teste de Conexão", "❌ Não foi possível conectar ao banco.")
        
        def save_config():
            self.model.db.update_config(host_var.get(), db_var.get(), user_var.get(), pass_var.get())
            if self.model.test_connection():
                messagebox.showinfo("Configuração", "✅ Configuração salva e conexão estabelecida!")
                config_window.destroy()
                self.refresh_current_tab()
            else:
                messagebox.showerror("Configuração", "⚠️ Configuração salva, mas não foi possível conectar.")
        
        test_btn = tk.Button(button_frame, text="🔍 Testar Conexão", command=test_config, 
                           bg='#032E05', fg='white', font=("Arial", 10), padx=15)
        test_btn.pack(side="left", padx=8)
        
        save_btn = tk.Button(button_frame, text="💾 Salvar", command=save_config, 
                           bg="#002A4D", fg='white', font=("Arial", 10), padx=15)
        save_btn.pack(side="left", padx=8)
        
        cancel_btn = tk.Button(button_frame, text="❌ Cancelar", command=config_window.destroy, 
                             bg='#580600', fg='white', font=("Arial", 10), padx=15)
        cancel_btn.pack(side="left", padx=8)
    
    def create_interface(self):
        """Criar interface principal"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🏥 Sistema de Agendamento de Exames", 
                              font=("Arial", 16, "bold"), bg='#2196F3', fg='white')
        title_label.pack(side="left", padx=20, pady=15)
        
        config_btn = tk.Button(header_frame, text="⚙️ Configurações", 
                             command=self.show_config_dialog, 
                             bg='#002A4D', fg='white', font=("Arial", 10))
        config_btn.pack(side="right", padx=20, pady=15)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar abas
        self.create_pacientes_tab()
        self.create_agendamentos_tab()
        self.create_relatorios_tab()
        
        # Carregar dados iniciais
        self.refresh_pacientes()
        
        # Bind para mudança de aba
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def create_pacientes_tab(self):
        """Criar aba de pacientes"""
        frame = tk.Frame(self.notebook, bg='#f9f9f9')
        self.notebook.add(frame, text="👥 Pacientes")
        
        # Barra de ferramentas
        toolbar = tk.Frame(frame, bg='#e8e8e8', height=50)
        toolbar.pack(fill="x", padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        tk.Button(toolbar, text="➕ Novo Paciente", command=self.add_paciente_dialog, 
                 bg="#032E05", fg='white', font=("Arial", 10), padx=10).pack(side="left", padx=5, pady=8)
        tk.Button(toolbar, text="✏️ Editar", command=self.edit_paciente_dialog, 
                 bg="#7E4D04", fg='white', font=("Arial", 10), padx=10).pack(side="left", padx=5, pady=8)
        tk.Button(toolbar, text="🗑️ Excluir", command=self.delete_paciente, 
                 bg="#580600", fg='white', font=("Arial", 10), padx=10).pack(side="left", padx=5, pady=8)
        tk.Button(toolbar, text="🔄 Atualizar", command=self.refresh_pacientes, 
                 bg='#002A4D', fg='white', font=("Arial", 10), padx=10).pack(side="left", padx=5, pady=8)
        
        # Frame para treeview
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview para pacientes
        columns = ("ID", "Nome", "CPF", "Telefone", "Data Nasc.", "Empresa")
        self.pacientes_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configurar colunas
        column_widths = {"ID": 60, "Nome": 200, "CPF": 120, "Telefone": 120, "Data Nasc.": 100, "Empresa": 150}
        for col in columns:
            self.pacientes_tree.heading(col, text=col)
            self.pacientes_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.pacientes_tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.pacientes_tree.xview)
        self.pacientes_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Pack treeview e scrollbars
        self.pacientes_tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        
        # Bind double-click
        self.pacientes_tree.bind("<Double-1>", lambda e: self.edit_paciente_dialog())
    
    def create_agendamentos_tab(self):
        """Criar aba de agendamentos"""
        frame = tk.Frame(self.notebook, bg='#f9f9f9')
        self.notebook.add(frame, text="📅 Agendamentos")
        
        # Toolbar
        toolbar = tk.Frame(frame, bg='#e8e8e8', height=50)
        toolbar.pack(fill="x", padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        tk.Button(toolbar, text="➕ Novo Agendamento", command=self.add_agendamento_dialog, 
                 bg='#032E05', fg='white', font=("Arial", 10), padx=10).pack(side="left", padx=5, pady=8)
        tk.Button(toolbar, text="✏️ Atualizar Status", command=self.update_status_dialog, 
                 bg='#7E4D04', fg='white', font=("Arial", 10), padx=10).pack(side="left", padx=5, pady=8)
        tk.Button(toolbar, text="🗑️ Cancelar", command=self.delete_agendamento, 
                 bg='#580600', fg='white', font=("Arial", 10), padx=10).pack(side="left", padx=5, pady=8)
        tk.Button(toolbar, text="🔄 Atualizar", command=self.refresh_agendamentos, 
                 bg='#002A4D', fg='white', font=("Arial", 10), padx=10).pack(side="left", padx=5, pady=8)
        
        # Frame para treeview
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview para agendamentos
        columns = ("ID", "Paciente", "Exame", "Data/Hora", "Status", "Unidade")
        self.agendamentos_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configurar colunas
        column_widths = {"ID": 60, "Paciente": 150, "Exame": 150, "Data/Hora": 120, "Status": 100, "Unidade": 200}
        for col in columns:
            self.agendamentos_tree.heading(col, text=col)
            self.agendamentos_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scroll2 = ttk.Scrollbar(tree_frame, orient="vertical", command=self.agendamentos_tree.yview)
        h_scroll2 = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.agendamentos_tree.xview)
        self.agendamentos_tree.configure(yscrollcommand=v_scroll2.set, xscrollcommand=h_scroll2.set)
        
        # Pack
        self.agendamentos_tree.pack(side="left", fill="both", expand=True)
        v_scroll2.pack(side="right", fill="y")
        h_scroll2.pack(side="bottom", fill="x")
    
    def create_relatorios_tab(self):
        """Criar aba de relatórios"""
        frame = tk.Frame(self.notebook, bg='#f9f9f9')
        self.notebook.add(frame, text="📊 Relatórios")
        
        # Botões de relatórios
        button_frame = tk.Frame(frame, bg='#e8e8e8')
        button_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(button_frame, text="📅 Exames Próximos", command=self.show_exames_proximos, 
                 bg="#520061", fg='white', font=("Arial", 10), padx=15).pack(side="left", padx=8, pady=8)
        tk.Button(button_frame, text="👨‍⚕️ Por Profissional", command=self.show_agend_profissional, 
                 bg='#520061', fg='white', font=("Arial", 10), padx=15).pack(side="left", padx=8, pady=8)
        tk.Button(button_frame, text="🏢 Por Empresa", command=self.show_pacientes_empresa, 
                 bg='#520061', fg='white', font=("Arial", 10), padx=15).pack(side="left", padx=8, pady=8)
        
        # Área de texto para relatórios
        text_frame = tk.Frame(frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.relatorio_text = tk.Text(text_frame, wrap="word", font=("Consolas", 10), bg='white')
        
        # Scrollbar para texto
        text_scroll = tk.Scrollbar(text_frame, orient="vertical", command=self.relatorio_text.yview)
        self.relatorio_text.configure(yscrollcommand=text_scroll.set)
        
        # Pack
        self.relatorio_text.pack(side="left", fill="both", expand=True)
        text_scroll.pack(side="right", fill="y")
    
    def on_tab_change(self, event=None):
        """Evento de mudança de aba"""
        try:
            selection = self.notebook.select()
            tab_name = self.notebook.tab(selection, "text")
            self.refresh_current_tab()
        except:
            pass
    
    def refresh_current_tab(self):
        """Atualizar dados da aba atual"""
        try:
            selection = self.notebook.select()
            tab_name = self.notebook.tab(selection, "text")
            
            if "Pacientes" in tab_name:
                self.refresh_pacientes()
            elif "Agendamentos" in tab_name:
                self.refresh_agendamentos()
        except:
            pass
    
    def refresh_pacientes(self):
        """Carregar pacientes na treeview"""
        try:
            # Limpar dados existentes
            for item in self.pacientes_tree.get_children():
                self.pacientes_tree.delete(item)
            
            # Carregar novos dados
            pacientes = self.model.get_pacientes()
            if pacientes:
                for pac in pacientes:
                    empresa = pac.get('empresa_nome', '') if pac.get('empresa_nome') else 'Sem empresa'
                    data_nasc = pac['data_nasc'].strftime('%d/%m/%Y') if pac['data_nasc'] else ''
                    
                    self.pacientes_tree.insert("", "end", values=(
                        pac['id_paciente'],
                        pac['nome'],
                        pac['cpf'],
                        pac['telefone'],
                        data_nasc,
                        empresa
                    ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar pacientes: {e}")
    
    def refresh_agendamentos(self):
        """Carregar agendamentos na treeview"""
        try:
            for item in self.agendamentos_tree.get_children():
                self.agendamentos_tree.delete(item)
            
            agendamentos = self.model.get_agendamentos()
            if agendamentos:
                for agend in agendamentos:
                    data_hora = agend['data_hora'].strftime('%d/%m/%Y %H:%M') if agend['data_hora'] else ''
                    
                    # Status com emoji
                    status_display = agend['status']
                    if agend['status'] == 'AGENDADO':
                        status_display = '🟡 AGENDADO'
                    elif agend['status'] == 'REALIZADO':
                        status_display = '✅ REALIZADO'
                    elif agend['status'] == 'CANCELADO':
                        status_display = '❌ CANCELADO'
                    
                    unidade_short = agend['unidade_endereco'][:40] + "..." if len(agend['unidade_endereco']) > 40 else agend['unidade_endereco']
                    
                    self.agendamentos_tree.insert("", "end", values=(
                        agend['id_agendamento'],
                        agend['paciente_nome'],
                        agend['exame_nome'],
                        data_hora,
                        status_display,
                        unidade_short
                    ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar agendamentos: {e}")
    
    # Diálogos simplificados
    def add_paciente_dialog(self):
        """Diálogo simplificado para adicionar paciente"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Paciente")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f0f0')
        dialog.grab_set()
        
        # Título
        tk.Label(dialog, text="Cadastro de Novo Paciente", font=("Arial", 12, "bold"), 
                bg='#f0f0f0').pack(pady=10)
        
        # Frame para campos
        frame = tk.Frame(dialog, bg='#f0f0f0')
        frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Campos
        tk.Label(frame, text="Nome:", bg='#f0f0f0').grid(row=0, column=0, sticky="w", pady=5)
        nome_var = tk.StringVar()
        tk.Entry(frame, textvariable=nome_var, width=30).grid(row=0, column=1, pady=5, padx=(10,0))
        
        tk.Label(frame, text="CPF:", bg='#f0f0f0').grid(row=1, column=0, sticky="w", pady=5)
        cpf_var = tk.StringVar()
        tk.Entry(frame, textvariable=cpf_var, width=30).grid(row=1, column=1, pady=5, padx=(10,0))
        
        tk.Label(frame, text="Telefone:", bg='#f0f0f0').grid(row=2, column=0, sticky="w", pady=5)
        telefone_var = tk.StringVar()
        tk.Entry(frame, textvariable=telefone_var, width=30).grid(row=2, column=1, pady=5, padx=(10,0))
        
        tk.Label(frame, text="Data Nascimento:", bg='#f0f0f0').grid(row=3, column=0, sticky="w", pady=5)
        data_var = tk.StringVar()
        tk.Entry(frame, textvariable=data_var, width=30).grid(row=3, column=1, pady=5, padx=(10,0))
        tk.Label(frame, text="(DD/MM/AAAA)", font=("Arial", 8), bg='#f0f0f0').grid(row=3, column=2, padx=5)
        
        tk.Label(frame, text="Endereço:", bg='#f0f0f0').grid(row=4, column=0, sticky="w", pady=5)
        endereco_var = tk.StringVar()
        tk.Entry(frame, textvariable=endereco_var, width=30).grid(row=4, column=1, pady=5, padx=(10,0))
        
        # Botões
        button_frame = tk.Frame(frame, bg='#f0f0f0')
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        def salvar():
            try:
                if not nome_var.get().strip():
                    messagebox.showerror("Erro", "Nome é obrigatório")
                    return
                
                if not cpf_var.get().strip():
                    messagebox.showerror("Erro", "CPF é obrigatório")
                    return
                
                # Converter data
                try:
                    data_nasc = datetime.strptime(data_var.get(), "%d/%m/%Y").date()
                except ValueError:
                    messagebox.showerror("Erro", "Data inválida. Use DD/MM/AAAA")
                    return
                
                # Salvar
                if self.model.add_paciente(
                    nome_var.get().strip(),
                    endereco_var.get().strip() or "Não informado",
                    telefone_var.get().strip() or "Não informado",
                    cpf_var.get().strip(),
                    data_nasc
                ):
                    messagebox.showinfo("Sucesso", "✅ Paciente cadastrado com sucesso!")
                    dialog.destroy()
                    self.refresh_pacientes()
                else:
                    messagebox.showerror("Erro", "❌ Erro ao cadastrar paciente")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        
        tk.Button(button_frame, text="💾 Salvar", command=salvar, 
                 bg='#032E05', fg='white', padx=15).pack(side="left", padx=5)
        tk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy, 
                 bg='#580600', fg='white', padx=15).pack(side="left", padx=5)
    
    def edit_paciente_dialog(self):
        """Editar paciente selecionado"""
        selection = self.pacientes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "⚠️ Selecione um paciente para editar")
            return
        
        messagebox.showinfo("Info", "Funcionalidade de edição será implementada em breve")
    
    def delete_paciente(self):
        """Excluir paciente selecionado"""
        selection = self.pacientes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "⚠️ Selecione um paciente para excluir")
            return
        
        item = self.pacientes_tree.item(selection[0])
        id_paciente = item['values'][0]
        nome_paciente = item['values'][1]
        
        if messagebox.askyesno("Confirmação", f"❓ Deseja excluir o paciente '{nome_paciente}'?"):
            if self.model.delete_paciente(id_paciente):
                messagebox.showinfo("Sucesso", "✅ Paciente excluído com sucesso!")
                self.refresh_pacientes()
            else:
                messagebox.showerror("Erro", "❌ Erro ao excluir. Pode haver agendamentos relacionados.")
    
    def add_agendamento_dialog(self):
        """Diálogo para novo agendamento"""
        messagebox.showinfo("Em Desenvolvimento", 
                          "🚧 Funcionalidade de agendamento será implementada em breve.\n\n"
                          "Para a versão completa, instale:\n"
                          "pip install ttkbootstrap")
    
    def update_status_dialog(self):
        """Atualizar status do agendamento"""
        messagebox.showinfo("Em Desenvolvimento", "🚧 Em desenvolvimento...")
    
    def delete_agendamento(self):
        """Cancelar agendamento"""
        messagebox.showinfo("Em Desenvolvimento", "🚧 Em desenvolvimento...")
    
    # Relatórios
    def show_exames_proximos(self):
        """Mostrar exames próximos"""
        try:
            exames = self.model.get_exames_proximos()
            
            self.relatorio_text.delete("1.0", tk.END)
            self.relatorio_text.insert("1.0", "=== EXAMES PRÓXIMOS ===\n\n")
            
            if exames:
                for exame in exames:
                    data_formatada = exame['data_hora'].strftime('%d/%m/%Y %H:%M')
                    
                    prioridade_emoji = {
                        'URGENTE': '🔴',
                        'PRÓXIMO': '🟡',
                        'FUTURO': '🟢'
                    }.get(exame['prioridade'], '⚪')
                    
                    texto = f"{prioridade_emoji} {exame['prioridade']}\n"
                    texto += f"Paciente: {exame['paciente']}\n"
                    texto += f"Exame: {exame['exame']}\n"
                    texto += f"Data/Hora: {data_formatada}\n"
                    texto += f"Unidade: {exame['unidade'][:50]}...\n" if len(exame['unidade']) > 50 else f"Unidade: {exame['unidade']}\n"
                    texto += "-" * 50 + "\n\n"
                    self.relatorio_text.insert(tk.END, texto)
            else:
                self.relatorio_text.insert(tk.END, "📋 Nenhum exame próximo encontrado.\n")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def show_agend_profissional(self):
        """Mostrar agendamentos por profissional"""
        try:
            dados = self.model.get_agendamentos_por_profissional()
            
            self.relatorio_text.delete("1.0", tk.END)
            self.relatorio_text.insert("1.0", "=== AGENDAMENTOS POR PROFISSIONAL ===\n\n")
            
            if dados:
                for item in dados:
                    texto = f"👨‍⚕️ Profissional: {item['profissional']}\n"
                    texto += f"   Exame: {item['exame']}\n"
                    texto += f"   Total de Agendamentos: {item['total']}\n"
                    texto += "-" * 40 + "\n\n"
                    self.relatorio_text.insert(tk.END, texto)
            else:
                self.relatorio_text.insert(tk.END, "📋 Nenhum dado encontrado.\n")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def show_pacientes_empresa(self):
        """Mostrar pacientes por empresa"""
        try:
            dados = self.model.get_pacientes_por_empresa()
            
            self.relatorio_text.delete("1.0", tk.END)
            self.relatorio_text.insert("1.0", "=== PACIENTES POR EMPRESA ===\n\n")
            
            if dados:
                empresa_atual = ""
                for item in dados:
                    if item['empresa'] != empresa_atual:
                        empresa_atual = item['empresa']
                        self.relatorio_text.insert(tk.END, f"\n🏢 {empresa_atual}\n")
                        self.relatorio_text.insert(tk.END, "=" * 50 + "\n")
                    
                    data_nasc = item['data_nasc'].strftime('%d/%m/%Y') if item['data_nasc'] else 'N/A'
                    texto = f"  👤 {item['paciente']} - CPF: {item['cpf']} - Nasc: {data_nasc}\n"
                    self.relatorio_text.insert(tk.END, texto)
            else:
                self.relatorio_text.insert(tk.END, "📋 Nenhum paciente vinculado a empresas encontrado.\n")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def run(self):
        """Executar aplicação"""
        self.root.mainloop()
