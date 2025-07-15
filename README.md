# Sistema de Agendamento de Exames Médicos

Este projeto implementa um sistema completo de banco de dados para gerenciamento de agendamentos de exames médicos, atendendo tanto pacientes individuais quanto empresariais.

## 📋 Estrutura do Projeto

### Scripts SQL Inclusos

1. **01_criar_tabelas.sql** - Scripts de definição do banco de dados
2. **02_inserir_dados.sql** - Scripts de inserção de dados de teste
3. **03_consultas.sql** - Consultas SQL (mínimo 6, sendo 4 com junção)
4. **04_funcoes_procedimentos_gatilhos.sql** - Processamento de BD ativo
5. **05_testes.sql** - Scripts de teste e validação

## 🏗️ Arquitetura do Banco de Dados

### Tabelas Principais

- **Empresa** - Dados das empresas cliente
- **Unidade** - Unidades de atendimento
- **Paciente** - Pacientes individuais e empresariais
- **ProfissionalDeSaude** - Médicos e profissionais
- **Agendamento** - Agendamentos de exames
- **Exame** - Catálogo de exames disponíveis
- **Disponibilidade** - Controle de horários disponíveis
- **Historico** - Histórico médico dos pacientes
- **Resultado** - Resultados dos exames
- **Consulta** - Consultas médicas
- **Notificacao** - Sistema de notificações
- **AuditoriaAgendamento** - Log de alterações

## 🔧 Funcionalidades Implementadas

### Funções Criadas
- `fn_CalcularIdade()` - Calcula idade precisa do paciente
- `fn_VerificarJejum()` - Verifica adequação do horário para jejum
- `fn_ReceitaPorPeriodo()` - Calcula receita por período

### Procedimentos Armazenados
- `sp_AgendarExame` - Agendamento com validações completas
- `sp_CancelarAgendamento` - Cancelamento controlado
- `sp_RelatorioAgendamentos` - Relatórios parametrizados

### Gatilhos (Triggers)
- `trg_ValidarPaciente` - Validação de dados de pacientes
- `trg_ControlarAgendamento` - Controle de conflitos
- `trg_CriarNotificacao` - Criação automática de notificações
- `trg_AuditoriaAgendamento` - Log de alterações

## 🛡️ Regras de Integridade

### Validações Implementadas
1. **Idade de Pacientes** - Entre 0 e 120 anos
2. **Conflitos de Agendamento** - Impede dupla marcação
3. **Limite Diário** - Máximo 3 agendamentos por paciente/dia
4. **Validação de CNPJ** - CNPJ deve existir na tabela Empresa
5. **Datas Futuras** - Agendamentos só para datas futuras
6. **Formatos** - CPF, CNPJ e UF em formatos válidos

### Constraints Criadas
- Chaves primárias e estrangeiras
- Checks de formato (CPF, CNPJ, UF)
- Checks de valores válidos (Status, Tipos)
- Unique constraints para evitar duplicatas

## 📊 Consultas Implementadas

### Consultas com Junção (4)
1. **Agendamentos Completos** - Paciente + Unidade + Dados
2. **Exames por Tipo** - Exame + Disponibilidade + Profissional + Unidade
3. **Histórico Empresarial** - Paciente + Empresa + Histórico + Resultado
4. **Agendamentos + Notificações** - Agendamento + Paciente + Exame + Notificação

### Consultas Adicionais (6+)
5. **Distribuição Etária** - Pacientes por faixa etária
6. **Estatísticas de Exames** - Análise por tipo de exame
7. **Disponibilidade por Unidade** - Relatório de disponibilidade
8. **Top Profissionais** - Ranking por agendamentos
9. **Empresas por Volume** - Ranking empresarial
10. **Eficácia de Notificações** - Taxa de sucesso por tipo

## 🚀 Como Executar

### Pré-requisitos
- SQL Server 2016 ou superior
- Permissões para criar banco de dados

### Ordem de Execução
```sql
-- 1. Criar estrutura
sqlcmd -S servidor -i 01_criar_tabelas.sql

-- 2. Inserir dados de teste
sqlcmd -S servidor -i 02_inserir_dados.sql

-- 3. Executar consultas
sqlcmd -S servidor -i 03_consultas.sql

-- 4. Criar funções e gatilhos
sqlcmd -S servidor -i 04_funcoes_procedimentos_gatilhos.sql

-- 5. Executar testes
sqlcmd -S servidor -i 05_testes.sql
```

## 📈 Exemplos de Uso

### Agendar um Exame
```sql
EXEC sp_AgendarExame 
    @CdPaciente = 1,
    @CdUnidade = 1,
    @CdExame = 1,
    @Data = '2025-07-20',
    @Hora = '08:00',
    @MotivoAgendamento = 'Check-up anual',
    @CdProfissional = 1;
```

### Cancelar Agendamento
```sql
EXEC sp_CancelarAgendamento 
    @CdAgendamento = 1,
    @Motivo = 'Paciente solicitou cancelamento';
```

### Consultar Idade de Paciente
```sql
SELECT Nome, dbo.fn_CalcularIdade(Data_Nascimento) AS Idade
FROM Paciente;
```

### Relatório de Agendamentos
```sql
EXEC sp_RelatorioAgendamentos 
    @DataInicio = '2025-07-01',
    @DataFim = '2025-07-31',
    @Status = 'Confirmado';
```

## 🔍 Características Técnicas

### Índices Criados
- CPF de pacientes
- CNPJ empresarial
- Datas de agendamento
- Status de agendamentos
- Data/hora de disponibilidade

### Tipos de Dados
- **VARCHAR** para textos variáveis
- **CHAR** para códigos fixos (UF)
- **DATE/TIME/DATETIME** para temporais
- **DECIMAL** para valores monetários
- **TEXT** para campos longos
- **INT IDENTITY** para chaves primárias

### Relacionamentos
- **1:N** - Empresa → Pacientes
- **1:N** - Unidade → Agendamentos
- **1:N** - Paciente → Históricos
- **1:1** - Agendamento → Notificação
- **N:M** - Profissionais ↔ Disponibilidades

## 📋 Validações em Tempo Real

O sistema implementa validações através de gatilhos que são executados automaticamente:

1. **Inserção de Pacientes** - Valida idade e CNPJ
2. **Criação de Agendamentos** - Previne conflitos
3. **Alteração de Status** - Registra auditoria
4. **Novos Agendamentos** - Cria notificações automáticas

## 📧 Sistema de Notificações

- **Tipos**: Email, SMS, WhatsApp
- **Status**: Pendente, Enviado, Falha
- **Criação Automática** via gatilho
- **Mensagens Personalizadas** com dados do exame

## 📊 Relatórios Disponíveis

- Agendamentos por período
- Estatísticas de exames
- Ranking de profissionais
- Performance de unidades
- Eficácia de notificações
- Receita por período

## 🛠️ Manutenção

### Backup Recomendado
```sql
BACKUP DATABASE SistemaAgendamentoExames 
TO DISK = 'C:\Backup\SistemaAgendamento.bak'
```

### Limpeza de Dados Antigos
```sql
-- Remover agendamentos cancelados com mais de 1 ano
DELETE FROM Agendamento 
WHERE Status = 'Cancelado' 
AND Data < DATEADD(YEAR, -1, GETDATE());
```

## 👥 Usuários do Sistema

- **Funcionários Administrativos** - Gerenciam agendamentos
- **Profissionais de Saúde** - Acessam agendamentos e registram resultados
- **Pacientes** - Consultam agendamentos (através de interface)
