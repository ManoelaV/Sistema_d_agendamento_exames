-- Script de Inserção de Dados

USE SistemaAgendamentoExames;
GO

-- Inserir dados na tabela Empresa
INSERT INTO Empresa (CNPJ, Nome_Empresa, Endereco_Empresa, Telefone_Empresa) VALUES
('12.345.678/0001-90', 'TechCorp Ltda', 'Av. Paulista, 1000 - São Paulo/SP', '(11) 3333-1000'),
('98.765.432/0001-10', 'Indústria Brasil S.A.', 'Rua das Flores, 500 - Rio de Janeiro/RJ', '(21) 2222-2000'),
('11.222.333/0001-44', 'Comércio Geral Ltda', 'Rua do Comércio, 200 - Belo Horizonte/MG', '(31) 3333-3000'),
('55.666.777/0001-88', 'Serviços Médicos Ltda', 'Av. Central, 750 - Brasília/DF', '(61) 4444-4000'),
('33.444.555/0001-22', 'Construção Civil S.A.', 'Rua dos Operários, 300 - Porto Alegre/RS', '(51) 5555-5000');

-- Inserir dados na tabela Unidade
INSERT INTO Unidade (Nome, UF, Cidade, Endereco) VALUES
('Unidade Central São Paulo', 'SP', 'São Paulo', 'Rua Augusta, 1500 - Consolação'),
('Unidade Norte Rio de Janeiro', 'RJ', 'Rio de Janeiro', 'Av. Atlântica, 2000 - Copacabana'),
('Unidade Sul Belo Horizonte', 'MG', 'Belo Horizonte', 'Av. Afonso Pena, 3000 - Centro'),
('Unidade Oeste Brasília', 'DF', 'Brasília', 'SQN 108 - Asa Norte'),
('Unidade Leste Porto Alegre', 'RS', 'Porto Alegre', 'Av. Ipiranga, 1200 - Centro'),
('Unidade Campinas', 'SP', 'Campinas', 'Rua Barão de Jaguara, 800 - Centro'),
('Unidade Niterói', 'RJ', 'Niterói', 'Rua da Conceição, 600 - Centro');

-- Inserir dados na tabela ProfissionalDeSaude
INSERT INTO ProfissionalDeSaude (Nome, Especialidade, CRM, Telefone, Email) VALUES
('Dra. Eduarda Ness', 'Cardiologia', 'CRM-SP 123456', '(11) 9999-1001', 'eduarda.moura@clinica.com'),
('Dra. Maiara Santos', 'Dermatologia', 'CRM-RJ 234567', '(21) 9999-2002', 'maiara.santos@clinica.com'),
('Dra. Adriane Moura', 'Endocrinologia', 'CRM-MG 345678', '(31) 9999-3003', 'Adriane.moura@clinica.com'),
('Dr. João Guilherme', 'Ginecologia', 'CRM-RS 456789', '(61) 9999-4004', 'joao.Guilherme@clinica.com'),
('Dr. Manoel Fernando', 'Neurologia', 'CRM-DF 567890', '(51) 9999-5005', 'manoel.fernando@clinica.com'),
('Dra. Luciana Rodrigues', 'Radiologia', 'CRM-SP 678901', '(11) 9999-6006', 'luciana.rodrigues@clinica.com'),
('Dr. Renan Fonseca', 'Patologia Clínica', 'CRM-RJ 789012', '(21) 9999-7007', 'renan.fonseca@clinica.com'),
('Dra. Cintia Azevedo', 'Ultrassonografia', 'CRM-MG 890123', '(31) 9999-8008', 'cintia.azevedo@clinica.com');

-- Inserir dados na tabela Paciente
INSERT INTO Paciente (Nome, Data_Nascimento, CPF, Telefone, Endereco, Email, CNPJ) VALUES
('José da Silva', '1980-05-15', '123.456.789-01', '(11) 8888-1001', 'Rua A, 100 - São Paulo/SP', 'jose.silva@email.com', NULL),
('Maria Oliveira', '1975-08-22', '234.567.890-12', '(21) 8888-2002', 'Rua B, 200 - Rio de Janeiro/RJ', 'maria.oliveira@email.com', NULL),
('Pedro Santos', '1990-12-10', '345.678.901-23', '(31) 8888-3003', 'Rua C, 300 - Belo Horizonte/MG', 'pedro.santos@email.com', '12.345.678/0001-90'),
('Ana Costa', '1985-03-18', '456.789.012-34', '(61) 8888-4004', 'Rua D, 400 - Brasília/DF', 'ana.costa@email.com', '98.765.432/0001-10'),
('Carlos Ferreira', '1992-07-25', '567.890.123-45', '(51) 8888-5005', 'Rua E, 500 - Porto Alegre/RS', 'carlos.ferreira@email.com', NULL),
('Luciana Silva', '1988-11-30', '678.901.234-56', '(11) 8888-6006', 'Rua F, 600 - São Paulo/SP', 'luciana.silva@email.com', '11.222.333/0001-44'),
('Ricardo Almeida', '1983-09-05', '789.012.345-67', '(21) 8888-7007', 'Rua G, 700 - Rio de Janeiro/RJ', 'ricardo.almeida@email.com', NULL),
('Fernanda Lima', '1995-04-12', '890.123.456-78', '(31) 8888-8008', 'Rua H, 800 - Belo Horizonte/MG', 'fernanda.lima@email.com', '55.666.777/0001-88'),
('Roberto Souza', '1979-01-20', '901.234.567-89', '(61) 8888-9009', 'Rua I, 900 - Brasília/DF', 'roberto.souza@email.com', NULL),
('Patrícia Martins', '1991-06-14', '012.345.678-90', '(51) 8888-0010', 'Rua J, 1000 - Porto Alegre/RS', 'patricia.martins@email.com', '33.444.555/0001-22');

-- Inserir dados na tabela Disponibilidade
INSERT INTO Disponibilidade (Status, Data, Hora, Cd_Unidade, Cd_Profissional) VALUES
('Disponível', '2025-07-15', '08:00', 1, 1),
('Disponível', '2025-07-15', '09:00', 1, 1),
('Disponível', '2025-07-15', '10:00', 1, 2),
('Disponível', '2025-07-15', '11:00', 2, 3),
('Disponível', '2025-07-15', '14:00', 2, 3),
('Disponível', '2025-07-16', '08:00', 3, 4),
('Disponível', '2025-07-16', '09:00', 3, 5),
('Disponível', '2025-07-16', '10:00', 4, 6),
('Disponível', '2025-07-16', '11:00', 4, 7),
('Disponível', '2025-07-17', '08:00', 5, 8),
('Ocupado', '2025-07-17', '09:00', 1, 1),
('Disponível', '2025-07-17', '10:00', 2, 2),
('Manutenção', '2025-07-18', '08:00', 3, NULL),
('Disponível', '2025-07-18', '14:00', 1, 3),
('Disponível', '2025-07-18', '15:00', 2, 4);

-- Inserir dados na tabela Exame
INSERT INTO Exame (Nome_Exame, Tipo_Exame, Requisitos, Descricao, Tempo_Estimado, Valor, Cd_Disponibilidade) VALUES
('Hemograma Completo', 'Laboratorial', 'Jejum de 8 horas', 'Exame de sangue para análise completa', 15, 45.00, 1),
('Glicemia de Jejum', 'Laboratorial', 'Jejum de 12 horas', 'Dosagem de glicose no sangue', 10, 25.00, 2),
('Ultrassom Abdominal', 'Imagem', 'Jejum de 6 horas', 'Ultrassonografia da região abdominal', 30, 120.00, 3),
('Raio-X Tórax', 'Imagem', 'Nenhum', 'Radiografia do tórax', 20, 80.00, 4),
('Consulta Cardiológica', 'Clínico', 'Trazer exames anteriores', 'Consulta com cardiologista', 45, 200.00, 5),
('Eletrocardiograma', 'Clínico', 'Nenhum', 'Exame do coração - ECG', 20, 60.00, 6),
('Colesterol Total', 'Laboratorial', 'Jejum de 12 horas', 'Dosagem de colesterol', 10, 30.00, 7),
('Mamografia', 'Imagem', 'Não usar desodorante', 'Exame das mamas', 25, 150.00, 8),
('Consulta Dermatológica', 'Clínico', 'Nenhum', 'Consulta com dermatologista', 30, 180.00, 9),
('Urina Tipo I', 'Laboratorial', 'Primeiro jato da manhã', 'Exame de urina rotina', 5, 20.00, 10);

-- Inserir dados na tabela Agendamento
INSERT INTO Agendamento (Hora, Data, Motivo_Agendamento, Status, Cd_Paciente, Cd_Unidade, Cd_Exame, Cd_Profissional) VALUES
('08:00', '2025-07-15', 'Check-up anual', 'Confirmado', 1, 1, 1, 1),
('09:00', '2025-07-15', 'Controle diabetes', 'Agendado', 2, 1, 2, 1),
('10:00', '2025-07-15', 'Dor abdominal', 'Confirmado', 3, 1, 3, 2),
('11:00', '2025-07-15', 'Exame admissional', 'Agendado', 4, 2, 4, 3),
('14:00', '2025-07-15', 'Rotina empresarial', 'Confirmado', 5, 2, 5, 3),
('08:00', '2025-07-16', 'Acompanhamento cardiológico', 'Agendado', 6, 3, 6, 4),
('09:00', '2025-07-16', 'Check-up preventivo', 'Confirmado', 7, 3, 7, 5),
('10:00', '2025-07-16', 'Rastreamento câncer mama', 'Agendado', 8, 4, 8, 6),
('11:00', '2025-07-16', 'Consulta dermatológica', 'Confirmado', 9, 4, 9, 7),
('08:00', '2025-07-17', 'Exame de rotina', 'Agendado', 10, 5, 10, 8);

-- Inserir dados na tabela Histórico
INSERT INTO Historico (Data_Registro, Recomendacoes, Cd_Paciente) VALUES
(GETDATE(), 'Manter dieta equilibrada e exercícios regulares', 1),
(GETDATE(), 'Controlar ingesta de açúcar, retorno em 3 meses', 2),
(GETDATE(), 'Resultados normais, manter acompanhamento anual', 3),
(GETDATE(), 'Apto para trabalho, sem restrições', 4),
(GETDATE(), 'Pressão arterial elevada, iniciar medicação', 5),
(GETDATE(), 'ECG normal, manter acompanhamento cardiológico', 6),
(GETDATE(), 'Colesterol borderline, ajustar dieta', 7),
(GETDATE(), 'Mamografia normal, repetir em 1 ano', 8),
(GETDATE(), 'Pele saudável, usar protetor solar diariamente', 9),
(GETDATE(), 'Exame de urina normal', 10);

-- Inserir dados na tabela Resultado
INSERT INTO Resultado (Resultado, Recomendacoes, Cd_Historico) VALUES
('Hemograma: valores dentro da normalidade', 'Manter hábitos saudáveis', 1),
('Glicemia: 95 mg/dL - Normal', 'Continuar dieta controlada', 2),
('Ultrassom: órgãos sem alterações', 'Repetir em 1 ano se assintomático', 3),
('Raio-X: campos pulmonares limpos', 'Nenhuma restrição', 4),
('Pressão: 140/90 mmHg - Hipertensão grau I', 'Iniciar anti-hipertensivo', 5),
('ECG: ritmo sinusal normal', 'Manter acompanhamento', 6),
('Colesterol Total: 210 mg/dL - Borderline', 'Dieta hipocolesterolêmica', 7),
('Mamografia: BIRADS I - Normal', 'Repetir rastreamento em 1 ano', 8),
('Pele: sem lesões suspeitas', 'Proteção solar diária', 9),
('EAS: densidade 1.020, sem alterações', 'Hidratação adequada', 10);

-- Inserir dados na tabela Consulta
INSERT INTO Consulta (Hora, Data, Tipo_Consulta, Status, Cd_Historico, Cd_Profissional) VALUES
('08:00', '2025-07-15', 'Consulta Inicial', 'Realizada', 1, 1),
('09:00', '2025-07-15', 'Retorno', 'Realizada', 2, 1),
('10:00', '2025-07-15', 'Consulta Inicial', 'Realizada', 3, 2),
('11:00', '2025-07-15', 'Exame Admissional', 'Realizada', 4, 3),
('14:00', '2025-07-15', 'Check-up', 'Realizada', 5, 3),
('08:00', '2025-07-16', 'Consulta Inicial', 'Agendada', 6, 4),
('09:00', '2025-07-16', 'Retorno', 'Agendada', 7, 5),
('10:00', '2025-07-16', 'Consulta Inicial', 'Agendada', 8, 6),
('11:00', '2025-07-16', 'Consulta Inicial', 'Agendada', 9, 7),
('08:00', '2025-07-17', 'Check-up', 'Agendada', 10, 8);

-- Inserir dados na tabela Notificação
INSERT INTO Notificacao (Status_Envio, Data_Envio, Mensagem, Tipo_Notificacao, Cd_Agendamento) VALUES
('Enviado', '2025-07-14 10:00:00', 'Lembre-se: exame agendado para amanhã às 08:00. Compareça em jejum.', 'Email', 1),
('Enviado', '2025-07-14 10:30:00', 'Seu exame está agendado para 15/07 às 09:00. Jejum de 12h necessário.', 'SMS', 2),
('Pendente', NULL, 'Confirmação: Ultrassom agendado para 15/07 às 10:00. Jejum de 6h.', 'Email', 3),
('Enviado', '2025-07-14 11:00:00', 'Exame admissional agendado para 15/07 às 11:00. Traga documentos.', 'WhatsApp', 4),
('Enviado', '2025-07-14 11:30:00', 'Check-up empresarial confirmado para 15/07 às 14:00.', 'Email', 5),
('Pendente', NULL, 'Consulta cardiológica agendada para 16/07 às 08:00.', 'SMS', 6),
('Enviado', '2025-07-15 14:00:00', 'Lembrete: exame preventivo amanhã às 09:00.', 'Email', 7),
('Pendente', NULL, 'Mamografia agendada para 16/07 às 10:00. Não use desodorante.', 'WhatsApp', 8),
('Enviado', '2025-07-15 15:00:00', 'Consulta dermatológica confirmada para 16/07 às 11:00.', 'Email', 9),
('Pendente', NULL, 'Exame de urina agendado para 17/07 às 08:00. Primeira urina da manhã.', 'SMS', 10);

PRINT 'Dados inseridos com sucesso!';
