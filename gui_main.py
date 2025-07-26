import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk_boot
from ttkbootstrap.constants import *
from datetime import datetime, date
import json
from models import ClinicaModel

class ClinicaGUI:
    def __init__(self):
        # Inicializar modelo
        self.model = ClinicaModel()
        
        # Criar janela principal
        self.root = ttk_boot.Window(themename="cosmo")
        self.root.title("Sistema de Agendamento de Exames - Clínica")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Configurar estilo
        self.setup_styles()
        
        # Verificar conexão inicial
        if not self.test_connection():
            self.show_config_dialog()
        
        # Criar interface
        self.create_main_interface()
        
        # Variáveis para dados
        self.current_tab = "pacientes"
        self.refresh_data()
    
    def setup_styles(self):
        """Configurar estilos personalizados"""
        style = ttk_boot.Style()
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
    
    def test_connection(self):
        """Testa conexão com o banco"""
        try:
            return self.model.test_connection()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco: {e}")
            return False
    
    def show_config_dialog(self):
        """Mostra diálogo de configuração do banco"""
        config_window = ttk_boot.Toplevel(self.root)
        config_window.title("Configuração do Banco de Dados")
        config_window.geometry("400x300")
        config_window.grab_set()
        
        # Carregar configuração atual
        current_config = self.model.db.config
        
        # Campos de configuração
        ttk_boot.Label(config_window, text="Configuração do Banco de Dados", 
                      style="Title.TLabel").pack(pady=10)
        
        frame = ttk_boot.Frame(config_window)
        frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Host
        ttk_boot.Label(frame, text="Host:").grid(row=0, column=0, sticky="w", pady=5)
        host_var = tk.StringVar(value=current_config.get("host", "localhost"))
        host_entry = ttk_boot.Entry(frame, textvariable=host_var, width=30)
        host_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Database
        ttk_boot.Label(frame, text="Database:").grid(row=1, column=0, sticky="w", pady=5)
        db_var = tk.StringVar(value=current_config.get("database", "clinica_exames"))
        db_entry = ttk_boot.Entry(frame, textvariable=db_var, width=30)
        db_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # User
        ttk_boot.Label(frame, text="Usuário:").grid(row=2, column=0, sticky="w", pady=5)
        user_var = tk.StringVar(value=current_config.get("user", "root"))
        user_entry = ttk_boot.Entry(frame, textvariable=user_var, width=30)
        user_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk_boot.Label(frame, text="Senha:").grid(row=3, column=0, sticky="w", pady=5)
        pass_var = tk.StringVar(value=current_config.get("password", ""))
        pass_entry = ttk_boot.Entry(frame, textvariable=pass_var, show="*", width=30)
        pass_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Botões
        button_frame = ttk_boot.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def test_config():
            self.model.db.update_config(host_var.get(), db_var.get(), user_var.get(), pass_var.get())
            if self.model.test_connection():
                messagebox.showinfo("Sucesso", "Conexão estabelecida com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        
        def save_config():
            self.model.db.update_config(host_var.get(), db_var.get(), user_var.get(), pass_var.get())
            if self.model.test_connection():
                messagebox.showinfo("Sucesso", "Configuração salva e conexão estabelecida!")
                config_window.destroy()
            else:
                messagebox.showerror("Erro", "Configuração salva, mas não foi possível conectar.")
        
        ttk_boot.Button(button_frame, text="Testar Conexão", command=test_config, 
                       bootstyle="info").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Salvar", command=save_config, 
                       bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Cancelar", command=config_window.destroy, 
                       bootstyle="secondary").pack(side="left", padx=5)
    
    def create_main_interface(self):
        """Criar interface principal"""
        # Título
        title_frame = ttk_boot.Frame(self.root)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        ttk_boot.Label(title_frame, text="Sistema de Agendamento de Exames", 
                      style="Title.TLabel").pack(side="left")
        
        # Botão de configuração
        ttk_boot.Button(title_frame, text="⚙️ Configurações", 
                       command=self.show_config_dialog, 
                       bootstyle="outline-secondary").pack(side="right")
        
        # Notebook para abas
        self.notebook = ttk_boot.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Criar abas
        self.create_pacientes_tab()
        self.create_exames_tab()
        self.create_agendamentos_tab()
        self.create_resultados_tab()
        self.create_relatorios_tab()
        
        # Bind para mudança de aba
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def create_pacientes_tab(self):
        """Criar aba de pacientes"""
        frame = ttk_boot.Frame(self.notebook)
        self.notebook.add(frame, text="👥 Pacientes")
        
        # Barra de ferramentas
        toolbar = ttk_boot.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        ttk_boot.Button(toolbar, text="➕ Novo Paciente", 
                       command=self.add_paciente_dialog, 
                       bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="✏️ Editar", 
                       command=self.edit_paciente_dialog, 
                       bootstyle="primary").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="🗑️ Excluir", 
                       command=self.delete_paciente, 
                       bootstyle="danger").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="🔄 Atualizar", 
                       command=lambda: self.refresh_data("pacientes"), 
                       bootstyle="info").pack(side="left", padx=5)
        
        # Treeview para pacientes
        columns = ("ID", "Nome", "CPF", "Telefone", "Data Nasc.", "Empresa")
        self.pacientes_tree = ttk_boot.Treeview(frame, columns=columns, show="headings", height=20)
        
        # Configurar colunas
        for col in columns:
            self.pacientes_tree.heading(col, text=col)
            self.pacientes_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar_pac = ttk_boot.Scrollbar(frame, orient="vertical", command=self.pacientes_tree.yview)
        self.pacientes_tree.configure(yscrollcommand=scrollbar_pac.set)
        
        # Pack treeview e scrollbar
        tree_frame = ttk_boot.Frame(frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.pacientes_tree.pack(side="left", fill="both", expand=True)
        scrollbar_pac.pack(side="right", fill="y")
        
        # Bind double-click
        self.pacientes_tree.bind("<Double-1>", lambda e: self.edit_paciente_dialog())
    
    def create_exames_tab(self):
        """Criar aba de exames"""
        frame = ttk_boot.Frame(self.notebook)
        self.notebook.add(frame, text="🔬 Exames")
        
        # Barra de ferramentas
        toolbar = ttk_boot.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        ttk_boot.Button(toolbar, text="➕ Novo Exame", 
                       command=self.add_exame_dialog, 
                       bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="✏️ Editar", 
                       command=self.edit_exame_dialog, 
                       bootstyle="primary").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="🗑️ Excluir", 
                       command=self.delete_exame, 
                       bootstyle="danger").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="🔄 Atualizar", 
                       command=lambda: self.refresh_data("exames"), 
                       bootstyle="info").pack(side="left", padx=5)
        
        # Treeview para exames
        columns = ("ID", "Nome", "Tipo", "Tempo (min)", "Requisitos")
        self.exames_tree = ttk_boot.Treeview(frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.exames_tree.heading(col, text=col)
            if col == "Requisitos":
                self.exames_tree.column(col, width=300)
            else:
                self.exames_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar_exam = ttk_boot.Scrollbar(frame, orient="vertical", command=self.exames_tree.yview)
        self.exames_tree.configure(yscrollcommand=scrollbar_exam.set)
        
        # Pack
        tree_frame = ttk_boot.Frame(frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.exames_tree.pack(side="left", fill="both", expand=True)
        scrollbar_exam.pack(side="right", fill="y")
        
        # Bind double-click
        self.exames_tree.bind("<Double-1>", lambda e: self.edit_exame_dialog())
    
    def create_agendamentos_tab(self):
        """Criar aba de agendamentos"""
        frame = ttk_boot.Frame(self.notebook)
        self.notebook.add(frame, text="📅 Agendamentos")
        
        # Barra de ferramentas
        toolbar = ttk_boot.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        ttk_boot.Button(toolbar, text="➕ Novo Agendamento", 
                       command=self.add_agendamento_dialog, 
                       bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="✏️ Atualizar Status", 
                       command=self.update_status_dialog, 
                       bootstyle="primary").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="🗑️ Cancelar", 
                       command=self.delete_agendamento, 
                       bootstyle="danger").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="🔄 Atualizar", 
                       command=lambda: self.refresh_data("agendamentos"), 
                       bootstyle="info").pack(side="left", padx=5)
        
        # Treeview para agendamentos
        columns = ("ID", "Paciente", "Exame", "Data/Hora", "Status", "Unidade", "Profissional")
        self.agendamentos_tree = ttk_boot.Treeview(frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.agendamentos_tree.heading(col, text=col)
            if col in ["Paciente", "Exame", "Unidade"]:
                self.agendamentos_tree.column(col, width=200)
            else:
                self.agendamentos_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar_agend = ttk_boot.Scrollbar(frame, orient="vertical", command=self.agendamentos_tree.yview)
        self.agendamentos_tree.configure(yscrollcommand=scrollbar_agend.set)
        
        # Pack
        tree_frame = ttk_boot.Frame(frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.agendamentos_tree.pack(side="left", fill="both", expand=True)
        scrollbar_agend.pack(side="right", fill="y")
    
    def create_resultados_tab(self):
        """Criar aba de resultados"""
        frame = ttk_boot.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Resultados")
        
        # Barra de ferramentas
        toolbar = ttk_boot.Frame(frame)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        ttk_boot.Button(toolbar, text="➕ Novo Resultado", 
                       command=self.add_resultado_dialog, 
                       bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(toolbar, text="🔄 Atualizar", 
                       command=lambda: self.refresh_data("resultados"), 
                       bootstyle="info").pack(side="left", padx=5)
        
        # Treeview para resultados
        columns = ("ID", "Paciente", "Exame", "Data", "Resultados")
        self.resultados_tree = ttk_boot.Treeview(frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.resultados_tree.heading(col, text=col)
            if col == "Resultados":
                self.resultados_tree.column(col, width=400)
            else:
                self.resultados_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar_res = ttk_boot.Scrollbar(frame, orient="vertical", command=self.resultados_tree.yview)
        self.resultados_tree.configure(yscrollcommand=scrollbar_res.set)
        
        # Pack
        tree_frame = ttk_boot.Frame(frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.resultados_tree.pack(side="left", fill="both", expand=True)
        scrollbar_res.pack(side="right", fill="y")
    
    def create_relatorios_tab(self):
        """Criar aba de relatórios"""
        frame = ttk_boot.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Relatórios")
        
        # Botões de relatórios
        button_frame = ttk_boot.Frame(frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk_boot.Button(button_frame, text="📅 Exames Próximos", 
                       command=self.show_exames_proximos, 
                       bootstyle="primary").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="👨‍⚕️ Por Profissional", 
                       command=self.show_agend_profissional, 
                       bootstyle="primary").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="🏢 Por Empresa", 
                       command=self.show_pacientes_empresa, 
                       bootstyle="primary").pack(side="left", padx=5)
        
        # Área de texto para relatórios
        self.relatorio_text = tk.Text(frame, wrap="word", font=("Consolas", 10))
        
        # Scrollbar para texto
        text_scrollbar = ttk_boot.Scrollbar(frame, orient="vertical", command=self.relatorio_text.yview)
        self.relatorio_text.configure(yscrollcommand=text_scrollbar.set)
        
        # Pack
        text_frame = ttk_boot.Frame(frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.relatorio_text.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")
    
    def on_tab_change(self, event=None):
        """Evento de mudança de aba"""
        selection = self.notebook.select()
        tab_name = self.notebook.tab(selection, "text")
        
        # Mapear nome da aba para chave
        tab_map = {
            "👥 Pacientes": "pacientes",
            "🔬 Exames": "exames", 
            "📅 Agendamentos": "agendamentos",
            "📋 Resultados": "resultados"
        }
        
        if tab_name in tab_map:
            self.current_tab = tab_map[tab_name]
            self.refresh_data(self.current_tab)
    
    def refresh_data(self, tab=None):
        """Atualizar dados da aba atual"""
        if not tab:
            tab = self.current_tab
            
        try:
            if tab == "pacientes":
                self.load_pacientes()
            elif tab == "exames":
                self.load_exames()
            elif tab == "agendamentos":
                self.load_agendamentos()
            elif tab == "resultados":
                self.load_resultados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
    
    def load_pacientes(self):
        """Carregar pacientes na treeview"""
        # Limpar dados existentes
        for item in self.pacientes_tree.get_children():
            self.pacientes_tree.delete(item)
        
        # Carregar novos dados
        pacientes = self.model.get_pacientes()
        if pacientes:
            for pac in pacientes:
                empresa = pac.get('empresa_nome', '') if pac.get('empresa_nome') else ''
                data_nasc = pac['data_nasc'].strftime('%d/%m/%Y') if pac['data_nasc'] else ''
                
                self.pacientes_tree.insert("", "end", values=(
                    pac['id_paciente'],
                    pac['nome'],
                    pac['cpf'],
                    pac['telefone'],
                    data_nasc,
                    empresa
                ))
    
    def load_exames(self):
        """Carregar exames na treeview"""
        for item in self.exames_tree.get_children():
            self.exames_tree.delete(item)
        
        exames = self.model.get_exames()
        if exames:
            for exame in exames:
                self.exames_tree.insert("", "end", values=(
                    exame['id_exame'],
                    exame['nome'],
                    exame['tipo'],
                    exame['tempo_estimado'],
                    exame['requisitos'][:50] + "..." if len(str(exame['requisitos'])) > 50 else exame['requisitos']
                ))
    
    def load_agendamentos(self):
        """Carregar agendamentos na treeview"""
        for item in self.agendamentos_tree.get_children():
            self.agendamentos_tree.delete(item)
        
        agendamentos = self.model.get_agendamentos()
        if agendamentos:
            for agend in agendamentos:
                prof_nome = agend.get('profissional_nome', '') if agend.get('profissional_nome') else 'N/A'
                data_hora = agend['data_hora'].strftime('%d/%m/%Y %H:%M') if agend['data_hora'] else ''
                
                self.agendamentos_tree.insert("", "end", values=(
                    agend['id_agendamento'],
                    agend['paciente_nome'],
                    agend['exame_nome'],
                    data_hora,
                    agend['status'],
                    agend['unidade_endereco'][:30] + "..." if len(agend['unidade_endereco']) > 30 else agend['unidade_endereco'],
                    prof_nome
                ))
    
    def load_resultados(self):
        """Carregar resultados na treeview"""
        for item in self.resultados_tree.get_children():
            self.resultados_tree.delete(item)
        
        resultados = self.model.get_resultados()
        if resultados:
            for res in resultados:
                data_hora = res['data_hora'].strftime('%d/%m/%Y') if res['data_hora'] else ''
                
                self.resultados_tree.insert("", "end", values=(
                    res['id_resultado'],
                    res['paciente_nome'],
                    res['exame_nome'],
                    data_hora,
                    res['resultados'][:50] + "..." if len(str(res['resultados'])) > 50 else res['resultados']
                ))
    
    # MÉTODOS DE DIÁLOGO - PACIENTES
    
    def add_paciente_dialog(self):
        """Diálogo para adicionar paciente"""
        dialog = ttk_boot.Toplevel(self.root)
        dialog.title("Novo Paciente")
        dialog.geometry("500x400")
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk_boot.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos
        ttk_boot.Label(main_frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        nome_var = tk.StringVar()
        ttk_boot.Entry(main_frame, textvariable=nome_var, width=40).grid(row=0, column=1, pady=5, padx=(10,0))
        
        ttk_boot.Label(main_frame, text="CPF:").grid(row=1, column=0, sticky="w", pady=5)
        cpf_var = tk.StringVar()
        ttk_boot.Entry(main_frame, textvariable=cpf_var, width=40).grid(row=1, column=1, pady=5, padx=(10,0))
        
        ttk_boot.Label(main_frame, text="Telefone:").grid(row=2, column=0, sticky="w", pady=5)
        telefone_var = tk.StringVar()
        ttk_boot.Entry(main_frame, textvariable=telefone_var, width=40).grid(row=2, column=1, pady=5, padx=(10,0))
        
        ttk_boot.Label(main_frame, text="Data Nascimento:").grid(row=3, column=0, sticky="w", pady=5)
        data_var = tk.StringVar()
        ttk_boot.Entry(main_frame, textvariable=data_var, width=40).grid(row=3, column=1, pady=5, padx=(10,0))
        ttk_boot.Label(main_frame, text="(DD/MM/AAAA)", font=("Arial", 8)).grid(row=3, column=2, padx=5)
        
        ttk_boot.Label(main_frame, text="Endereço:").grid(row=4, column=0, sticky="w", pady=5)
        endereco_text = tk.Text(main_frame, width=30, height=3)
        endereco_text.grid(row=4, column=1, pady=5, padx=(10,0))
        
        ttk_boot.Label(main_frame, text="Empresa:").grid(row=5, column=0, sticky="w", pady=5)
        empresa_var = tk.StringVar()
        empresa_combo = ttk_boot.Combobox(main_frame, textvariable=empresa_var, width=37, state="readonly")
        empresa_combo.grid(row=5, column=1, pady=5, padx=(10,0))
        
        # Carregar empresas
        empresas = self.model.get_empresas()
        empresa_values = ["Nenhuma"]
        empresa_ids = [None]
        if empresas:
            for emp in empresas:
                empresa_values.append(emp['nome'])
                empresa_ids.append(emp['id_empresa'])
        
        empresa_combo['values'] = empresa_values
        empresa_combo.set("Nenhuma")
        
        # Botões
        button_frame = ttk_boot.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        def salvar():
            try:
                # Validar campos
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
                
                # ID da empresa
                empresa_idx = empresa_combo.current()
                id_empresa = empresa_ids[empresa_idx] if empresa_idx >= 0 else None
                
                # Salvar
                if self.model.add_paciente(
                    nome_var.get().strip(),
                    endereco_text.get("1.0", tk.END).strip(),
                    telefone_var.get().strip(),
                    cpf_var.get().strip(),
                    data_nasc,
                    id_empresa
                ):
                    messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
                    dialog.destroy()
                    self.refresh_data("pacientes")
                else:
                    messagebox.showerror("Erro", "Erro ao cadastrar paciente")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        
        ttk_boot.Button(button_frame, text="Salvar", command=salvar, bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="secondary").pack(side="left", padx=5)
    
    def edit_paciente_dialog(self):
        """Diálogo para editar paciente"""
        selection = self.pacientes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um paciente para editar")
            return
        
        messagebox.showinfo("Info", "Funcionalidade de edição será implementada em breve")
    
    def delete_paciente(self):
        """Excluir paciente selecionado"""
        selection = self.pacientes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um paciente para excluir")
            return
        
        item = self.pacientes_tree.item(selection[0])
        id_paciente = item['values'][0]
        nome_paciente = item['values'][1]
        
        if messagebox.askyesno("Confirmação", f"Deseja excluir o paciente '{nome_paciente}'?"):
            if self.model.delete_paciente(id_paciente):
                messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
                self.refresh_data("pacientes")
            else:
                messagebox.showerror("Erro", "Erro ao excluir paciente. Verifique se não há agendamentos relacionados.")
    
    # MÉTODOS DE DIÁLOGO - EXAMES
    
    def add_exame_dialog(self):
        """Diálogo para adicionar exame"""
        messagebox.showinfo("Info", "Funcionalidade de cadastro de exames será implementada em breve")
    
    def edit_exame_dialog(self):
        """Diálogo para editar exame"""
        messagebox.showinfo("Info", "Funcionalidade de edição de exames será implementada em breve")
    
    def delete_exame(self):
        """Excluir exame selecionado"""
        selection = self.exames_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um exame para excluir")
            return
        
        item = self.exames_tree.item(selection[0])
        id_exame = item['values'][0]
        nome_exame = item['values'][1]
        
        if messagebox.askyesno("Confirmação", f"Deseja excluir o exame '{nome_exame}'?"):
            if self.model.delete_exame(id_exame):
                messagebox.showinfo("Sucesso", "Exame excluído com sucesso!")
                self.refresh_data("exames")
            else:
                messagebox.showerror("Erro", "Erro ao excluir exame. Verifique se não há agendamentos relacionados.")
    
    # MÉTODOS DE DIÁLOGO - AGENDAMENTOS
    
    def add_agendamento_dialog(self):
        """Diálogo para adicionar agendamento"""
        messagebox.showinfo("Info", "Funcionalidade de agendamento será implementada em breve")
    
    def update_status_dialog(self):
        """Diálogo para atualizar status do agendamento"""
        messagebox.showinfo("Info", "Funcionalidade de atualização de status será implementada em breve")
    
    def delete_agendamento(self):
        """Cancelar agendamento selecionado"""
        messagebox.showinfo("Info", "Funcionalidade de cancelamento será implementada em breve")
    
    # MÉTODO DE DIÁLOGO - RESULTADOS
    
    def add_resultado_dialog(self):
        """Diálogo para adicionar resultado"""
        messagebox.showinfo("Info", "Funcionalidade de resultados será implementada em breve")
    
    # MÉTODOS DE RELATÓRIOS
    
    def show_exames_proximos(self):
        """Mostrar relatório de exames próximos"""
        try:
            exames = self.model.get_exames_proximos()
            
            self.relatorio_text.delete("1.0", tk.END)
            self.relatorio_text.insert("1.0", "=== EXAMES PRÓXIMOS ===\n\n")
            
            if exames:
                for exame in exames:
                    data_formatada = exame['data_hora'].strftime('%d/%m/%Y %H:%M')
                    texto = f"PRIORIDADE: {exame['prioridade']}\n"
                    texto += f"Paciente: {exame['paciente']}\n"
                    texto += f"Exame: {exame['exame']}\n"
                    texto += f"Data/Hora: {data_formatada}\n"
                    texto += f"Unidade: {exame['unidade']}\n"
                    texto += "-" * 50 + "\n\n"
                    self.relatorio_text.insert(tk.END, texto)
            else:
                self.relatorio_text.insert(tk.END, "Nenhum exame próximo encontrado.\n")
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
                    texto = f"Profissional: {item['profissional']}\n"
                    texto += f"Exame: {item['exame']}\n"
                    texto += f"Total de Agendamentos: {item['total']}\n"
                    texto += "-" * 40 + "\n\n"
                    self.relatorio_text.insert(tk.END, texto)
            else:
                self.relatorio_text.insert(tk.END, "Nenhum dado encontrado.\n")
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
                    
                    data_nasc = item['data_nasc'].strftime('%d/%m/%Y') if item['data_nasc'] else ''
                    texto = f"  • {item['paciente']} - CPF: {item['cpf']} - Nasc: {data_nasc}\n"
                    self.relatorio_text.insert(tk.END, texto)
            else:
                self.relatorio_text.insert(tk.END, "Nenhum paciente vinculado a empresas encontrado.\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def run(self):
        """Executar aplicação"""
        self.root.mainloop()
