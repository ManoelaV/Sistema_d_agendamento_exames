# 🏥 Sistema de Agendamento de Exames

## 📋 O QUE É?

Sistema completo para gestão de exames clínicos com interface gráfica moderna.

## ⚡ INÍCIO RÁPIDO

```bash
# Executar o sistema
./run.sh

```

## ✅ FUNCIONALIDADES

### 👥 **Pacientes**
- Cadastro, edição, exclusão
- Vinculação com empresas

### 🔬 **Exames** 
- 3 tipos: LABORATORIAL, IMAGEM, CLÍNICO
- Campos específicos por tipo
- Interface dinâmica

### 📅 **Agendamentos**
- Criação completa
- Controle de status
- Validações automáticas

### 📋 **Resultados**
- Para exames realizados
- Editor de texto extenso
- Recomendações médicas

### 📊 **Relatórios**
- Exames próximos
- Por profissional
- Por empresa

## 🚀 INSTALAÇÃO

### 1. Dependências do Sistema
```bash
sudo apt install python3-tk python3-venv mysql-server
```

### 2. Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Banco de Dados
```bash
mysql -u root -p < trabalhoPBD.sql
```

### 4. Executar
```bash
python main.py
```

## 🔧 CONFIGURAÇÃO

Na primeira execução:
- Host: `localhost`
- Database: `clinica_exames`
- User: `root`
- Password: sua senha MySQL

## 📁 ARQUIVOS PRINCIPAIS

```
├── main.py                  # Executar sistema
├── run.sh                   # Script automático
├── exemplo_exames.py        # Testar exames
├── exemplo_agendamentos.py  # Testar agendamentos
├── trabalhoPBD.sql         # Criar banco
├── README.md               # Esta documentação
└── venv/                   # Ambiente virtual
```

## 🐛 PROBLEMAS COMUNS

### Erro: externally-managed-environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: No module named 'tkinter'
```bash
sudo apt install python3-tk
```

### Erro: No module named 'mysql.connector'
```bash
pip install mysql-connector-python
```

### Erro de conexão MySQL
```bash
sudo systemctl start mysql
```

## 💡 EXEMPLOS DE USO

### Cadastrar Exame
1. Executar `python main.py`
2. Aba "Exames" → "➕ Novo Exame"
3. Preencher campos
4. Selecionar tipo
5. Salvar

### Criar Agendamento
1. Aba "Agendamentos" → "➕ Novo Agendamento"
2. Selecionar paciente e exame
3. Definir data/hora
4. Salvar

### Adicionar Resultado
1. Aba "Resultados" → "➕ Novo Resultado"
2. Selecionar exame REALIZADO
3. Digitar resultados
4. Salvar

## 📞 SUPORTE

1. **Teste as funcionalidades:**
   ```bash
   ./venv/bin/python exemplo_exames.py
   ```

2. **Verifique conexão MySQL:**
   ```bash
   mysql -u root -p -e "SHOW DATABASES;"
   ```

3. **Logs de erro:**
   - Execute o sistema pelo terminal
   - Observe mensagens de erro

## 🎯 STATUS

**✅ IMPLEMENTADO:**
- Interface gráfica completa
- Todas as operações CRUD
- Validações automáticas
- Relatórios básicos
- Ambiente virtual configurado

**🔄 PRÓXIMAS VERSÕES:**
- Backup/Restore
- Exportação PDF
- Calendário visual
- Dashboard com gráficos

---

**🚀 Sistema 100% funcional e pronto para uso!**
