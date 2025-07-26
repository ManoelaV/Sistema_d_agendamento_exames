# Sistema de Agendamento de Exames - Interface Desktop

Este projeto implementa uma interface desktop básica para comunicação com banco de dados MySQL, desenvolvida especificamente para o sistema de agendamento de exames clínicos.

##  Funcionalidades

### Interface Principal
- **Interface gráfica moderna** usando ttkbootstrap (com fallback para tkinter padrão)
- **Configuração dinâmica** do banco de dados através da interface
- **Navegação por abas** para diferentes módulos do sistema
- **Tema moderno** e responsivo

### Módulos Implementados

#### 👥 Gestão de Pacientes
- ✅ Cadastro de novos pacientes
- ✅ Edição de dados existentes
- ✅ Exclusão de pacientes
- ✅ Visualização em lista
- ✅ Vinculação com empresas

#### 🔬 Gestão de Exames
- ✅ Cadastro de diferentes tipos de exames (LABORATORIAL, IMAGEM, CLÍNICO)
- ✅ Campos específicos por tipo de exame
- ✅ Configuração de tempo estimado e requisitos
- ✅ Edição e exclusão de exames

#### 📅 Gestão de Agendamentos
- ✅ Criação de novos agendamentos
- ✅ Seleção de paciente, exame, unidade e profissional
- ✅ Controle de status (AGENDADO, REALIZADO, CANCELADO)
- ✅ Validação de documentos e requisitos
- ✅ Cancelamento de agendamentos

#### 📋 Gestão de Resultados
- ✅ Cadastro de resultados para exames realizados
- ✅ Adição de recomendações médicas
- ✅ Vinculação automática com agendamentos

#### 📊 Relatórios
- ✅ **Exames Próximos**: Lista exames com prioridade (URGENTE, PRÓXIMO, FUTURO)
- ✅ **Por Profissional**: Estatísticas de agendamentos por profissional
- ✅ **Por Empresa**: Pacientes vinculados a empresas

## 🗄️ Estrutura do Banco

O sistema trabalha com as seguintes tabelas:
- `Empresa` - Dados das empresas parceiras
- `Paciente` - Informações dos pacientes
- `Exame` - Catálogo de exames disponíveis
- `Unidade` - Unidades de atendimento
- `Profissional` - Profissionais de saúde
- `Agendamento` - Agendamentos realizados
- `Resultado` - Resultados dos exames
- `Disponibilidade` - Disponibilidade de exames por unidade
- `Transferencia` - Histórico de transferências

## 🚀 Como Executar

### Pré-requisitos

1. **Python 3.7+** instalado
2. **MySQL** rodando com o banco `clinica_exames` criado
3. **Dependências Python**:

```bash
pip install -r requirements.txt
```

### Dependências

```
mysql-connector-python==8.2.0
ttkbootstrap==1.10.1
```

### Preparação do Banco

1. Execute o arquivo `trabalhoPBD.sql` no MySQL para criar a estrutura e dados de teste:

```sql
mysql -u root -p < trabalhoPBD.sql
```

### Execução

```bash
python main.py
```

## 🔧 Configuração

### Primeira Execução

1. Execute `python main.py`
2. Se a conexão falhar, será aberto um diálogo de configuração
3. Configure:
   - **Host**: localhost (ou IP do servidor MySQL)
   - **Database**: clinica_exames
   - **Usuário**: root (ou seu usuário MySQL)
   - **Senha**: sua senha MySQL

### Arquivo de Configuração

As configurações são salvas automaticamente em `db_config.json`:

```json
{
    "host": "localhost",
    "database": "clinica_exames",
    "user": "root",
    "password": "sua_senha"
}
```

## 📁 Estrutura do Projeto

```
Sistema_d_agendamento_exames/
├── main.py              # Arquivo principal de execução
├── database.py          # Classe de conexão com MySQL
├── models.py           # Modelos de dados e operações CRUD
├── gui_main.py         # Interface principal (ttkbootstrap)
├── gui_dialogs.py      # Diálogos e janelas secundárias
├── requirements.txt    # Dependências Python
├── db_config.json     # Configurações do banco (auto-gerado)
├── trabalhoPBD.sql    # Script de criação do banco
└── README.md          # Este arquivo
```

## 🎨 Interface

### Telas Principais

1. **Aba Pacientes**
   - Lista todos os pacientes cadastrados
   - Botões: Novo, Editar, Excluir, Atualizar

2. **Aba Exames**
   - Catálogo de exames disponíveis
   - Diferentes tipos com campos específicos

3. **Aba Agendamentos**
   - Visualização de todos os agendamentos
   - Controle de status e validações

4. **Aba Resultados**
   - Resultados de exames realizados
   - Recomendações médicas

5. **Aba Relatórios**
   - Relatórios gerenciais em tempo real

### Características da Interface

- **Design Responsivo**: Adapta-se ao tamanho da janela
- **Validação de Dados**: Campos obrigatórios e formatos validados
- **Mensagens Claras**: Feedback visual para todas as operações
- **Navegação Intuitiva**: Interface organizada por contexto
- **Fallback Robusto**: Funciona mesmo sem ttkbootstrap

## 🔒 Validações e Regras de Negócio

### Validações Implementadas
- ✅ CPF único por paciente
- ✅ Formato de data válido (DD/MM/AAAA)
- ✅ Campos obrigatórios preenchidos
- ✅ Status só muda para REALIZADO com documentos e requisitos OK
- ✅ Resultados só para exames realizados

### Gatilhos do Banco
- **Verificação de Requisitos**: Impede alterar status para REALIZADO sem validações

### Views Implementadas
- **vw_exames_proximos**: Exames com classificação de prioridade temporal

## 🐛 Troubleshooting

### Erro de Conexão
```
Erro ao conectar ao banco
```
**Solução**: Verifique se MySQL está rodando e configure corretamente via interface

### Erro de Importação ttkbootstrap
```
Import "ttkbootstrap" could not be resolved
```
**Solução**: Execute `pip install ttkbootstrap` ou use a versão simplificada

### Erro de Dependência MySQL
```
No module named 'mysql.connector'
```
**Solução**: Execute `pip install mysql-connector-python`

## 🔄 Versões

### v1.0 - Versão Atual
- ✅ Interface completa com ttkbootstrap
- ✅ Fallback para tkinter padrão
- ✅ Todas as operações CRUD
- ✅ Relatórios básicos
- ✅ Configuração via interface

### Próximas Versões (Propostas)
- 🔄 Backup/Restore do banco
- 🔄 Exportação de relatórios (PDF/Excel)
- 🔄 Calendário visual para agendamentos
- 🔄 Notificações de exames próximos
- 🔄 Dashboard com gráficos

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências estão instaladas
2. Confirme que o MySQL está rodando
3. Execute o script SQL para criar a estrutura
4. Verifique as configurações de conexão

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração.

---

**Desenvolvido com ❤️ para facilitar a gestão de exames clínicos**
