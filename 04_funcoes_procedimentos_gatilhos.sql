-- Funções, Procedimentos e Gatilhos 
-- Processamento de BD ativo com gatilhos e procedimentos

USE SistemaAgendamentoExames;
GO

-- ========================================
-- FUNÇÃO 1: Calcular idade do paciente
-- ========================================
CREATE FUNCTION fn_CalcularIdade(@DataNascimento DATE)
RETURNS INT
AS
BEGIN
    RETURN DATEDIFF(YEAR, @DataNascimento, GETDATE()) - 
           CASE 
               WHEN MONTH(@DataNascimento) > MONTH(GETDATE()) OR 
                    (MONTH(@DataNascimento) = MONTH(GETDATE()) AND DAY(@DataNascimento) > DAY(GETDATE()))
               THEN 1 
               ELSE 0 
           END;
END;
GO

-- ========================================
-- FUNÇÃO 2: Verificar se paciente está em jejum adequado
-- ========================================
CREATE FUNCTION fn_VerificarJejum(@CdExame INT, @HoraAgendamento TIME)
RETURNS VARCHAR(100)
AS
BEGIN
    DECLARE @Requisitos VARCHAR(MAX);
    DECLARE @Resultado VARCHAR(100);
    
    SELECT @Requisitos = Requisitos FROM Exame WHERE Cd_Exame = @CdExame;
    
    IF @Requisitos LIKE '%jejum%' OR @Requisitos LIKE '%Jejum%'
    BEGIN
        IF @HoraAgendamento <= '10:00:00'
            SET @Resultado = 'Horário adequado para jejum';
        ELSE
            SET @Resultado = 'ATENÇÃO: Horário pode não ser adequado para jejum';
    END
    ELSE
        SET @Resultado = 'Jejum não necessário';
    
    RETURN @Resultado;
END;
GO

-- ========================================
-- FUNÇÃO 3: Calcular receita total por período
-- ========================================
CREATE FUNCTION fn_ReceitaPorPeriodo(@DataInicio DATE, @DataFim DATE)
RETURNS DECIMAL(15,2)
AS
BEGIN
    DECLARE @Receita DECIMAL(15,2);
    
    SELECT @Receita = ISNULL(SUM(e.Valor), 0)
    FROM Agendamento a
    INNER JOIN Exame e ON a.Cd_Exame = e.Cd_Exame
    WHERE a.Data BETWEEN @DataInicio AND @DataFim
    AND a.Status IN ('Confirmado', 'Realizado');
    
    RETURN @Receita;
END;
GO

-- ========================================
-- PROCEDIMENTO 1: Agendar exame com validações
-- ========================================
CREATE PROCEDURE sp_AgendarExame
    @CdPaciente INT,
    @CdUnidade INT,
    @CdExame INT,
    @Data DATE,
    @Hora TIME,
    @MotivoAgendamento VARCHAR(200) = NULL,
    @CdProfissional INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @Erro VARCHAR(500) = '';
    DECLARE @CdDisponibilidade INT;
    DECLARE @StatusDisponibilidade VARCHAR(20);
    
    -- Validar se a data é futura
    IF @Data <= CAST(GETDATE() AS DATE)
    BEGIN
        SET @Erro = 'Data do agendamento deve ser futura';
        RAISERROR(@Erro, 16, 1);
        RETURN;
    END
    
    -- Verificar disponibilidade
    SELECT @CdDisponibilidade = Cd_Disponibilidade, @StatusDisponibilidade = Status
    FROM Disponibilidade 
    WHERE Cd_Unidade = @CdUnidade 
    AND Data = @Data 
    AND Hora = @Hora
    AND (Cd_Profissional = @CdProfissional OR @CdProfissional IS NULL);
    
    IF @CdDisponibilidade IS NULL
    BEGIN
        SET @Erro = 'Horário não disponível para agendamento';
        RAISERROR(@Erro, 16, 1);
        RETURN;
    END
    
    IF @StatusDisponibilidade != 'Disponível'
    BEGIN
        SET @Erro = 'Horário não está disponível (Status: ' + @StatusDisponibilidade + ')';
        RAISERROR(@Erro, 16, 1);
        RETURN;
    END
    
    -- Verificar se paciente já tem agendamento no mesmo horário
    IF EXISTS(SELECT 1 FROM Agendamento WHERE Cd_Paciente = @CdPaciente AND Data = @Data AND Hora = @Hora AND Status NOT IN ('Cancelado'))
    BEGIN
        SET @Erro = 'Paciente já possui agendamento neste horário';
        RAISERROR(@Erro, 16, 1);
        RETURN;
    END
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Inserir agendamento
        INSERT INTO Agendamento (Hora, Data, Motivo_Agendamento, Status, Cd_Paciente, Cd_Unidade, Cd_Exame, Cd_Profissional)
        VALUES (@Hora, @Data, @MotivoAgendamento, 'Agendado', @CdPaciente, @CdUnidade, @CdExame, @CdProfissional);
        
        -- Atualizar disponibilidade
        UPDATE Disponibilidade 
        SET Status = 'Ocupado' 
        WHERE Cd_Disponibilidade = @CdDisponibilidade;
        
        COMMIT TRANSACTION;
        
        PRINT 'Agendamento realizado com sucesso!';
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- ========================================
-- PROCEDIMENTO 2: Cancelar agendamento
-- ========================================
CREATE PROCEDURE sp_CancelarAgendamento
    @CdAgendamento INT,
    @Motivo VARCHAR(200) = 'Cancelamento solicitado pelo paciente'
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @CdUnidade INT, @Data DATE, @Hora TIME, @CdProfissional INT;
    DECLARE @StatusAtual VARCHAR(20);
    
    -- Verificar se agendamento existe e obter dados
    SELECT @CdUnidade = Cd_Unidade, @Data = Data, @Hora = Hora, @CdProfissional = Cd_Profissional, @StatusAtual = Status
    FROM Agendamento 
    WHERE Cd_Agendamento = @CdAgendamento;
    
    IF @CdUnidade IS NULL
    BEGIN
        RAISERROR('Agendamento não encontrado', 16, 1);
        RETURN;
    END
    
    IF @StatusAtual IN ('Cancelado', 'Realizado')
    BEGIN
        RAISERROR('Agendamento não pode ser cancelado (Status atual: %s)', 16, 1, @StatusAtual);
        RETURN;
    END
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Atualizar status do agendamento
        UPDATE Agendamento 
        SET Status = 'Cancelado' 
        WHERE Cd_Agendamento = @CdAgendamento;
        
        -- Liberar disponibilidade
        UPDATE Disponibilidade 
        SET Status = 'Disponível' 
        WHERE Cd_Unidade = @CdUnidade 
        AND Data = @Data 
        AND Hora = @Hora
        AND (Cd_Profissional = @CdProfissional OR @CdProfissional IS NULL);
        
        COMMIT TRANSACTION;
        
        PRINT 'Agendamento cancelado com sucesso!';
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- ========================================
-- GATILHO 1: Validar dados do paciente antes de inserir/atualizar
-- ========================================
CREATE TRIGGER trg_ValidarPaciente
ON Paciente
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @Erro VARCHAR(500);
    DECLARE @CdPaciente INT, @DataNascimento DATE, @CNPJ VARCHAR(18);
    
    -- Cursor para processar todos os registros afetados
    DECLARE paciente_cursor CURSOR FOR
    SELECT Cd_Paciente, Data_Nascimento, CNPJ FROM inserted;
    
    OPEN paciente_cursor;
    FETCH NEXT FROM paciente_cursor INTO @CdPaciente, @DataNascimento, @CNPJ;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Validar idade mínima (deve ser maior que 0 e menor que 120 anos)
        IF DATEDIFF(YEAR, @DataNascimento, GETDATE()) < 0 OR DATEDIFF(YEAR, @DataNascimento, GETDATE()) > 120
        BEGIN
            SET @Erro = 'Data de nascimento inválida para o paciente ID: ' + CAST(@CdPaciente AS VARCHAR(10));
            RAISERROR(@Erro, 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        -- Validar se CNPJ existe na tabela Empresa (quando informado)
        IF @CNPJ IS NOT NULL AND NOT EXISTS(SELECT 1 FROM Empresa WHERE CNPJ = @CNPJ)
        BEGIN
            SET @Erro = 'CNPJ informado não existe na tabela Empresa: ' + @CNPJ;
            RAISERROR(@Erro, 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        FETCH NEXT FROM paciente_cursor INTO @CdPaciente, @DataNascimento, @CNPJ;
    END
    
    CLOSE paciente_cursor;
    DEALLOCATE paciente_cursor;
END;
GO

-- ========================================
-- GATILHO 2: Controlar conflitos de agendamento
-- ========================================
CREATE TRIGGER trg_ControlarAgendamento
ON Agendamento
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @CdAgendamento INT, @CdPaciente INT, @Data DATE, @Hora TIME, @CdUnidade INT, @CdProfissional INT;
    DECLARE @Conflitos INT;
    DECLARE @Erro VARCHAR(500);
    
    -- Cursor para processar todos os registros afetados
    DECLARE agendamento_cursor CURSOR FOR
    SELECT Cd_Agendamento, Cd_Paciente, Data, Hora, Cd_Unidade, Cd_Profissional FROM inserted;
    
    OPEN agendamento_cursor;
    FETCH NEXT FROM agendamento_cursor INTO @CdAgendamento, @CdPaciente, @Data, @Hora, @CdUnidade, @CdProfissional;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Verificar conflito de horário para o mesmo profissional
        IF @CdProfissional IS NOT NULL
        BEGIN
            SELECT @Conflitos = COUNT(*)
            FROM Agendamento 
            WHERE Cd_Profissional = @CdProfissional 
            AND Data = @Data 
            AND Hora = @Hora
            AND Status NOT IN ('Cancelado')
            AND Cd_Agendamento != @CdAgendamento;
            
            IF @Conflitos > 0
            BEGIN
                SET @Erro = 'Conflito de horário: Profissional já possui agendamento neste horário';
                RAISERROR(@Erro, 16, 1);
                ROLLBACK TRANSACTION;
                RETURN;
            END
        END
        
        -- Verificar se paciente tem mais de 3 agendamentos no mesmo dia
        SELECT @Conflitos = COUNT(*)
        FROM Agendamento 
        WHERE Cd_Paciente = @CdPaciente 
        AND Data = @Data
        AND Status NOT IN ('Cancelado')
        AND Cd_Agendamento != @CdAgendamento;
        
        IF @Conflitos >= 3
        BEGIN
            SET @Erro = 'Paciente não pode ter mais de 3 agendamentos no mesmo dia';
            RAISERROR(@Erro, 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        FETCH NEXT FROM agendamento_cursor INTO @CdAgendamento, @CdPaciente, @Data, @Hora, @CdUnidade, @CdProfissional;
    END
    
    CLOSE agendamento_cursor;
    DEALLOCATE agendamento_cursor;
END;
GO

-- ========================================
-- GATILHO 3: Criar notificação automática ao agendar exame
-- ========================================
CREATE TRIGGER trg_CriarNotificacao
ON Agendamento
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @CdAgendamento INT, @CdPaciente INT, @Data DATE, @Hora TIME;
    DECLARE @NomePaciente VARCHAR(100), @NomeExame VARCHAR(100), @Requisitos TEXT;
    DECLARE @Mensagem TEXT;
    
    -- Cursor para processar todos os registros inseridos
    DECLARE notificacao_cursor CURSOR FOR
    SELECT i.Cd_Agendamento, i.Cd_Paciente, i.Data, i.Hora
    FROM inserted i;
    
    OPEN notificacao_cursor;
    FETCH NEXT FROM notificacao_cursor INTO @CdAgendamento, @CdPaciente, @Data, @Hora;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Obter dados para criar a mensagem
        SELECT 
            @NomePaciente = p.Nome,
            @NomeExame = e.Nome_Exame,
            @Requisitos = e.Requisitos
        FROM Paciente p
        INNER JOIN Agendamento a ON p.Cd_Paciente = a.Cd_Paciente
        INNER JOIN Exame e ON a.Cd_Exame = e.Cd_Exame
        WHERE a.Cd_Agendamento = @CdAgendamento;
        
        -- Criar mensagem personalizada
        SET @Mensagem = 'Olá ' + @NomePaciente + '! Seu exame "' + @NomeExame + '" está agendado para ' + 
                       FORMAT(@Data, 'dd/MM/yyyy') + ' às ' + FORMAT(@Hora, 'HH:mm') + '.';
        
        IF @Requisitos IS NOT NULL AND @Requisitos != ''
            SET @Mensagem = @Mensagem + ' Requisitos: ' + @Requisitos;
        
        -- Inserir notificação
        INSERT INTO Notificacao (Status_Envio, Mensagem, Tipo_Notificacao, Cd_Agendamento)
        VALUES ('Pendente', @Mensagem, 'Email', @CdAgendamento);
        
        FETCH NEXT FROM notificacao_cursor INTO @CdAgendamento, @CdPaciente, @Data, @Hora;
    END
    
    CLOSE notificacao_cursor;
    DEALLOCATE notificacao_cursor;
END;
GO

-- ========================================
-- GATILHO 4: Auditoria de mudanças no status do agendamento
-- ========================================
-- Primeiro, criar tabela de auditoria
CREATE TABLE AuditoriaAgendamento (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Cd_Agendamento INT NOT NULL,
    Status_Anterior VARCHAR(20),
    Status_Novo VARCHAR(20),
    Data_Alteracao DATETIME DEFAULT GETDATE(),
    Usuario VARCHAR(100) DEFAULT SUSER_SNAME()
);
GO

CREATE TRIGGER trg_AuditoriaAgendamento
ON Agendamento
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO AuditoriaAgendamento (Cd_Agendamento, Status_Anterior, Status_Novo)
    SELECT 
        i.Cd_Agendamento,
        d.Status AS Status_Anterior,
        i.Status AS Status_Novo
    FROM inserted i
    INNER JOIN deleted d ON i.Cd_Agendamento = d.Cd_Agendamento
    WHERE i.Status != d.Status;
END;
GO

-- ========================================
-- PROCEDIMENTO 3: Relatório de agendamentos com validação
-- ========================================
CREATE PROCEDURE sp_RelatorioAgendamentos
    @DataInicio DATE,
    @DataFim DATE,
    @Status VARCHAR(20) = NULL,
    @CdUnidade INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validar parâmetros
    IF @DataInicio > @DataFim
    BEGIN
        RAISERROR('Data de início não pode ser maior que data de fim', 16, 1);
        RETURN;
    END
    
    SELECT 
        a.Cd_Agendamento,
        p.Nome AS Paciente,
        p.CPF,
        CASE 
            WHEN p.CNPJ IS NOT NULL THEN 'Empresarial'
            ELSE 'Individual'
        END AS Tipo_Paciente,
        e.Nome_Exame,
        e.Tipo_Exame,
        e.Valor,
        u.Nome AS Unidade,
        ps.Nome AS Profissional,
        a.Data,
        a.Hora,
        a.Status,
        a.Motivo_Agendamento,
        dbo.fn_VerificarJejum(a.Cd_Exame, a.Hora) AS Status_Jejum
    FROM Agendamento a
    INNER JOIN Paciente p ON a.Cd_Paciente = p.Cd_Paciente
    INNER JOIN Exame e ON a.Cd_Exame = e.Cd_Exame
    INNER JOIN Unidade u ON a.Cd_Unidade = u.Cd_Unidade
    LEFT JOIN ProfissionalDeSaude ps ON a.Cd_Profissional = ps.Cd_Profissional
    WHERE a.Data BETWEEN @DataInicio AND @DataFim
    AND (@Status IS NULL OR a.Status = @Status)
    AND (@CdUnidade IS NULL OR a.Cd_Unidade = @CdUnidade)
    ORDER BY a.Data, a.Hora;
    
    -- Estatísticas do período
    SELECT 
        COUNT(*) AS Total_Agendamentos,
        COUNT(CASE WHEN Status = 'Realizado' THEN 1 END) AS Realizados,
        COUNT(CASE WHEN Status = 'Cancelado' THEN 1 END) AS Cancelados,
        SUM(e.Valor) AS Receita_Total,
        dbo.fn_ReceitaPorPeriodo(@DataInicio, @DataFim) AS Receita_Confirmada
    FROM Agendamento a
    INNER JOIN Exame e ON a.Cd_Exame = e.Cd_Exame
    WHERE a.Data BETWEEN @DataInicio AND @DataFim
    AND (@CdUnidade IS NULL OR a.Cd_Unidade = @CdUnidade);
END;
GO

PRINT 'Funções, procedimentos e gatilhos criados com sucesso!';
PRINT 'Regras de integridade implementadas:';
PRINT '1. Validação de idade dos pacientes';
PRINT '2. Controle de conflitos de agendamento';
PRINT '3. Limite de agendamentos por paciente/dia';
PRINT '4. Validação de CNPJ empresarial';
PRINT '5. Auditoria de mudanças de status';
PRINT '6. Criação automática de notificações';
