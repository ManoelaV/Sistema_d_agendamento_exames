-- Script de Testes
-- Testes para validar funcionalidades, gatilhos e integridade

USE SistemaAgendamentoExames;
GO

PRINT '========================================';
PRINT 'INICIANDO TESTES DO SISTEMA';
PRINT '========================================';

-- ========================================
-- TESTE 1: Testar função de cálculo de idade
-- ========================================
PRINT '1. Testando função de cálculo de idade:';
SELECT 
    Nome,
    Data_Nascimento,
    dbo.fn_CalcularIdade(Data_Nascimento) AS Idade
FROM Paciente
WHERE Cd_Paciente <= 5;

-- ========================================
-- TESTE 2: Testar função de verificação de jejum
-- ========================================
PRINT '2. Testando função de verificação de jejum:';
SELECT 
    e.Nome_Exame,
    e.Requisitos,
    dbo.fn_VerificarJejum(e.Cd_Exame, '08:00') AS Status_08h,
    dbo.fn_VerificarJejum(e.Cd_Exame, '14:00') AS Status_14h
FROM Exame e
WHERE e.Cd_Exame <= 5;

-- ========================================
-- TESTE 3: Testar função de receita por período
-- ========================================
PRINT '3. Testando função de receita por período:';
SELECT dbo.fn_ReceitaPorPeriodo('2025-07-15', '2025-07-17') AS Receita_Periodo;

-- ========================================
-- TESTE 4: Testar procedimento de agendamento (sucesso)
-- ========================================
PRINT '4. Testando agendamento válido:';
BEGIN TRY
    EXEC sp_AgendarExame 
        @CdPaciente = 1,
        @CdUnidade = 1,
        @CdExame = 1,
        @Data = '2025-07-20',
        @Hora = '14:00',
        @MotivoAgendamento = 'Teste de agendamento',
        @CdProfissional = 1;
    PRINT 'SUCESSO: Agendamento criado';
END TRY
BEGIN CATCH
    PRINT 'ERRO: ' + ERROR_MESSAGE();
END CATCH

-- ========================================
-- TESTE 5: Testar gatilho de validação - idade inválida
-- ========================================
PRINT '5. Testando validação de idade (deve falhar):';
BEGIN TRY
    INSERT INTO Paciente (Nome, Data_Nascimento, CPF, Telefone, Endereco, Email)
    VALUES ('Teste Idade', '2030-01-01', '999.999.999-99', '(11) 9999-9999', 'Rua Teste', 'teste@email.com');
    PRINT 'ERRO: Deveria ter falhado na validação de idade';
END TRY
BEGIN CATCH
    PRINT 'SUCESSO: Validação de idade funcionou - ' + ERROR_MESSAGE();
END CATCH

-- ========================================
-- TESTE 6: Testar gatilho de validação - CNPJ inválido
-- ========================================
PRINT '6. Testando validação de CNPJ (deve falhar):';
BEGIN TRY
    INSERT INTO Paciente (Nome, Data_Nascimento, CPF, Telefone, Endereco, Email, CNPJ)
    VALUES ('Teste CNPJ', '1990-01-01', '888.888.888-88', '(11) 8888-8888', 'Rua Teste', 'teste2@email.com', '99.999.999/9999-99');
    PRINT 'ERRO: Deveria ter falhado na validação de CNPJ';
END TRY
BEGIN CATCH
    PRINT 'SUCESSO: Validação de CNPJ funcionou - ' + ERROR_MESSAGE();
END CATCH

-- ========================================
-- TESTE 7: Testar conflito de agendamento
-- ========================================
PRINT '7. Testando conflito de agendamento (deve falhar):';
BEGIN TRY
    EXEC sp_AgendarExame 
        @CdPaciente = 2,
        @CdUnidade = 1,
        @CdExame = 2,
        @Data = '2025-07-15',
        @Hora = '08:00',
        @MotivoAgendamento = 'Teste conflito',
        @CdProfissional = 1;
    PRINT 'ERRO: Deveria ter falhado por conflito';
END TRY
BEGIN CATCH
    PRINT 'SUCESSO: Validação de conflito funcionou - ' + ERROR_MESSAGE();
END CATCH

-- ========================================
-- TESTE 8: Testar cancelamento de agendamento
-- ========================================
PRINT '8. Testando cancelamento de agendamento:';
DECLARE @UltimoAgendamento INT;
SELECT @UltimoAgendamento = MAX(Cd_Agendamento) FROM Agendamento;

BEGIN TRY
    EXEC sp_CancelarAgendamento @CdAgendamento = @UltimoAgendamento;
    PRINT 'SUCESSO: Agendamento cancelado';
END TRY
BEGIN CATCH
    PRINT 'ERRO: ' + ERROR_MESSAGE();
END CATCH

-- ========================================
-- TESTE 9: Verificar criação automática de notificação
-- ========================================
PRINT '9. Verificando criação automática de notificação:';
SELECT TOP 3
    n.Cd_Notificacao,
    n.Status_Envio,
    LEFT(n.Mensagem, 50) + '...' AS Mensagem_Resumo,
    n.Tipo_Notificacao,
    a.Cd_Agendamento
FROM Notificacao n
INNER JOIN Agendamento a ON n.Cd_Agendamento = a.Cd_Agendamento
ORDER BY n.Cd_Notificacao DESC;

-- ========================================
-- TESTE 10: Testar relatório com parâmetros
-- ========================================
PRINT '10. Testando relatório de agendamentos:';
EXEC sp_RelatorioAgendamentos 
    @DataInicio = '2025-07-15',
    @DataFim = '2025-07-17',
    @Status = 'Agendado';

-- ========================================
-- TESTE 11: Verificar auditoria de mudanças
-- ========================================
PRINT '11. Verificando auditoria de mudanças:';

-- Atualizar status de um agendamento para testar auditoria
UPDATE Agendamento 
SET Status = 'Confirmado' 
WHERE Cd_Agendamento = 1;

-- Verificar se a auditoria foi registrada
SELECT 
    aa.Cd_Agendamento,
    aa.Status_Anterior,
    aa.Status_Novo,
    aa.Data_Alteracao,
    aa.Usuario
FROM AuditoriaAgendamento aa
ORDER BY aa.Data_Alteracao DESC;

-- ========================================
-- TESTE 12: Testar limite de agendamentos por dia
-- ========================================
PRINT '12. Testando limite de agendamentos por dia:';

-- Primeiro, vamos criar disponibilidades adicionais para o teste
INSERT INTO Disponibilidade (Status, Data, Hora, Cd_Unidade, Cd_Profissional) VALUES
('Disponível', '2025-07-25', '08:00', 1, 1),
('Disponível', '2025-07-25', '09:00', 1, 1),
('Disponível', '2025-07-25', '10:00', 1, 1),
('Disponível', '2025-07-25', '11:00', 1, 1);

-- Inserir exames para as novas disponibilidades
DECLARE @NewDisp1 INT = (SELECT Cd_Disponibilidade FROM Disponibilidade WHERE Data = '2025-07-25' AND Hora = '08:00' AND Cd_Unidade = 1);
DECLARE @NewDisp2 INT = (SELECT Cd_Disponibilidade FROM Disponibilidade WHERE Data = '2025-07-25' AND Hora = '09:00' AND Cd_Unidade = 1);
DECLARE @NewDisp3 INT = (SELECT Cd_Disponibilidade FROM Disponibilidade WHERE Data = '2025-07-25' AND Hora = '10:00' AND Cd_Unidade = 1);
DECLARE @NewDisp4 INT = (SELECT Cd_Disponibilidade FROM Disponibilidade WHERE Data = '2025-07-25' AND Hora = '11:00' AND Cd_Unidade = 1);

INSERT INTO Exame (Nome_Exame, Tipo_Exame, Requisitos, Descricao, Tempo_Estimado, Valor, Cd_Disponibilidade) VALUES
('Teste 1', 'Laboratorial', 'Nenhum', 'Teste 1', 15, 50.00, @NewDisp1),
('Teste 2', 'Laboratorial', 'Nenhum', 'Teste 2', 15, 50.00, @NewDisp2),
('Teste 3', 'Laboratorial', 'Nenhum', 'Teste 3', 15, 50.00, @NewDisp3),
('Teste 4', 'Laboratorial', 'Nenhum', 'Teste 4', 15, 50.00, @NewDisp4);

-- Agora testar o limite (primeiros 3 devem funcionar, o 4º deve falhar)
DECLARE @ExameTest1 INT = (SELECT Cd_Exame FROM Exame WHERE Nome_Exame = 'Teste 1');
DECLARE @ExameTest2 INT = (SELECT Cd_Exame FROM Exame WHERE Nome_Exame = 'Teste 2');
DECLARE @ExameTest3 INT = (SELECT Cd_Exame FROM Exame WHERE Nome_Exame = 'Teste 3');
DECLARE @ExameTest4 INT = (SELECT Cd_Exame FROM Exame WHERE Nome_Exame = 'Teste 4');

-- Agendamento 1 (deve funcionar)
BEGIN TRY
    EXEC sp_AgendarExame @CdPaciente = 1, @CdUnidade = 1, @CdExame = @ExameTest1, @Data = '2025-07-25', @Hora = '08:00', @CdProfissional = 1;
    PRINT 'Agendamento 1/3 criado com sucesso';
END TRY
BEGIN CATCH
    PRINT 'Erro no agendamento 1: ' + ERROR_MESSAGE();
END CATCH

-- Agendamento 2 (deve funcionar)
BEGIN TRY
    EXEC sp_AgendarExame @CdPaciente = 1, @CdUnidade = 1, @CdExame = @ExameTest2, @Data = '2025-07-25', @Hora = '09:00', @CdProfissional = 1;
    PRINT 'Agendamento 2/3 criado com sucesso';
END TRY
BEGIN CATCH
    PRINT 'Erro no agendamento 2: ' + ERROR_MESSAGE();
END CATCH

-- Agendamento 3 (deve funcionar)
BEGIN TRY
    EXEC sp_AgendarExame @CdPaciente = 1, @CdUnidade = 1, @CdExame = @ExameTest3, @Data = '2025-07-25', @Hora = '10:00', @CdProfissional = 1;
    PRINT 'Agendamento 3/3 criado com sucesso';
END TRY
BEGIN CATCH
    PRINT 'Erro no agendamento 3: ' + ERROR_MESSAGE();
END CATCH

-- Agendamento 4 (deve falhar - excede limite)
BEGIN TRY
    EXEC sp_AgendarExame @CdPaciente = 1, @CdUnidade = 1, @CdExame = @ExameTest4, @Data = '2025-07-25', @Hora = '11:00', @CdProfissional = 1;
    PRINT 'ERRO: Agendamento 4 não deveria ter sido permitido';
END TRY
BEGIN CATCH
    PRINT 'SUCESSO: Limite de agendamentos funcionou - ' + ERROR_MESSAGE();
END CATCH

-- ========================================
-- RESUMO DOS TESTES
-- ========================================
PRINT '========================================';
PRINT 'RESUMO DOS TESTES EXECUTADOS:';
PRINT '========================================';
PRINT '✓ Funções de cálculo de idade';
PRINT '✓ Funções de verificação de jejum';
PRINT '✓ Funções de cálculo de receita';
PRINT '✓ Procedimento de agendamento';
PRINT '✓ Procedimento de cancelamento';
PRINT '✓ Gatilho de validação de idade';
PRINT '✓ Gatilho de validação de CNPJ';
PRINT '✓ Gatilho de controle de conflitos';
PRINT '✓ Gatilho de criação de notificações';
PRINT '✓ Gatilho de auditoria';
PRINT '✓ Gatilho de limite de agendamentos/dia';
PRINT '✓ Relatórios com validação';
PRINT '========================================';

-- Verificar quantidades finais
SELECT 'Pacientes' AS Tabela, COUNT(*) AS Total FROM Paciente
UNION ALL
SELECT 'Agendamentos' AS Tabela, COUNT(*) AS Total FROM Agendamento
UNION ALL
SELECT 'Notificações' AS Tabela, COUNT(*) AS Total FROM Notificacao
UNION ALL
SELECT 'Auditorias' AS Tabela, COUNT(*) AS Total FROM AuditoriaAgendamento;
