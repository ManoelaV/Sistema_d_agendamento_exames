-- Script de Criação das Tabelas

-- Criação do banco de dados
USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'SistemaAgendamentoExames')
BEGIN
    CREATE DATABASE SistemaAgendamentoExames;
END
GO

USE SistemaAgendamentoExames;
GO

-- Tabela Empresa
CREATE TABLE Empresa (
    CNPJ VARCHAR(18) PRIMARY KEY,
    Nome_Empresa VARCHAR(100) NOT NULL,
    Endereco_Empresa VARCHAR(200) NOT NULL,
    Telefone_Empresa VARCHAR(15) NOT NULL,
    CONSTRAINT CK_CNPJ_Format CHECK (CNPJ LIKE '[0-9][0-9].[0-9][0-9][0-9].[0-9][0-9][0-9]/[0-9][0-9][0-9][0-9]-[0-9][0-9]')
);

-- Tabela Unidade
CREATE TABLE Unidade (
    Cd_Unidade INT IDENTITY(1,1) PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    UF CHAR(2) NOT NULL,
    Cidade VARCHAR(50) NOT NULL,
    Endereco VARCHAR(200) NOT NULL,
    CONSTRAINT CK_UF_Format CHECK (UF LIKE '[A-Z][A-Z]')
);

-- Tabela Profissional de Saúde
CREATE TABLE ProfissionalDeSaude (
    Cd_Profissional INT IDENTITY(1,1) PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Especialidade VARCHAR(50) NOT NULL,
    CRM VARCHAR(20) NOT NULL UNIQUE,
    Telefone VARCHAR(15),
    Email VARCHAR(100)
);

-- Tabela Paciente
CREATE TABLE Paciente (
    Cd_Paciente INT IDENTITY(1,1) PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Data_Nascimento DATE NOT NULL,
    CPF VARCHAR(14) NOT NULL UNIQUE,
    Telefone VARCHAR(15) NOT NULL,
    Endereco VARCHAR(200) NOT NULL,
    Email VARCHAR(100),
    CNPJ VARCHAR(18) NULL,
    Data_Cadastro DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Paciente_Empresa FOREIGN KEY (CNPJ) REFERENCES Empresa(CNPJ),
    CONSTRAINT CK_CPF_Format CHECK (CPF LIKE '[0-9][0-9][0-9].[0-9][0-9][0-9].[0-9][0-9][0-9]-[0-9][0-9]'),
    CONSTRAINT CK_Data_Nascimento CHECK (Data_Nascimento <= GETDATE())
);

-- Tabela Histórico
CREATE TABLE Historico (
    Cd_Historico INT IDENTITY(1,1) PRIMARY KEY,
    Data_Registro DATETIME DEFAULT GETDATE(),
    Recomendacoes TEXT,
    Cd_Paciente INT NOT NULL,
    CONSTRAINT FK_Historico_Paciente FOREIGN KEY (Cd_Paciente) REFERENCES Paciente(Cd_Paciente)
);

-- Tabela Resultado
CREATE TABLE Resultado (
    Cd_Resultado INT IDENTITY(1,1) PRIMARY KEY,
    Resultado TEXT NOT NULL,
    Recomendacoes TEXT,
    Data_Resultado DATETIME DEFAULT GETDATE(),
    Cd_Historico INT NOT NULL,
    CONSTRAINT FK_Resultado_Historico FOREIGN KEY (Cd_Historico) REFERENCES Historico(Cd_Historico)
);

-- Tabela Consulta
CREATE TABLE Consulta (
    Cd_Consulta INT IDENTITY(1,1) PRIMARY KEY,
    Hora TIME NOT NULL,
    Data DATE NOT NULL,
    Tipo_Consulta VARCHAR(50) NOT NULL,
    Status VARCHAR(20) DEFAULT 'Agendada',
    Cd_Historico INT NOT NULL,
    Cd_Profissional INT NOT NULL,
    CONSTRAINT FK_Consulta_Historico FOREIGN KEY (Cd_Historico) REFERENCES Historico(Cd_Historico),
    CONSTRAINT FK_Consulta_Profissional FOREIGN KEY (Cd_Profissional) REFERENCES ProfissionalDeSaude(Cd_Profissional),
    CONSTRAINT CK_Status_Consulta CHECK (Status IN ('Agendada', 'Realizada', 'Cancelada', 'Reagendada'))
);

-- Tabela Disponibilidade
CREATE TABLE Disponibilidade (
    Cd_Disponibilidade INT IDENTITY(1,1) PRIMARY KEY,
    Status VARCHAR(20) DEFAULT 'Disponível',
    Data DATE NOT NULL,
    Hora TIME NOT NULL,
    Cd_Unidade INT NOT NULL,
    Cd_Profissional INT NULL,
    CONSTRAINT FK_Disponibilidade_Unidade FOREIGN KEY (Cd_Unidade) REFERENCES Unidade(Cd_Unidade),
    CONSTRAINT FK_Disponibilidade_Profissional FOREIGN KEY (Cd_Profissional) REFERENCES ProfissionalDeSaude(Cd_Profissional),
    CONSTRAINT CK_Status_Disponibilidade CHECK (Status IN ('Disponível', 'Ocupado', 'Manutenção')),
    CONSTRAINT UQ_Disponibilidade UNIQUE (Data, Hora, Cd_Unidade, Cd_Profissional)
);

-- Tabela Exame
CREATE TABLE Exame (
    Cd_Exame INT IDENTITY(1,1) PRIMARY KEY,
    Nome_Exame VARCHAR(100) NOT NULL,
    Tipo_Exame VARCHAR(20) NOT NULL,
    Requisitos TEXT,
    Descricao TEXT,
    Tempo_Estimado INT, -- em minutos
    Valor DECIMAL(10,2),
    Cd_Disponibilidade INT NOT NULL,
    CONSTRAINT FK_Exame_Disponibilidade FOREIGN KEY (Cd_Disponibilidade) REFERENCES Disponibilidade(Cd_Disponibilidade),
    CONSTRAINT CK_Tipo_Exame CHECK (Tipo_Exame IN ('Laboratorial', 'Imagem', 'Clínico')),
    CONSTRAINT CK_Tempo_Estimado CHECK (Tempo_Estimado > 0)
);

-- Tabela Agendamento
CREATE TABLE Agendamento (
    Cd_Agendamento INT IDENTITY(1,1) PRIMARY KEY,
    Hora TIME NOT NULL,
    Data DATE NOT NULL,
    Motivo_Agendamento VARCHAR(200),
    Status VARCHAR(20) DEFAULT 'Agendado',
    Data_Agendamento DATETIME DEFAULT GETDATE(),
    Cd_Paciente INT NOT NULL,
    Cd_Unidade INT NOT NULL,
    Cd_Exame INT NOT NULL,
    Cd_Profissional INT NULL,
    CONSTRAINT FK_Agendamento_Paciente FOREIGN KEY (Cd_Paciente) REFERENCES Paciente(Cd_Paciente),
    CONSTRAINT FK_Agendamento_Unidade FOREIGN KEY (Cd_Unidade) REFERENCES Unidade(Cd_Unidade),
    CONSTRAINT FK_Agendamento_Exame FOREIGN KEY (Cd_Exame) REFERENCES Exame(Cd_Exame),
    CONSTRAINT FK_Agendamento_Profissional FOREIGN KEY (Cd_Profissional) REFERENCES ProfissionalDeSaude(Cd_Profissional),
    CONSTRAINT CK_Status_Agendamento CHECK (Status IN ('Agendado', 'Confirmado', 'Realizado', 'Cancelado', 'Reagendado')),
    CONSTRAINT CK_Data_Futura CHECK (Data >= CAST(GETDATE() AS DATE))
);

-- Tabela Notificação
CREATE TABLE Notificacao (
    Cd_Notificacao INT IDENTITY(1,1) PRIMARY KEY,
    Status_Envio VARCHAR(20) DEFAULT 'Pendente',
    Data_Envio DATETIME,
    Mensagem TEXT NOT NULL,
    Tipo_Notificacao VARCHAR(20) DEFAULT 'Email',
    Cd_Agendamento INT NOT NULL,
    CONSTRAINT FK_Notificacao_Agendamento FOREIGN KEY (Cd_Agendamento) REFERENCES Agendamento(Cd_Agendamento),
    CONSTRAINT CK_Status_Envio CHECK (Status_Envio IN ('Pendente', 'Enviado', 'Falha')),
    CONSTRAINT CK_Tipo_Notificacao CHECK (Tipo_Notificacao IN ('Email', 'SMS', 'WhatsApp'))
);

-- Índices para melhorar a performance
CREATE INDEX IX_Paciente_CPF ON Paciente(CPF);
CREATE INDEX IX_Paciente_CNPJ ON Paciente(CNPJ);
CREATE INDEX IX_Agendamento_Data ON Agendamento(Data);
CREATE INDEX IX_Agendamento_Status ON Agendamento(Status);
CREATE INDEX IX_Disponibilidade_Data_Hora ON Disponibilidade(Data, Hora);
CREATE INDEX IX_Consulta_Data ON Consulta(Data);

PRINT 'Tabelas criadas com sucesso!';
