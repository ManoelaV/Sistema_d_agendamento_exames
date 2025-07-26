from database import DatabaseConnection
from datetime import datetime, date

class ClinicaModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    # PACIENTE CRUD
    def get_pacientes(self):
        """Retorna todos os pacientes"""
        query = """
        SELECT p.*, e.nome as empresa_nome 
        FROM Paciente p 
        LEFT JOIN Empresa e ON p.id_empresa = e.id_empresa
        ORDER BY p.nome
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_paciente_by_id(self, id_paciente):
        """Retorna um paciente específico"""
        query = "SELECT * FROM Paciente WHERE id_paciente = %s"
        result = self.db.execute_query(query, (id_paciente,), fetch=True)
        return result[0] if result else None
    
    def add_paciente(self, nome, endereco, telefone, cpf, data_nasc, id_empresa=None):
        """Adiciona um novo paciente"""
        query = """
        INSERT INTO Paciente (nome, endereco, telefone, cpf, data_nasc, id_empresa)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (nome, endereco, telefone, cpf, data_nasc, id_empresa))
    
    def update_paciente(self, id_paciente, nome, endereco, telefone, cpf, data_nasc, id_empresa=None):
        """Atualiza um paciente"""
        query = """
        UPDATE Paciente 
        SET nome = %s, endereco = %s, telefone = %s, cpf = %s, data_nasc = %s, id_empresa = %s
        WHERE id_paciente = %s
        """
        return self.db.execute_query(query, (nome, endereco, telefone, cpf, data_nasc, id_empresa, id_paciente))
    
    def delete_paciente(self, id_paciente):
        """Remove um paciente"""
        query = "DELETE FROM Paciente WHERE id_paciente = %s"
        return self.db.execute_query(query, (id_paciente,))
    
    # EXAME CRUD
    def get_exames(self):
        """Retorna todos os exames"""
        query = "SELECT * FROM Exame ORDER BY nome"
        return self.db.execute_query(query, fetch=True)
    
    def get_exame_by_id(self, id_exame):
        """Retorna um exame específico"""
        query = "SELECT * FROM Exame WHERE id_exame = %s"
        result = self.db.execute_query(query, (id_exame,), fetch=True)
        return result[0] if result else None
    
    def add_exame(self, nome, descricao, requisitos, tempo_estimado, tipo, **kwargs):
        """Adiciona um novo exame"""
        # Campos base
        fields = ['nome', 'descricao', 'requisitos', 'tempo_estimado', 'tipo']
        values = [nome, descricao, requisitos, tempo_estimado, tipo]
        placeholders = ['%s'] * 5
        
        # Campos opcionais
        optional_fields = ['tempo_coleta_analise', 'restricoes_alimentares', 'tecnologia_utilizada', 
                          'preparos_especiais', 'tempo_medio_consulta', 'especialidade_medica', 'intervalo_limpeza']
        
        for field in optional_fields:
            if field in kwargs and kwargs[field] is not None:
                fields.append(field)
                values.append(kwargs[field])
                placeholders.append('%s')
        
        query = f"INSERT INTO Exame ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
        return self.db.execute_query(query, tuple(values))
    
    def update_exame(self, id_exame, nome, descricao, requisitos, tempo_estimado, tipo, **kwargs):
        """Atualiza um exame"""
        # Campos base
        set_clauses = ['nome = %s', 'descricao = %s', 'requisitos = %s', 'tempo_estimado = %s', 'tipo = %s']
        values = [nome, descricao, requisitos, tempo_estimado, tipo]
        
        # Campos opcionais
        optional_fields = ['tempo_coleta_analise', 'restricoes_alimentares', 'tecnologia_utilizada', 
                          'preparos_especiais', 'tempo_medio_consulta', 'especialidade_medica', 'intervalo_limpeza']
        
        for field in optional_fields:
            if field in kwargs:
                set_clauses.append(f'{field} = %s')
                values.append(kwargs[field])
        
        values.append(id_exame)
        query = f"UPDATE Exame SET {', '.join(set_clauses)} WHERE id_exame = %s"
        return self.db.execute_query(query, tuple(values))
    
    def delete_exame(self, id_exame):
        """Remove um exame"""
        query = "DELETE FROM Exame WHERE id_exame = %s"
        return self.db.execute_query(query, (id_exame,))
    
    # AGENDAMENTO CRUD
    def get_agendamentos(self):
        """Retorna todos os agendamentos com informações completas"""
        query = """
        SELECT a.*, p.nome as paciente_nome, e.nome as exame_nome, 
               u.endereco as unidade_endereco, pr.nome as profissional_nome
        FROM Agendamento a
        JOIN Paciente p ON a.id_paciente = p.id_paciente
        JOIN Exame e ON a.id_exame = e.id_exame
        JOIN Unidade u ON a.id_unidade = u.id_unidade
        LEFT JOIN Profissional pr ON a.id_profissional = pr.id_profissional
        ORDER BY a.data_hora
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_agendamentos_by_data(self, data_inicio, data_fim):
        """Retorna agendamentos em um período"""
        query = """
        SELECT a.*, p.nome as paciente_nome, e.nome as exame_nome, 
               u.endereco as unidade_endereco, pr.nome as profissional_nome
        FROM Agendamento a
        JOIN Paciente p ON a.id_paciente = p.id_paciente
        JOIN Exame e ON a.id_exame = e.id_exame
        JOIN Unidade u ON a.id_unidade = u.id_unidade
        LEFT JOIN Profissional pr ON a.id_profissional = pr.id_profissional
        WHERE DATE(a.data_hora) BETWEEN %s AND %s
        ORDER BY a.data_hora
        """
        return self.db.execute_query(query, (data_inicio, data_fim), fetch=True)
    
    def add_agendamento(self, id_paciente, id_exame, id_unidade, data_hora, id_profissional=None):
        """Adiciona um novo agendamento"""
        query = """
        INSERT INTO Agendamento (id_paciente, id_exame, id_unidade, id_profissional, data_hora)
        VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (id_paciente, id_exame, id_unidade, id_profissional, data_hora))
    
    def update_agendamento_status(self, id_agendamento, status, documentos_ok=None, requisitos_ok=None):
        """Atualiza status do agendamento"""
        query = "UPDATE Agendamento SET status = %s"
        params = [status]
        
        if documentos_ok is not None:
            query += ", documentos_ok = %s"
            params.append(documentos_ok)
        
        if requisitos_ok is not None:
            query += ", requisitos_ok = %s"
            params.append(requisitos_ok)
        
        query += " WHERE id_agendamento = %s"
        params.append(id_agendamento)
        
        return self.db.execute_query(query, tuple(params))
    
    def delete_agendamento(self, id_agendamento):
        """Remove um agendamento"""
        query = "DELETE FROM Agendamento WHERE id_agendamento = %s"
        return self.db.execute_query(query, (id_agendamento,))
    
    # EMPRESA CRUD
    def get_empresas(self):
        """Retorna todas as empresas"""
        query = "SELECT * FROM Empresa ORDER BY nome"
        return self.db.execute_query(query, fetch=True)
    
    def add_empresa(self, nome, cnpj, telefone, endereco):
        """Adiciona uma nova empresa"""
        query = "INSERT INTO Empresa (nome, cnpj, telefone, endereco) VALUES (%s, %s, %s, %s)"
        return self.db.execute_query(query, (nome, cnpj, telefone, endereco))
    
    # UNIDADE CRUD
    def get_unidades(self):
        """Retorna todas as unidades"""
        query = "SELECT * FROM Unidade ORDER BY id_unidade"
        return self.db.execute_query(query, fetch=True)
    
    def add_unidade(self, endereco):
        """Adiciona uma nova unidade"""
        query = "INSERT INTO Unidade (endereco) VALUES (%s)"
        return self.db.execute_query(query, (endereco,))
    
    # PROFISSIONAL CRUD
    def get_profissionais(self):
        """Retorna todos os profissionais"""
        query = "SELECT * FROM Profissional ORDER BY nome"
        return self.db.execute_query(query, fetch=True)
    
    def add_profissional(self, nome, especialidade):
        """Adiciona um novo profissional"""
        query = "INSERT INTO Profissional (nome, especialidade) VALUES (%s, %s)"
        return self.db.execute_query(query, (nome, especialidade))
    
    # RESULTADO CRUD
    def get_resultados(self):
        """Retorna todos os resultados com informações do agendamento"""
        query = """
        SELECT r.*, a.data_hora, p.nome as paciente_nome, e.nome as exame_nome
        FROM Resultado r
        JOIN Agendamento a ON r.id_agendamento = a.id_agendamento
        JOIN Paciente p ON a.id_paciente = p.id_paciente
        JOIN Exame e ON a.id_exame = e.id_exame
        ORDER BY a.data_hora DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def add_resultado(self, id_agendamento, resultados, recomendacoes=None):
        """Adiciona um resultado"""
        query = "INSERT INTO Resultado (id_agendamento, resultados, recomendacoes) VALUES (%s, %s, %s)"
        return self.db.execute_query(query, (id_agendamento, resultados, recomendacoes))
    
    # DISPONIBILIDADE
    def get_disponibilidades(self):
        """Retorna disponibilidades com informações dos exames e unidades"""
        query = """
        SELECT d.*, e.nome as exame_nome, u.endereco as unidade_endereco
        FROM Disponibilidade d
        JOIN Exame e ON d.id_exame = e.id_exame
        JOIN Unidade u ON d.id_unidade = u.id_unidade
        ORDER BY d.data
        """
        return self.db.execute_query(query, fetch=True)
    
    def add_disponibilidade(self, id_exame, id_unidade, data):
        """Adiciona disponibilidade"""
        query = "INSERT INTO Disponibilidade (id_exame, id_unidade, data) VALUES (%s, %s, %s)"
        return self.db.execute_query(query, (id_exame, id_unidade, data))
    
    # RELATÓRIOS
    def get_exames_proximos(self):
        """Retorna exames próximos usando a view"""
        query = "SELECT * FROM vw_exames_proximos ORDER BY data_hora"
        return self.db.execute_query(query, fetch=True)
    
    def get_agendamentos_por_profissional(self):
        """Retorna estatísticas de agendamentos por profissional"""
        query = """
        SELECT pr.nome AS profissional, e.nome AS exame, COUNT(a.id_agendamento) AS total
        FROM Agendamento a
        JOIN Profissional pr ON a.id_profissional = pr.id_profissional
        JOIN Exame e ON a.id_exame = e.id_exame
        GROUP BY pr.nome, e.nome
        ORDER BY total DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_pacientes_por_empresa(self):
        """Retorna pacientes vinculados a empresas"""
        query = """
        SELECT emp.nome AS empresa, p.nome AS paciente, p.cpf, p.data_nasc
        FROM Paciente p
        JOIN Empresa emp ON p.id_empresa = emp.id_empresa
        ORDER BY emp.nome, p.nome
        """
        return self.db.execute_query(query, fetch=True)
    
    def test_connection(self):
        """Testa a conexão com o banco"""
        return self.db.test_connection()
