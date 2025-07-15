-- Consultas SQL 
-- Mínimo 6 consultas, sendo 4 com junção entre tabelas

USE SistemaAgendamentoExames;
GO

-- ========================================
-- CONSULTA 1: Lista de agendamentos com dados do paciente e unidade (COM JUNÇÃO)
-- ========================================
PRINT '1. Lista de agendamentos com dados do paciente e unidade:'
SELECT 
    a.Cd_Agendamento,
    a.Data,
    a.Hora,
    p.Nome AS Nome_Paciente,
    p.CPF,
    u.Nome AS Nome_Unidade,
    u.Cidade,
    u.UF,
    a.Status,
    a.Motivo_Agendamento
FROM Agendamento a
INNER JOIN Paciente p ON a.Cd_Paciente = p.Cd_Paciente
INNER JOIN Unidade u ON a.Cd_Unidade = u.Cd_Unidade
ORDER BY a.Data, a.Hora;

-- ========================================
-- CONSULTA 2: Exames por tipo com disponibilidade e profissional (COM JUNÇÃO)
-- ========================================
PRINT '2. Exames por tipo com disponibilidade e profissional:'
SELECT 
    e.Tipo_Exame,
    e.Nome_Exame,
    e.Valor,
    d.Data,
    d.Hora,
    d.Status AS Status_Disponibilidade,
    u.Nome AS Unidade,
    ps.Nome AS Profissional,
    ps.Especialidade
FROM Exame e
INNER JOIN Disponibilidade d ON e.Cd_Disponibilidade = d.Cd_Disponibilidade
INNER JOIN Unidade u ON d.Cd_Unidade = u.Cd_Unidade
LEFT JOIN ProfissionalDeSaude ps ON d.Cd_Profissional = ps.Cd_Profissional
ORDER BY e.Tipo_Exame, e.Nome_Exame;

-- ========================================
-- CONSULTA 3: Histórico completo de pacientes empresariais (COM JUNÇÃO)
-- ========================================
PRINT '3. Histórico completo de pacientes empresariais:'
SELECT 
    p.Nome AS Nome_Paciente,
    p.CPF,
    e.Nome_Empresa,
    e.CNPJ,
    h.Data_Registro,
    h.Recomendacoes,
    r.Resultado,
    r.Data_Resultado
FROM Paciente p
INNER JOIN Empresa e ON p.CNPJ = e.CNPJ
INNER JOIN Historico h ON p.Cd_Paciente = h.Cd_Paciente
LEFT JOIN Resultado r ON h.Cd_Historico = r.Cd_Historico
ORDER BY e.Nome_Empresa, p.Nome;

-- ========================================
-- CONSULTA 4: Agendamentos com exames e notificações (COM JUNÇÃO)
-- ========================================
PRINT '4. Agendamentos com exames e notificações:'
SELECT 
    a.Cd_Agendamento,
    p.Nome AS Paciente,
    ex.Nome_Exame,
    ex.Tipo_Exame,
    a.Data,
    a.Hora,
    a.Status AS Status_Agendamento,
    n.Status_Envio,
    n.Tipo_Notificacao,
    n.Data_Envio
FROM Agendamento a
INNER JOIN Paciente p ON a.Cd_Paciente = p.Cd_Paciente
INNER JOIN Exame ex ON a.Cd_Exame = ex.Cd_Exame
LEFT JOIN Notificacao n ON a.Cd_Agendamento = n.Cd_Agendamento
ORDER BY a.Data, a.Hora;

-- ========================================
-- CONSULTA 5: Pacientes por faixa etária (SEM JUNÇÃO)
-- ========================================
PRINT '5. Distribuição de pacientes por faixa etária:'
SELECT 
    CASE 
        WHEN DATEDIFF(YEAR, Data_Nascimento, GETDATE()) < 18 THEN 'Menor de 18'
        WHEN DATEDIFF(YEAR, Data_Nascimento, GETDATE()) BETWEEN 18 AND 30 THEN '18-30 anos'
        WHEN DATEDIFF(YEAR, Data_Nascimento, GETDATE()) BETWEEN 31 AND 50 THEN '31-50 anos'
        WHEN DATEDIFF(YEAR, Data_Nascimento, GETDATE()) BETWEEN 51 AND 65 THEN '51-65 anos'
        ELSE 'Mais de 65 anos'
    END AS Faixa_Etaria,
    COUNT(*) AS Quantidade_Pacientes,
    ROUND(AVG(CAST(DATEDIFF(YEAR, Data_Nascimento, GETDATE()) AS FLOAT)), 1) AS Idade_Media
FROM Paciente
GROUP BY 
    CASE 
        WHEN DATEDIFF(YEAR, Data_Nascimento, GETDATE()) < 18 THEN 'Menor de 18'
        WHEN DATEDIFF(YEAR, Data_Nascimento, GETDATE()) BETWEEN 18 AND 30 THEN '18-30 anos'
        WHEN DATEDIFF(YEAR, Data_Nascimento, GETDATE()) BETWEEN 31 AND 50 THEN '31-50 anos'
        WHEN DATEDIFF(YEAR, Data_Nascimento, GETDATE()) BETWEEN 51 AND 65 THEN '51-65 anos'
        ELSE 'Mais de 65 anos'
    END
ORDER BY Idade_Media;

-- ========================================
-- CONSULTA 6: Estatísticas de exames por tipo (SEM JUNÇÃO)
-- ========================================
PRINT '6. Estatísticas de exames por tipo:'
SELECT 
    Tipo_Exame,
    COUNT(*) AS Total_Exames,
    AVG(Valor) AS Valor_Medio,
    MIN(Valor) AS Valor_Minimo,
    MAX(Valor) AS Valor_Maximo,
    AVG(Tempo_Estimado) AS Tempo_Medio_Minutos
FROM Exame
GROUP BY Tipo_Exame
ORDER BY Total_Exames DESC;

-- ========================================
-- CONSULTA 7: Disponibilidade por unidade e status
-- ========================================
PRINT '7. Relatório de disponibilidade por unidade:'
SELECT 
    u.Nome AS Unidade,
    u.Cidade,
    d.Status,
    COUNT(*) AS Quantidade_Horarios,
    MIN(d.Data) AS Data_Inicio,
    MAX(d.Data) AS Data_Final
FROM Unidade u
INNER JOIN Disponibilidade d ON u.Cd_Unidade = d.Cd_Unidade
GROUP BY u.Nome, u.Cidade, d.Status
ORDER BY u.Nome, d.Status;

-- ========================================
-- CONSULTA 8: Top 5 profissionais com mais agendamentos
-- ========================================
PRINT '8. Top 5 profissionais com mais agendamentos:'
SELECT TOP 5
    ps.Nome AS Profissional,
    ps.Especialidade,
    ps.CRM,
    COUNT(a.Cd_Agendamento) AS Total_Agendamentos,
    COUNT(CASE WHEN a.Status = 'Realizado' THEN 1 END) AS Agendamentos_Realizados,
    ROUND(
        CAST(COUNT(CASE WHEN a.Status = 'Realizado' THEN 1 END) AS FLOAT) / 
        CAST(COUNT(a.Cd_Agendamento) AS FLOAT) * 100, 2
    ) AS Percentual_Realizacao
FROM ProfissionalDeSaude ps
LEFT JOIN Agendamento a ON ps.Cd_Profissional = a.Cd_Profissional
GROUP BY ps.Nome, ps.Especialidade, ps.CRM
HAVING COUNT(a.Cd_Agendamento) > 0
ORDER BY Total_Agendamentos DESC;

-- ========================================
-- CONSULTA 9: Empresas com mais pacientes atendidos
-- ========================================
PRINT '9. Ranking de empresas por número de pacientes:'
SELECT 
    e.Nome_Empresa,
    e.CNPJ,
    COUNT(p.Cd_Paciente) AS Total_Pacientes,
    COUNT(a.Cd_Agendamento) AS Total_Agendamentos,
    CASE 
        WHEN COUNT(a.Cd_Agendamento) > 0 
        THEN ROUND(CAST(COUNT(a.Cd_Agendamento) AS FLOAT) / CAST(COUNT(p.Cd_Paciente) AS FLOAT), 2)
        ELSE 0
    END AS Media_Agendamentos_Por_Paciente
FROM Empresa e
INNER JOIN Paciente p ON e.CNPJ = p.CNPJ
LEFT JOIN Agendamento a ON p.Cd_Paciente = a.Cd_Paciente
GROUP BY e.Nome_Empresa, e.CNPJ
ORDER BY Total_Pacientes DESC;

-- ========================================
-- CONSULTA 10: Eficácia do sistema de notificações
-- ========================================
PRINT '10. Relatório de eficácia das notificações:'
SELECT 
    n.Tipo_Notificacao,
    COUNT(*) AS Total_Notificacoes,
    COUNT(CASE WHEN n.Status_Envio = 'Enviado' THEN 1 END) AS Enviadas_Sucesso,
    COUNT(CASE WHEN n.Status_Envio = 'Falha' THEN 1 END) AS Falhas_Envio,
    COUNT(CASE WHEN n.Status_Envio = 'Pendente' THEN 1 END) AS Pendentes,
    ROUND(
        CAST(COUNT(CASE WHEN n.Status_Envio = 'Enviado' THEN 1 END) AS FLOAT) / 
        CAST(COUNT(*) AS FLOAT) * 100, 2
    ) AS Taxa_Sucesso_Percentual
FROM Notificacao n
GROUP BY n.Tipo_Notificacao
ORDER BY Taxa_Sucesso_Percentual DESC;

PRINT 'Todas as consultas executadas com sucesso!';
