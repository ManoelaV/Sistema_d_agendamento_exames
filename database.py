import mysql.connector
from mysql.connector import Error
import json
import os

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.config_file = 'db_config.json'
        self.load_config()
    
    def load_config(self):
        """Carrega a configuração do banco de dados do arquivo JSON"""
        default_config = {
            "host": "localhost",
            "database": "clinica_exames",
            "user": "root",
            "password": ""
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
                self.save_config()
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Salva a configuração no arquivo JSON"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return False
        return False
    
    def disconnect(self):
        """Fecha a conexão com o banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Executa uma query no banco de dados"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
                
        except Error as e:
            print(f"Erro na query: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def execute_many(self, query, data):
        """Executa múltiplas queries com dados diferentes"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, data)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erro na execução múltipla: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def test_connection(self):
        """Testa a conexão com o banco"""
        try:
            if self.connect():
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                self.disconnect()
                return True
        except:
            pass
        return False
    
    def update_config(self, host, database, user, password):
        """Atualiza a configuração do banco"""
        self.config = {
            "host": host,
            "database": database,
            "user": user,
            "password": password
        }
        self.save_config()
