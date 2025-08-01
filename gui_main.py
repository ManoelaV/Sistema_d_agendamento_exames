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
        dialog = ttk_boot.Toplevel(self.root)
        dialog.title("Novo Exame")
        dialog.geometry("700x650")
        dialog.grab_set()
        
        # Frame principal com scrollbar
        canvas = tk.Canvas(dialog)
        scrollbar = ttk_boot.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk_boot.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        ttk_boot.Label(scrollable_frame, text="Cadastro de Novo Exame", 
                      style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos básicos
        basic_frame = ttk_boot.LabelFrame(scrollable_frame, text="Informações Básicas", padding=10)
        basic_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        basic_frame.columnconfigure(1, weight=1)
        
        # Nome
        ttk_boot.Label(basic_frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        nome_var = tk.StringVar()
        ttk_boot.Entry(basic_frame, textvariable=nome_var, width=50).grid(row=0, column=1, sticky="ew", pady=5, padx=(10,0))
        
        # Descrição
        ttk_boot.Label(basic_frame, text="Descrição:").grid(row=1, column=0, sticky="nw", pady=5)
        descricao_text = tk.Text(basic_frame, width=45, height=3, wrap="word")
        descricao_text.grid(row=1, column=1, sticky="ew", pady=5, padx=(10,0))
        
        # Requisitos
        ttk_boot.Label(basic_frame, text="Requisitos:").grid(row=2, column=0, sticky="nw", pady=5)
        requisitos_text = tk.Text(basic_frame, width=45, height=3, wrap="word")
        requisitos_text.grid(row=2, column=1, sticky="ew", pady=5, padx=(10,0))
        
        # Tempo Estimado
        ttk_boot.Label(basic_frame, text="Tempo Estimado (min):").grid(row=3, column=0, sticky="w", pady=5)
        tempo_var = tk.StringVar()
        ttk_boot.Entry(basic_frame, textvariable=tempo_var, width=20).grid(row=3, column=1, sticky="w", pady=5, padx=(10,0))
        
        # Tipo de Exame
        ttk_boot.Label(basic_frame, text="Tipo de Exame:").grid(row=4, column=0, sticky="w", pady=5)
        tipo_var = tk.StringVar()
        tipo_combo = ttk_boot.Combobox(basic_frame, textvariable=tipo_var, 
                                       values=["LABORATORIAL", "IMAGEM", "CLINICO"], 
                                       state="readonly", width=30)
        tipo_combo.grid(row=4, column=1, sticky="w", pady=5, padx=(10,0))
        
        # Campos específicos por tipo
        specific_frame = ttk_boot.LabelFrame(scrollable_frame, text="Campos Específicos por Tipo", padding=10)
        specific_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        specific_frame.columnconfigure(1, weight=1)
        
        # Campos LABORATORIAL
        lab_frame = ttk_boot.LabelFrame(specific_frame, text="Específicos para LABORATORIAL", padding=10)
        lab_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        lab_frame.columnconfigure(1, weight=1)
        
        ttk_boot.Label(lab_frame, text="Tempo Coleta/Análise (min):").grid(row=0, column=0, sticky="w", pady=3)
        tempo_coleta_var = tk.StringVar()
        ttk_boot.Entry(lab_frame, textvariable=tempo_coleta_var, width=20).grid(row=0, column=1, sticky="w", pady=3, padx=(10,0))
        
        ttk_boot.Label(lab_frame, text="Restrições Alimentares:").grid(row=1, column=0, sticky="nw", pady=3)
        restricoes_text = tk.Text(lab_frame, width=40, height=2, wrap="word")
        restricoes_text.grid(row=1, column=1, sticky="ew", pady=3, padx=(10,0))
        
        # Campos IMAGEM
        img_frame = ttk_boot.LabelFrame(specific_frame, text="Específicos para IMAGEM", padding=10)
        img_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        img_frame.columnconfigure(1, weight=1)
        
        ttk_boot.Label(img_frame, text="Tecnologia Utilizada:").grid(row=0, column=0, sticky="w", pady=3)
        tecnologia_var = tk.StringVar()
        ttk_boot.Entry(img_frame, textvariable=tecnologia_var, width=40).grid(row=0, column=1, sticky="ew", pady=3, padx=(10,0))
        
        ttk_boot.Label(img_frame, text="Preparos Especiais:").grid(row=1, column=0, sticky="nw", pady=3)
        preparos_text = tk.Text(img_frame, width=40, height=2, wrap="word")
        preparos_text.grid(row=1, column=1, sticky="ew", pady=3, padx=(10,0))
        
        # Campos CLINICO
        clin_frame = ttk_boot.LabelFrame(specific_frame, text="Específicos para CLÍNICO", padding=10)
        clin_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        clin_frame.columnconfigure(1, weight=1)
        
        ttk_boot.Label(clin_frame, text="Tempo Médio Consulta (min):").grid(row=0, column=0, sticky="w", pady=3)
        tempo_consulta_var = tk.StringVar()
        ttk_boot.Entry(clin_frame, textvariable=tempo_consulta_var, width=20).grid(row=0, column=1, sticky="w", pady=3, padx=(10,0))
        
        ttk_boot.Label(clin_frame, text="Especialidade Médica:").grid(row=1, column=0, sticky="w", pady=3)
        especialidade_var = tk.StringVar()
        ttk_boot.Entry(clin_frame, textvariable=especialidade_var, width=40).grid(row=1, column=1, sticky="ew", pady=3, padx=(10,0))
        
        # Campo comum - Intervalo de Limpeza
        common_frame = ttk_boot.LabelFrame(scrollable_frame, text="Configurações Gerais", padding=10)
        common_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        common_frame.columnconfigure(1, weight=1)
        
        ttk_boot.Label(common_frame, text="Intervalo Limpeza (min):").grid(row=0, column=0, sticky="w", pady=5)
        intervalo_var = tk.StringVar(value="15")  # Valor padrão
        ttk_boot.Entry(common_frame, textvariable=intervalo_var, width=20).grid(row=0, column=1, sticky="w", pady=5, padx=(10,0))
        
        # Instruções
        instr_frame = ttk_boot.LabelFrame(scrollable_frame, text="Instruções", padding=10)
        instr_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        instruction_text = (
            "• Nome e tempo estimado são obrigatórios\n"
            "• Selecione o tipo de exame para habilitar campos específicos\n"
            "• LABORATORIAL: Tempo de coleta/análise e restrições alimentares\n"
            "• IMAGEM: Tecnologia utilizada e preparos especiais\n"
            "• CLÍNICO: Tempo de consulta e especialidade médica\n"
            "• Intervalo de limpeza padrão: 15 minutos"
        )
        ttk_boot.Label(instr_frame, text=instruction_text, justify="left").pack(anchor="w")
        
        # Função para habilitar/desabilitar campos específicos
        def on_tipo_change(event=None):
            tipo = tipo_var.get()
            
            # Resetar todos os campos específicos
            for widget in [tempo_coleta_var, restricoes_text, tecnologia_var, preparos_text, 
                          tempo_consulta_var, especialidade_var]:
                if isinstance(widget, tk.StringVar):
                    widget.set("")
                else:
                    widget.delete("1.0", tk.END)
            
            # Configurar frames baseado no tipo
            if tipo == "LABORATORIAL":
                lab_frame.configure(style="success.TLabelframe")
                img_frame.configure(style="secondary.TLabelframe")
                clin_frame.configure(style="secondary.TLabelframe")
            elif tipo == "IMAGEM":
                lab_frame.configure(style="secondary.TLabelframe")
                img_frame.configure(style="success.TLabelframe")
                clin_frame.configure(style="secondary.TLabelframe")
            elif tipo == "CLINICO":
                lab_frame.configure(style="secondary.TLabelframe")
                img_frame.configure(style="secondary.TLabelframe")
                clin_frame.configure(style="success.TLabelframe")
        
        tipo_combo.bind("<<ComboboxSelected>>", on_tipo_change)
        
        # Botões
        button_frame = ttk_boot.Frame(scrollable_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def salvar():
            try:
                # Validar campos obrigatórios
                if not nome_var.get().strip():
                    messagebox.showerror("Erro", "Nome é obrigatório")
                    return
                
                if not tempo_var.get().strip():
                    messagebox.showerror("Erro", "Tempo estimado é obrigatório")
                    return
                
                if not tipo_var.get():
                    messagebox.showerror("Erro", "Selecione o tipo de exame")
                    return
                
                # Validar tempo estimado
                try:
                    tempo_estimado = int(tempo_var.get())
                    if tempo_estimado <= 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Erro", "Tempo estimado deve ser um número inteiro positivo")
                    return
                
                # Validar intervalo de limpeza
                try:
                    intervalo_limpeza = int(intervalo_var.get())
                    if intervalo_limpeza < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Erro", "Intervalo de limpeza deve ser um número inteiro não negativo")
                    return
                
                # Preparar dados básicos
                nome = nome_var.get().strip()
                descricao = descricao_text.get("1.0", tk.END).strip() or None
                requisitos = requisitos_text.get("1.0", tk.END).strip() or None
                tipo = tipo_var.get()
                
                # Preparar campos específicos baseado no tipo
                kwargs = {"intervalo_limpeza": intervalo_limpeza}
                
                if tipo == "LABORATORIAL":
                    if tempo_coleta_var.get().strip():
                        try:
                            kwargs["tempo_coleta_analise"] = int(tempo_coleta_var.get())
                        except ValueError:
                            messagebox.showerror("Erro", "Tempo de coleta/análise deve ser um número inteiro")
                            return
                    
                    restricoes = restricoes_text.get("1.0", tk.END).strip()
                    if restricoes:
                        kwargs["restricoes_alimentares"] = restricoes
                
                elif tipo == "IMAGEM":
                    tecnologia = tecnologia_var.get().strip()
                    if tecnologia:
                        kwargs["tecnologia_utilizada"] = tecnologia
                    
                    preparos = preparos_text.get("1.0", tk.END).strip()
                    if preparos:
                        kwargs["preparos_especiais"] = preparos
                
                elif tipo == "CLINICO":
                    if tempo_consulta_var.get().strip():
                        try:
                            kwargs["tempo_medio_consulta"] = int(tempo_consulta_var.get())
                        except ValueError:
                            messagebox.showerror("Erro", "Tempo médio de consulta deve ser um número inteiro")
                            return
                    
                    especialidade = especialidade_var.get().strip()
                    if especialidade:
                        kwargs["especialidade_medica"] = especialidade
                
                # Salvar exame
                if self.model.add_exame(nome, descricao, requisitos, tempo_estimado, tipo, **kwargs):
                    messagebox.showinfo("Sucesso", "Exame cadastrado com sucesso!")
                    dialog.destroy()
                    self.refresh_data("exames")
                else:
                    messagebox.showerror("Erro", "Erro ao cadastrar exame")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        
        def limpar():
            nome_var.set("")
            descricao_text.delete("1.0", tk.END)
            requisitos_text.delete("1.0", tk.END)
            tempo_var.set("")
            tipo_combo.set("")
            tempo_coleta_var.set("")
            restricoes_text.delete("1.0", tk.END)
            tecnologia_var.set("")
            preparos_text.delete("1.0", tk.END)
            tempo_consulta_var.set("")
            especialidade_var.set("")
            intervalo_var.set("15")
            
            # Resetar estilos
            lab_frame.configure(style="TLabelframe")
            img_frame.configure(style="TLabelframe")
            clin_frame.configure(style="TLabelframe")
        
        ttk_boot.Button(button_frame, text="Salvar", command=salvar, bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Limpar", command=limpar, bootstyle="warning").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="secondary").pack(side="left", padx=5)
        
        # Configurar scroll com mouse wheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def edit_exame_dialog(self):
        """Diálogo para editar exame"""
        selection = self.exames_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um exame para editar")
            return
        
        item = self.exames_tree.item(selection[0])
        id_exame = item['values'][0]
        
        # Buscar dados do exame
        exame = self.model.get_exame_by_id(id_exame)
        if not exame:
            messagebox.showerror("Erro", "Exame não encontrado")
            return
        
        dialog = ttk_boot.Toplevel(self.root)
        dialog.title(f"Editar Exame - {exame['nome']}")
        dialog.geometry("700x650")
        dialog.grab_set()
        
        # Frame principal com scrollbar
        canvas = tk.Canvas(dialog)
        scrollbar = ttk_boot.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk_boot.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        ttk_boot.Label(scrollable_frame, text=f"Editar Exame: {exame['nome']}", 
                      style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos básicos
        basic_frame = ttk_boot.LabelFrame(scrollable_frame, text="Informações Básicas", padding=10)
        basic_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        basic_frame.columnconfigure(1, weight=1)
        
        # Nome
        ttk_boot.Label(basic_frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        nome_var = tk.StringVar(value=exame['nome'])
        ttk_boot.Entry(basic_frame, textvariable=nome_var, width=50).grid(row=0, column=1, sticky="ew", pady=5, padx=(10,0))
        
        # Descrição
        ttk_boot.Label(basic_frame, text="Descrição:").grid(row=1, column=0, sticky="nw", pady=5)
        descricao_text = tk.Text(basic_frame, width=45, height=3, wrap="word")
        descricao_text.grid(row=1, column=1, sticky="ew", pady=5, padx=(10,0))
        if exame['descricao']:
            descricao_text.insert("1.0", exame['descricao'])
        
        # Requisitos
        ttk_boot.Label(basic_frame, text="Requisitos:").grid(row=2, column=0, sticky="nw", pady=5)
        requisitos_text = tk.Text(basic_frame, width=45, height=3, wrap="word")
        requisitos_text.grid(row=2, column=1, sticky="ew", pady=5, padx=(10,0))
        if exame['requisitos']:
            requisitos_text.insert("1.0", exame['requisitos'])
        
        # Tempo Estimado
        ttk_boot.Label(basic_frame, text="Tempo Estimado (min):").grid(row=3, column=0, sticky="w", pady=5)
        tempo_var = tk.StringVar(value=str(exame['tempo_estimado']))
        ttk_boot.Entry(basic_frame, textvariable=tempo_var, width=20).grid(row=3, column=1, sticky="w", pady=5, padx=(10,0))
        
        # Tipo de Exame
        ttk_boot.Label(basic_frame, text="Tipo de Exame:").grid(row=4, column=0, sticky="w", pady=5)
        tipo_var = tk.StringVar(value=exame['tipo'])
        tipo_combo = ttk_boot.Combobox(basic_frame, textvariable=tipo_var, 
                                       values=["LABORATORIAL", "IMAGEM", "CLINICO"], 
                                       state="readonly", width=30)
        tipo_combo.grid(row=4, column=1, sticky="w", pady=5, padx=(10,0))
        
        # Campos específicos por tipo
        specific_frame = ttk_boot.LabelFrame(scrollable_frame, text="Campos Específicos por Tipo", padding=10)
        specific_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        specific_frame.columnconfigure(1, weight=1)
        
        # Campos LABORATORIAL
        lab_frame = ttk_boot.LabelFrame(specific_frame, text="Específicos para LABORATORIAL", padding=10)
        lab_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        lab_frame.columnconfigure(1, weight=1)
        
        ttk_boot.Label(lab_frame, text="Tempo Coleta/Análise (min):").grid(row=0, column=0, sticky="w", pady=3)
        tempo_coleta_var = tk.StringVar(value=str(exame['tempo_coleta_analise']) if exame['tempo_coleta_analise'] else "")
        ttk_boot.Entry(lab_frame, textvariable=tempo_coleta_var, width=20).grid(row=0, column=1, sticky="w", pady=3, padx=(10,0))
        
        ttk_boot.Label(lab_frame, text="Restrições Alimentares:").grid(row=1, column=0, sticky="nw", pady=3)
        restricoes_text = tk.Text(lab_frame, width=40, height=2, wrap="word")
        restricoes_text.grid(row=1, column=1, sticky="ew", pady=3, padx=(10,0))
        if exame['restricoes_alimentares']:
            restricoes_text.insert("1.0", exame['restricoes_alimentares'])
        
        # Campos IMAGEM
        img_frame = ttk_boot.LabelFrame(specific_frame, text="Específicos para IMAGEM", padding=10)
        img_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        img_frame.columnconfigure(1, weight=1)
        
        ttk_boot.Label(img_frame, text="Tecnologia Utilizada:").grid(row=0, column=0, sticky="w", pady=3)
        tecnologia_var = tk.StringVar(value=exame['tecnologia_utilizada'] if exame['tecnologia_utilizada'] else "")
        ttk_boot.Entry(img_frame, textvariable=tecnologia_var, width=40).grid(row=0, column=1, sticky="ew", pady=3, padx=(10,0))
        
        ttk_boot.Label(img_frame, text="Preparos Especiais:").grid(row=1, column=0, sticky="nw", pady=3)
        preparos_text = tk.Text(img_frame, width=40, height=2, wrap="word")
        preparos_text.grid(row=1, column=1, sticky="ew", pady=3, padx=(10,0))
        if exame['preparos_especiais']:
            preparos_text.insert("1.0", exame['preparos_especiais'])
        
        # Campos CLINICO
        clin_frame = ttk_boot.LabelFrame(specific_frame, text="Específicos para CLÍNICO", padding=10)
        clin_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        clin_frame.columnconfigure(1, weight=1)
        
        ttk_boot.Label(clin_frame, text="Tempo Médio Consulta (min):").grid(row=0, column=0, sticky="w", pady=3)
        tempo_consulta_var = tk.StringVar(value=str(exame['tempo_medio_consulta']) if exame['tempo_medio_consulta'] else "")
        ttk_boot.Entry(clin_frame, textvariable=tempo_consulta_var, width=20).grid(row=0, column=1, sticky="w", pady=3, padx=(10,0))
        
        ttk_boot.Label(clin_frame, text="Especialidade Médica:").grid(row=1, column=0, sticky="w", pady=3)
        especialidade_var = tk.StringVar(value=exame['especialidade_medica'] if exame['especialidade_medica'] else "")
        ttk_boot.Entry(clin_frame, textvariable=especialidade_var, width=40).grid(row=1, column=1, sticky="ew", pady=3, padx=(10,0))
        
        # Campo comum - Intervalo de Limpeza
        common_frame = ttk_boot.LabelFrame(scrollable_frame, text="Configurações Gerais", padding=10)
        common_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        common_frame.columnconfigure(1, weight=1)
        
        ttk_boot.Label(common_frame, text="Intervalo Limpeza (min):").grid(row=0, column=0, sticky="w", pady=5)
        intervalo_var = tk.StringVar(value=str(exame['intervalo_limpeza']) if exame['intervalo_limpeza'] else "15")
        ttk_boot.Entry(common_frame, textvariable=intervalo_var, width=20).grid(row=0, column=1, sticky="w", pady=5, padx=(10,0))
        
        # Função para destacar campos específicos
        def highlight_specific_fields():
            tipo = exame['tipo']
            if tipo == "LABORATORIAL":
                lab_frame.configure(style="success.TLabelframe")
                img_frame.configure(style="secondary.TLabelframe")
                clin_frame.configure(style="secondary.TLabelframe")
            elif tipo == "IMAGEM":
                lab_frame.configure(style="secondary.TLabelframe")
                img_frame.configure(style="success.TLabelframe")
                clin_frame.configure(style="secondary.TLabelframe")
            elif tipo == "CLINICO":
                lab_frame.configure(style="secondary.TLabelframe")
                img_frame.configure(style="secondary.TLabelframe")
                clin_frame.configure(style="success.TLabelframe")
        
        # Aplicar destaque inicial
        highlight_specific_fields()
        
        # Função para mudança de tipo
        def on_tipo_change(event=None):
            highlight_specific_fields()
        
        tipo_combo.bind("<<ComboboxSelected>>", on_tipo_change)
        
        # Botões
        button_frame = ttk_boot.Frame(scrollable_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def salvar():
            try:
                # Validar campos obrigatórios
                if not nome_var.get().strip():
                    messagebox.showerror("Erro", "Nome é obrigatório")
                    return
                
                if not tempo_var.get().strip():
                    messagebox.showerror("Erro", "Tempo estimado é obrigatório")
                    return
                
                if not tipo_var.get():
                    messagebox.showerror("Erro", "Selecione o tipo de exame")
                    return
                
                # Validar tempo estimado
                try:
                    tempo_estimado = int(tempo_var.get())
                    if tempo_estimado <= 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Erro", "Tempo estimado deve ser um número inteiro positivo")
                    return
                
                # Validar intervalo de limpeza
                try:
                    intervalo_limpeza = int(intervalo_var.get())
                    if intervalo_limpeza < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Erro", "Intervalo de limpeza deve ser um número inteiro não negativo")
                    return
                
                # Preparar dados básicos
                nome = nome_var.get().strip()
                descricao = descricao_text.get("1.0", tk.END).strip() or None
                requisitos = requisitos_text.get("1.0", tk.END).strip() or None
                tipo = tipo_var.get()
                
                # Preparar campos específicos baseado no tipo
                kwargs = {"intervalo_limpeza": intervalo_limpeza}
                
                if tipo == "LABORATORIAL":
                    if tempo_coleta_var.get().strip():
                        try:
                            kwargs["tempo_coleta_analise"] = int(tempo_coleta_var.get())
                        except ValueError:
                            messagebox.showerror("Erro", "Tempo de coleta/análise deve ser um número inteiro")
                            return
                    else:
                        kwargs["tempo_coleta_analise"] = None
                    
                    restricoes = restricoes_text.get("1.0", tk.END).strip()
                    kwargs["restricoes_alimentares"] = restricoes if restricoes else None
                    
                    # Limpar campos de outros tipos
                    kwargs["tecnologia_utilizada"] = None
                    kwargs["preparos_especiais"] = None
                    kwargs["tempo_medio_consulta"] = None
                    kwargs["especialidade_medica"] = None
                
                elif tipo == "IMAGEM":
                    tecnologia = tecnologia_var.get().strip()
                    kwargs["tecnologia_utilizada"] = tecnologia if tecnologia else None
                    
                    preparos = preparos_text.get("1.0", tk.END).strip()
                    kwargs["preparos_especiais"] = preparos if preparos else None
                    
                    # Limpar campos de outros tipos
                    kwargs["tempo_coleta_analise"] = None
                    kwargs["restricoes_alimentares"] = None
                    kwargs["tempo_medio_consulta"] = None
                    kwargs["especialidade_medica"] = None
                
                elif tipo == "CLINICO":
                    if tempo_consulta_var.get().strip():
                        try:
                            kwargs["tempo_medio_consulta"] = int(tempo_consulta_var.get())
                        except ValueError:
                            messagebox.showerror("Erro", "Tempo médio de consulta deve ser um número inteiro")
                            return
                    else:
                        kwargs["tempo_medio_consulta"] = None
                    
                    especialidade = especialidade_var.get().strip()
                    kwargs["especialidade_medica"] = especialidade if especialidade else None
                    
                    # Limpar campos de outros tipos
                    kwargs["tempo_coleta_analise"] = None
                    kwargs["restricoes_alimentares"] = None
                    kwargs["tecnologia_utilizada"] = None
                    kwargs["preparos_especiais"] = None
                
                # Atualizar exame
                if self.model.update_exame(id_exame, nome, descricao, requisitos, tempo_estimado, tipo, **kwargs):
                    messagebox.showinfo("Sucesso", "Exame atualizado com sucesso!")
                    dialog.destroy()
                    self.refresh_data("exames")
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar exame")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        
        ttk_boot.Button(button_frame, text="Salvar", command=salvar, bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="secondary").pack(side="left", padx=5)
        
        # Configurar scroll com mouse wheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
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
        dialog = ttk_boot.Toplevel(self.root)
        dialog.title("Novo Agendamento")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk_boot.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ttk_boot.Label(main_frame, text="Novo Agendamento", 
                      style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Paciente
        ttk_boot.Label(main_frame, text="Paciente:").grid(row=1, column=0, sticky="w", pady=5)
        paciente_var = tk.StringVar()
        paciente_combo = ttk_boot.Combobox(main_frame, textvariable=paciente_var, width=50, state="readonly")
        paciente_combo.grid(row=1, column=1, pady=5, padx=(10,0))
        
        # Carregar pacientes
        pacientes = self.model.get_pacientes()
        paciente_values = []
        paciente_ids = []
        if pacientes:
            for pac in pacientes:
                display_text = f"{pac['nome']} - CPF: {pac['cpf']}"
                paciente_values.append(display_text)
                paciente_ids.append(pac['id_paciente'])
        
        paciente_combo['values'] = paciente_values
        
        # Exame
        ttk_boot.Label(main_frame, text="Exame:").grid(row=2, column=0, sticky="w", pady=5)
        exame_var = tk.StringVar()
        exame_combo = ttk_boot.Combobox(main_frame, textvariable=exame_var, width=50, state="readonly")
        exame_combo.grid(row=2, column=1, pady=5, padx=(10,0))
        
        # Carregar exames
        exames = self.model.get_exames()
        exame_values = []
        exame_ids = []
        if exames:
            for exame in exames:
                display_text = f"{exame['nome']} ({exame['tipo']}) - {exame['tempo_estimado']}min"
                exame_values.append(display_text)
                exame_ids.append(exame['id_exame'])
        
        exame_combo['values'] = exame_values
        
        # Unidade
        ttk_boot.Label(main_frame, text="Unidade:").grid(row=3, column=0, sticky="w", pady=5)
        unidade_var = tk.StringVar()
        unidade_combo = ttk_boot.Combobox(main_frame, textvariable=unidade_var, width=50, state="readonly")
        unidade_combo.grid(row=3, column=1, pady=5, padx=(10,0))
        
        # Carregar unidades
        unidades = self.model.get_unidades()
        unidade_values = []
        unidade_ids = []
        if unidades:
            for unidade in unidades:
                display_text = f"Unidade {unidade['id_unidade']} - {unidade['endereco']}"
                unidade_values.append(display_text)
                unidade_ids.append(unidade['id_unidade'])
        
        unidade_combo['values'] = unidade_values
        
        # Profissional (opcional)
        ttk_boot.Label(main_frame, text="Profissional:").grid(row=4, column=0, sticky="w", pady=5)
        profissional_var = tk.StringVar()
        profissional_combo = ttk_boot.Combobox(main_frame, textvariable=profissional_var, width=50, state="readonly")
        profissional_combo.grid(row=4, column=1, pady=5, padx=(10,0))
        
        # Carregar profissionais
        profissionais = self.model.get_profissionais()
        profissional_values = ["Nenhum"]
        profissional_ids = [None]
        if profissionais:
            for prof in profissionais:
                display_text = f"{prof['nome']} - {prof['especialidade']}"
                profissional_values.append(display_text)
                profissional_ids.append(prof['id_profissional'])
        
        profissional_combo['values'] = profissional_values
        profissional_combo.set("Nenhum")
        
        # Data
        ttk_boot.Label(main_frame, text="Data:").grid(row=5, column=0, sticky="w", pady=5)
        data_var = tk.StringVar()
        data_entry = ttk_boot.Entry(main_frame, textvariable=data_var, width=20)
        data_entry.grid(row=5, column=1, pady=5, padx=(10,0), sticky="w")
        ttk_boot.Label(main_frame, text="(DD/MM/AAAA)", font=("Arial", 8)).grid(row=5, column=1, padx=(200,0), sticky="w")
        
        # Hora
        ttk_boot.Label(main_frame, text="Hora:").grid(row=6, column=0, sticky="w", pady=5)
        hora_var = tk.StringVar()
        hora_entry = ttk_boot.Entry(main_frame, textvariable=hora_var, width=20)
        hora_entry.grid(row=6, column=1, pady=5, padx=(10,0), sticky="w")
        ttk_boot.Label(main_frame, text="(HH:MM)", font=("Arial", 8)).grid(row=6, column=1, padx=(200,0), sticky="w")
        
        # Frame para validações
        valid_frame = ttk_boot.LabelFrame(main_frame, text="Validações", padding=10)
        valid_frame.grid(row=7, column=0, columnspan=2, pady=20, sticky="ew")
        
        # Documentos OK
        documentos_var = tk.BooleanVar()
        ttk_boot.Checkbutton(valid_frame, text="Documentos OK", 
                            variable=documentos_var).grid(row=0, column=0, sticky="w", padx=10)
        
        # Requisitos OK
        requisitos_var = tk.BooleanVar()
        ttk_boot.Checkbutton(valid_frame, text="Requisitos OK", 
                            variable=requisitos_var).grid(row=0, column=1, sticky="w", padx=10)
        
        # Botões
        button_frame = ttk_boot.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        def salvar():
            try:
                # Validar campos obrigatórios
                if paciente_combo.current() < 0:
                    messagebox.showerror("Erro", "Selecione um paciente")
                    return
                
                if exame_combo.current() < 0:
                    messagebox.showerror("Erro", "Selecione um exame")
                    return
                
                if unidade_combo.current() < 0:
                    messagebox.showerror("Erro", "Selecione uma unidade")
                    return
                
                if not data_var.get().strip() or not hora_var.get().strip():
                    messagebox.showerror("Erro", "Data e hora são obrigatórios")
                    return
                
                # Converter data e hora
                try:
                    data_hora_str = f"{data_var.get()} {hora_var.get()}"
                    data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
                except ValueError:
                    messagebox.showerror("Erro", "Data ou hora inválida. Use DD/MM/AAAA e HH:MM")
                    return
                
                # Obter IDs selecionados
                id_paciente = paciente_ids[paciente_combo.current()]
                id_exame = exame_ids[exame_combo.current()]
                id_unidade = unidade_ids[unidade_combo.current()]
                
                prof_idx = profissional_combo.current()
                id_profissional = profissional_ids[prof_idx] if prof_idx >= 0 else None
                
                # Salvar agendamento
                if self.model.add_agendamento(id_paciente, id_exame, id_unidade, data_hora, id_profissional):
                    messagebox.showinfo("Sucesso", "Agendamento criado com sucesso!")
                    dialog.destroy()
                    self.refresh_data("agendamentos")
                else:
                    messagebox.showerror("Erro", "Erro ao criar agendamento")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        
        ttk_boot.Button(button_frame, text="Salvar", command=salvar, bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="secondary").pack(side="left", padx=5)
    
    def update_status_dialog(self):
        """Diálogo para atualizar status do agendamento"""
        selection = self.agendamentos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um agendamento para atualizar")
            return
        
        item = self.agendamentos_tree.item(selection[0])
        id_agendamento = item['values'][0]
        paciente_nome = item['values'][1]
        exame_nome = item['values'][2]
        status_atual = item['values'][4]
        
        dialog = ttk_boot.Toplevel(self.root)
        dialog.title("Atualizar Status do Agendamento")
        dialog.geometry("400x300")
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk_boot.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Informações do agendamento
        info_frame = ttk_boot.LabelFrame(main_frame, text="Agendamento", padding=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ttk_boot.Label(info_frame, text=f"Paciente: {paciente_nome}").pack(anchor="w")
        ttk_boot.Label(info_frame, text=f"Exame: {exame_nome}").pack(anchor="w")
        ttk_boot.Label(info_frame, text=f"Status Atual: {status_atual}").pack(anchor="w")
        
        # Novo status
        ttk_boot.Label(main_frame, text="Novo Status:").pack(anchor="w", pady=(0, 5))
        status_var = tk.StringVar(value=status_atual)
        status_combo = ttk_boot.Combobox(main_frame, textvariable=status_var, 
                                        values=["AGENDADO", "REALIZADO", "CANCELADO"], 
                                        state="readonly", width=30)
        status_combo.pack(anchor="w", pady=(0, 10))
        
        # Validações (apenas para status REALIZADO)
        valid_frame = ttk_boot.LabelFrame(main_frame, text="Validações (para REALIZADO)", padding=10)
        valid_frame.pack(fill="x", pady=(0, 20))
        
        documentos_var = tk.BooleanVar()
        ttk_boot.Checkbutton(valid_frame, text="Documentos OK", 
                            variable=documentos_var).pack(anchor="w")
        
        requisitos_var = tk.BooleanVar()
        ttk_boot.Checkbutton(valid_frame, text="Requisitos OK", 
                            variable=requisitos_var).pack(anchor="w")
        
        # Botões
        button_frame = ttk_boot.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        def salvar():
            try:
                novo_status = status_var.get()
                
                # Validar se status REALIZADO tem validações
                if novo_status == "REALIZADO":
                    if not documentos_var.get() or not requisitos_var.get():
                        messagebox.showerror("Erro", "Para status REALIZADO, documentos e requisitos devem estar OK")
                        return
                
                # Atualizar status
                documentos_ok = documentos_var.get() if novo_status == "REALIZADO" else None
                requisitos_ok = requisitos_var.get() if novo_status == "REALIZADO" else None
                
                if self.model.update_agendamento_status(id_agendamento, novo_status, documentos_ok, requisitos_ok):
                    messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")
                    dialog.destroy()
                    self.refresh_data("agendamentos")
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar status")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        
        ttk_boot.Button(button_frame, text="Salvar", command=salvar, bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="secondary").pack(side="left", padx=5)
    
    def delete_agendamento(self):
        """Cancelar agendamento selecionado"""
        selection = self.agendamentos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um agendamento para cancelar")
            return
        
        item = self.agendamentos_tree.item(selection[0])
        id_agendamento = item['values'][0]
        paciente_nome = item['values'][1]
        exame_nome = item['values'][2]
        status_atual = item['values'][4]
        
        if status_atual == "CANCELADO":
            messagebox.showwarning("Aviso", "Este agendamento já está cancelado")
            return
        
        if messagebox.askyesno("Confirmação", 
                              f"Deseja cancelar o agendamento?\n\nPaciente: {paciente_nome}\nExame: {exame_nome}"):
            try:
                if self.model.update_agendamento_status(id_agendamento, "CANCELADO"):
                    messagebox.showinfo("Sucesso", "Agendamento cancelado com sucesso!")
                    self.refresh_data("agendamentos")
                else:
                    messagebox.showerror("Erro", "Erro ao cancelar agendamento")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
    
    # MÉTODO DE DIÁLOGO - RESULTADOS
    
    def add_resultado_dialog(self):
        """Diálogo para adicionar resultado"""
        dialog = ttk_boot.Toplevel(self.root)
        dialog.title("Novo Resultado")
        dialog.geometry("700x600")
        dialog.grab_set()
        
        # Frame principal
        main_frame = ttk_boot.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ttk_boot.Label(main_frame, text="Novo Resultado", 
                      style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Agendamento (apenas exames REALIZADOS)
        ttk_boot.Label(main_frame, text="Agendamento:").grid(row=1, column=0, sticky="w", pady=5)
        agendamento_var = tk.StringVar()
        agendamento_combo = ttk_boot.Combobox(main_frame, textvariable=agendamento_var, width=70, state="readonly")
        agendamento_combo.grid(row=1, column=1, pady=5, padx=(10,0))
        
        # Carregar apenas agendamentos REALIZADOS que não têm resultado
        agendamentos_realizados = self.model.get_agendamentos_realizados_sem_resultado()
        agendamento_values = []
        agendamento_ids = []
        
        if agendamentos_realizados:
            for agend in agendamentos_realizados:
                data_formatada = agend['data_hora'].strftime('%d/%m/%Y %H:%M')
                display_text = f"{agend['paciente_nome']} - {agend['exame_nome']} ({data_formatada})"
                agendamento_values.append(display_text)
                agendamento_ids.append(agend['id_agendamento'])
        
        agendamento_combo['values'] = agendamento_values
        
        if not agendamentos_realizados:
            ttk_boot.Label(main_frame, text="Nenhum exame realizado sem resultado encontrado", 
                          foreground="red").grid(row=2, column=0, columnspan=2, pady=10)
        
        # Resultados
        ttk_boot.Label(main_frame, text="Resultados:").grid(row=3, column=0, sticky="nw", pady=5)
        resultados_text = tk.Text(main_frame, width=60, height=15, wrap="word")
        resultados_text.grid(row=3, column=1, pady=5, padx=(10,0))
        
        # Scrollbar para resultados
        result_scrollbar = ttk_boot.Scrollbar(main_frame, orient="vertical", command=resultados_text.yview)
        result_scrollbar.grid(row=3, column=2, sticky="ns", pady=5)
        resultados_text.configure(yscrollcommand=result_scrollbar.set)
        
        # Recomendações (opcional)
        ttk_boot.Label(main_frame, text="Recomendações:").grid(row=4, column=0, sticky="nw", pady=5)
        recomendacoes_text = tk.Text(main_frame, width=60, height=8, wrap="word")
        recomendacoes_text.grid(row=4, column=1, pady=5, padx=(10,0))
        
        # Scrollbar para recomendações
        recom_scrollbar = ttk_boot.Scrollbar(main_frame, orient="vertical", command=recomendacoes_text.yview)
        recom_scrollbar.grid(row=4, column=2, sticky="ns", pady=5)
        recomendacoes_text.configure(yscrollcommand=recom_scrollbar.set)
        
        # Frame de instrução
        instr_frame = ttk_boot.LabelFrame(main_frame, text="Instruções", padding=10)
        instr_frame.grid(row=5, column=0, columnspan=3, pady=20, sticky="ew")
        
        instruction_text = ("• Selecione um agendamento com status REALIZADO\n"
                           "• Digite os resultados detalhados do exame\n"
                           "• Adicione recomendações médicas se necessário\n"
                           "• Apenas exames sem resultado podem ser cadastrados")
        ttk_boot.Label(instr_frame, text=instruction_text, justify="left").pack(anchor="w")
        
        # Botões
        button_frame = ttk_boot.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        def salvar():
            try:
                # Validar agendamento selecionado
                if agendamento_combo.current() < 0:
                    messagebox.showerror("Erro", "Selecione um agendamento")
                    return
                
                # Validar resultados
                resultados = resultados_text.get("1.0", tk.END).strip()
                if not resultados:
                    messagebox.showerror("Erro", "Digite os resultados do exame")
                    return
                
                # Obter dados
                id_agendamento = agendamento_ids[agendamento_combo.current()]
                recomendacoes = recomendacoes_text.get("1.0", tk.END).strip()
                recomendacoes = recomendacoes if recomendacoes else None
                
                # Salvar resultado
                if self.model.add_resultado(id_agendamento, resultados, recomendacoes):
                    messagebox.showinfo("Sucesso", "Resultado cadastrado com sucesso!")
                    dialog.destroy()
                    self.refresh_data("resultados")
                else:
                    messagebox.showerror("Erro", "Erro ao cadastrar resultado")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        
        def limpar():
            resultados_text.delete("1.0", tk.END)
            recomendacoes_text.delete("1.0", tk.END)
            agendamento_combo.set("")
        
        ttk_boot.Button(button_frame, text="Salvar", command=salvar, bootstyle="success").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Limpar", command=limpar, bootstyle="warning").pack(side="left", padx=5)
        ttk_boot.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="secondary").pack(side="left", padx=5)
    
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
