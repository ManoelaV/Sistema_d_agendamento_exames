-- REMOÇÃO E CRIAÇÃO DO BANCO
DROP DATABASE IF EXISTS clinica_exames;
CREATE DATABASE clinica_exames;
USE clinica_exames;

-- CRIAÇÃO DAS TABELAS NA ORDEM CORRETA
CREATE TABLE Empresa (
    id_empresa INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    endereco TEXT NOT NULL
);

CREATE TABLE Unidade (
    id_unidade INT AUTO_INCREMENT PRIMARY KEY,
    endereco TEXT NOT NULL
);

CREATE TABLE Profissional (
    id_profissional INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    especialidade VARCHAR(100)
);

CREATE TABLE Exame (
    id_exame INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    requisitos TEXT,
    tempo_estimado INT NOT NULL,
    tipo VARCHAR(20) CHECK (tipo IN ('LABORATORIAL', 'IMAGEM', 'CLINICO')),
    tempo_coleta_analise INT,
    restricoes_alimentares TEXT,
    tecnologia_utilizada VARCHAR(100),
    preparos_especiais TEXT,
    tempo_medio_consulta INT,
    especialidade_medica VARCHAR(100),
    intervalo_limpeza INT NOT NULL DEFAULT 15
);

-- PACIENTE DEVE VIR DEPOIS DE EMPRESA
CREATE TABLE Paciente (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    id_empresa INT,  -- INT mesmo tipo que id_empresa na Empresa
    nome VARCHAR(255) NOT NULL,
    endereco TEXT NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_nasc DATE NOT NULL,
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa) ON DELETE SET NULL
);

-- TABELAS COM RELACIONAMENTOS
CREATE TABLE Disponibilidade (
    id_disponibilidade INT AUTO_INCREMENT PRIMARY KEY,
    id_exame INT NOT NULL,
    id_unidade INT NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (id_exame) REFERENCES Exame(id_exame) ON DELETE CASCADE,
    FOREIGN KEY (id_unidade) REFERENCES Unidade(id_unidade) ON DELETE CASCADE,
    UNIQUE (id_exame, id_unidade, data)
);

CREATE TABLE Agendamento (
    id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_exame INT NOT NULL,
    id_unidade INT NOT NULL,
    id_profissional INT,
    data_hora DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'AGENDADO' CHECK (status IN ('AGENDADO', 'REALIZADO', 'CANCELADO')),
    documentos_ok BOOLEAN DEFAULT false,
    requisitos_ok BOOLEAN DEFAULT false,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente) ON DELETE CASCADE,
    FOREIGN KEY (id_exame) REFERENCES Exame(id_exame) ON DELETE CASCADE,
    FOREIGN KEY (id_unidade) REFERENCES Unidade(id_unidade) ON DELETE CASCADE,
    FOREIGN KEY (id_profissional) REFERENCES Profissional(id_profissional) ON DELETE SET NULL
);

CREATE TABLE Resultado (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_agendamento INT NOT NULL UNIQUE,
    resultados TEXT NOT NULL,
    recomendacoes TEXT,
    FOREIGN KEY (id_agendamento) REFERENCES Agendamento(id_agendamento) ON DELETE CASCADE
);

CREATE TABLE Transferencia (
    id_transferencia INT AUTO_INCREMENT PRIMARY KEY,
    id_exame INT NOT NULL,
    id_unidade_origem INT NOT NULL,
    id_unidade_destino INT NOT NULL,
    data_transferencia DATE NOT NULL,
    motivo TEXT,
    FOREIGN KEY (id_exame) REFERENCES Exame(id_exame) ON DELETE CASCADE,
    FOREIGN KEY (id_unidade_origem) REFERENCES Unidade(id_unidade) ON DELETE CASCADE,
    FOREIGN KEY (id_unidade_destino) REFERENCES Unidade(id_unidade) ON DELETE CASCADE
);

-- INSERÇÕES DE DADOS
INSERT INTO Empresa (nome, cnpj, telefone, endereco) VALUES
('Empresa ABC', '12345678000190', '(53)9999-8888', 'Rua Industrial, 100 - Pelotas/RS'),
('Saúde Integrada', '98765432000121', '(51)7777-6666', 'Av. Comercial, 500 - Porto Alegre/RS');

INSERT INTO Paciente (id_empresa, nome, endereco, telefone, cpf, data_nasc) VALUES
(NULL, 'João Silva', 'Rua A, 123', '(53)1234-5678', '12345678901', '1990-05-15'),
(1, 'Maria Oliveira', 'Rua B, 456', '(53)8765-4321', '23456789012', '1985-08-22'),
(2, 'Carlos Pereira', 'Av. Central, 789', '(51)5555-4444', '34567890123', '2000-03-10'),
(NULL, 'Ana Souza', 'Rua das Flores, 321', '(53)2222-3333', '45678901234', '1975-11-28');

INSERT INTO Unidade (endereco) VALUES
('Av. Duque de Caxias, 250 - Pelotas/RS'),
('Rua Gonçalves Chaves, 789 - Pelotas/RS'),
('Av. Presidente Vargas, 1000 - Rio Grande/RS');

INSERT INTO Exame (nome, descricao, requisitos, tempo_estimado, tipo, tempo_coleta_analise, restricoes_alimentares) VALUES
('Hemograma', 'Análise sanguínea completa', 'Jejum de 8 horas', 30, 'LABORATORIAL', 15, 'Sem restrições adicionais'),
('Glicemia', 'Medição de açúcar no sangue', 'Jejum de 12 horas', 20, 'LABORATORIAL', 10, 'Evitar doces 24h antes');

INSERT INTO Exame (nome, descricao, requisitos, tempo_estimado, tipo, tecnologia_utilizada, preparos_especiais) VALUES
('Ultrassonografia', 'Exame de imagem abdominal', 'Bexiga cheia', 45, 'IMAGEM', 'Ultrassom HD', 'Ingerir 1L de água 1h antes'),
('Ressonância Magnética', 'Exame de imagem cerebral', 'Sem objetos metálicos', 60, 'IMAGEM', 'Ressonância 3T', 'Jejum de 4 horas');

INSERT INTO Exame (nome, descricao, requisitos, tempo_estimado, tipo, tempo_medio_consulta, especialidade_medica) VALUES
('Consulta Cardiológica', 'Avaliação cardíaca completa', 'Trazer exames anteriores', 40, 'CLINICO', 30, 'Cardiologia'),
('Check-up Anual', 'Avaliação clínica geral', 'Trazer histórico médico', 50, 'CLINICO', 40, 'Clínica Geral');

INSERT INTO Profissional (nome, especialidade) VALUES
('Dra. Ana Souza', 'Patologia Clínica'),
('Dr. Carlos Santos', 'Radiologia'),
('Dr. Pedro Mendes', 'Cardiologia'),
('Dra. Juliana Lima', 'Clínica Geral');

INSERT INTO Disponibilidade (id_exame, id_unidade, data) VALUES
(1, 1, '2024-07-25'),
(1, 1, '2024-07-26'),
(3, 2, '2024-07-26'),
(4, 3, '2024-07-27'),
(5, 1, '2024-07-28'),
(6, 2, '2024-07-29');

INSERT INTO Agendamento (id_paciente, id_exame, id_unidade, id_profissional, data_hora) VALUES
(1, 1, 1, 1, '2024-07-25 09:00:00'),
(2, 3, 2, 2, '2024-07-26 14:30:00'),
(3, 5, 1, 3, '2024-07-28 10:00:00'),
(4, 6, 2, 4, '2024-07-29 11:00:00');

INSERT INTO Resultado (id_agendamento, resultados, recomendacoes) VALUES
(1, 'Valores dentro da normalidade', 'Manter hábitos saudáveis');

INSERT INTO Transferencia (id_exame, id_unidade_origem, id_unidade_destino, data_transferencia, motivo) VALUES
(1, 3, 1, '2024-07-20', 'Aumento de demanda na região'),
(4, 2, 3, '2024-07-22', 'Manutenção de equipamento');

-- CONSULTAS (6 no total, todas com junções)
-- 1. Pacientes e seus exames agendados
SELECT 
    p.nome AS paciente,
    e.nome AS exame,
    a.data_hora AS agendamento,
    u.endereco AS unidade
FROM Agendamento a
JOIN Paciente p ON a.id_paciente = p.id_paciente
JOIN Exame e ON a.id_exame = e.id_exame
JOIN Unidade u ON a.id_unidade = u.id_unidade;

-- 2. Exames realizados com resultados
SELECT 
    p.nome AS paciente,
    e.nome AS exame,
    a.data_hora AS realizacao,
    r.resultados,
    r.recomendacoes
FROM Agendamento a
JOIN Resultado r ON a.id_agendamento = r.id_agendamento
JOIN Paciente p ON a.id_paciente = p.id_paciente
JOIN Exame e ON a.id_exame = e.id_exame
WHERE a.status = 'REALIZADO';

-- 3. Disponibilidade de exames por unidade
SELECT 
    e.nome AS exame,
    u.endereco AS unidade,
    d.data AS data_disponivel
FROM Disponibilidade d
JOIN Exame e ON d.id_exame = e.id_exame
JOIN Unidade u ON d.id_unidade = u.id_unidade
WHERE d.data BETWEEN '2024-07-25' AND '2024-07-30';

-- 4. Transferências de exames entre unidades
SELECT 
    e.nome AS exame,
    uo.endereco AS origem,
    ud.endereco AS destino,
    t.data_transferencia,
    t.motivo
FROM Transferencia t
JOIN Exame e ON t.id_exame = e.id_exame
JOIN Unidade uo ON t.id_unidade_origem = uo.id_unidade
JOIN Unidade ud ON t.id_unidade_destino = ud.id_unidade;

-- 5. Pacientes vinculados a empresas
SELECT 
    emp.nome AS empresa,
    p.nome AS paciente,
    p.cpf,
    p.data_nasc
FROM Paciente p
JOIN Empresa emp ON p.id_empresa = emp.id_empresa;

-- 6. Profissionais e seus exames agendados
SELECT 
    pr.nome AS profissional,
    e.nome AS exame,
    COUNT(a.id_agendamento) AS total_agendamentos
FROM Agendamento a
JOIN Profissional pr ON a.id_profissional = pr.id_profissional
JOIN Exame e ON a.id_exame = e.id_exame
GROUP BY pr.nome, e.nome;

-- PROCESSAMENTO ATIVO: GATILHO PARA VERIFICAÇÃO DE REQUISITO
DELIMITER $$

CREATE TRIGGER tg_atualiza_status_exame
BEFORE UPDATE ON Agendamento
FOR EACH ROW
BEGIN
    -- Verificar se está tentando atualizar para REALIZADO
    IF NEW.status = 'REALIZADO' THEN
        -- Verificar se os requisitos foram atendidos
        IF NEW.documentos_ok = false OR NEW.requisitos_ok = false THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Exame não pode ser marcado como realizado: requisitos ou documentos pendentes';
        END IF;
    END IF;
END$$

DELIMITER ;

-- VIEW PARA EXAMES PRÓXIMOS
CREATE VIEW vw_exames_proximos AS
SELECT 
    p.nome AS paciente,
    e.nome AS exame,
    a.data_hora,
    u.endereco AS unidade,
    CASE 
        WHEN a.data_hora BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 2 DAY) THEN 'URGENTE'
        WHEN a.data_hora BETWEEN DATE_ADD(NOW(), INTERVAL 3 DAY) AND DATE_ADD(NOW(), INTERVAL 7 DAY) THEN 'PRÓXIMO'
        ELSE 'FUTURO'
    END AS prioridade
FROM Agendamento a
JOIN Paciente p ON a.id_paciente = p.id_paciente
JOIN Exame e ON a.id_exame = e.id_exame
JOIN Unidade u ON a.id_unidade = u.id_unidade
WHERE a.status = 'AGENDADO'
AND a.data_hora BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 7 DAY);