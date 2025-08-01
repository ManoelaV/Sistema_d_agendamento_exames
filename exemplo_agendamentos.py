#!/usr/bin/env python3
"""
Exemplo de uso das funcionalidades de agendamento e resultados
Sistema de Agendamento de Exames - Clínica
"""

from models import ClinicaModel
from datetime import datetime, date, timedelta
import traceback

def main():
    print("🏥 === Exemplo de Agendamentos e Resultados ===")
    print()
    
    # Inicializar modelo
    model = ClinicaModel()
    
    # Testar conexão
    if not model.test_connection():
        print("❌ Erro: Não foi possível conectar ao banco de dados")
        print("   Verifique se o MySQL está rodando e configure corretamente")
        return
    
    print("✅ Conexão com banco estabelecida!")
    print()
    
    try:
        # 1. Listar dados disponíveis
        print("📋 === DADOS DISPONÍVEIS ===")
        
        pacientes = model.get_pacientes()
        print(f"👥 Pacientes cadastrados: {len(pacientes) if pacientes else 0}")
        if pacientes:
            for i, pac in enumerate(pacientes[:3]):  # Mostrar apenas 3
                print(f"   {i+1}. {pac['nome']} - CPF: {pac['cpf']}")
        
        exames = model.get_exames()
        print(f"🔬 Exames disponíveis: {len(exames) if exames else 0}")
        if exames:
            for i, exame in enumerate(exames[:3]):  # Mostrar apenas 3
                print(f"   {i+1}. {exame['nome']} ({exame['tipo']}) - {exame['tempo_estimado']}min")
        
        unidades = model.get_unidades()
        print(f"🏢 Unidades disponíveis: {len(unidades) if unidades else 0}")
        if unidades:
            for i, unidade in enumerate(unidades[:3]):  # Mostrar apenas 3
                print(f"   {i+1}. Unidade {unidade['id_unidade']} - {unidade['endereco']}")
        
        profissionais = model.get_profissionais()
        print(f"👨‍⚕️ Profissionais disponíveis: {len(profissionais) if profissionais else 0}")
        if profissionais:
            for i, prof in enumerate(profissionais[:3]):  # Mostrar apenas 3
                print(f"   {i+1}. {prof['nome']} - {prof['especialidade']}")
        
        print()
        
        # 2. Exemplo de criação de agendamento
        print("📅 === EXEMPLO DE AGENDAMENTO ===")
        
        if pacientes and exames and unidades:
            # Usar primeiro paciente, primeiro exame, primeira unidade
            id_paciente = pacientes[0]['id_paciente']
            id_exame = exames[0]['id_exame']
            id_unidade = unidades[0]['id_unidade']
            id_profissional = profissionais[0]['id_profissional'] if profissionais else None
            
            # Data/hora de exemplo (amanhã às 14:00)
            data_hora = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=1)
            
            print(f"Criando agendamento:")
            print(f"  Paciente: {pacientes[0]['nome']}")
            print(f"  Exame: {exames[0]['nome']}")
            print(f"  Unidade: {unidades[0]['endereco']}")
            print(f"  Profissional: {profissionais[0]['nome'] if profissionais else 'Nenhum'}")
            print(f"  Data/Hora: {data_hora.strftime('%d/%m/%Y %H:%M')}")
            
            if model.add_agendamento(id_paciente, id_exame, id_unidade, data_hora, id_profissional):
                print("✅ Agendamento criado com sucesso!")
                
                # Buscar o agendamento recém-criado
                agendamentos = model.get_agendamentos()
                if agendamentos:
                    ultimo_agendamento = agendamentos[-1]  # Último agendamento
                    id_agendamento = ultimo_agendamento['id_agendamento']
                    
                    print(f"   ID do agendamento: {id_agendamento}")
                    print(f"   Status: {ultimo_agendamento['status']}")
                    
                    # 3. Exemplo de atualização de status
                    print()
                    print("🔄 === ATUALIZANDO STATUS PARA REALIZADO ===")
                    
                    if model.update_agendamento_status(id_agendamento, "REALIZADO", True, True):
                        print("✅ Status atualizado para REALIZADO!")
                        
                        # 4. Exemplo de criação de resultado
                        print()
                        print("📋 === CRIANDO RESULTADO ===")
                        
                        resultados_exemplo = f"""
EXAME: {exames[0]['nome']}
PACIENTE: {pacientes[0]['nome']}
DATA: {data_hora.strftime('%d/%m/%Y %H:%M')}

RESULTADOS:
- Parâmetro A: Normal
- Parâmetro B: Dentro dos valores de referência
- Parâmetro C: Ligeiramente elevado (necessita acompanhamento)

OBSERVAÇÕES:
Exame realizado com sucesso. Paciente colaborativo.
Equipamentos funcionando adequadamente.
                        """.strip()
                        
                        recomendacoes_exemplo = """
RECOMENDAÇÕES MÉDICAS:
1. Repetir exame em 30 dias para acompanhamento do Parâmetro C
2. Manter dieta balanceada
3. Praticar exercícios físicos regulares
4. Retorno médico em 15 dias para avaliação

ORIENTAÇÕES:
- Manter medicação atual
- Hidratação adequada
- Evitar jejum prolongado
                        """.strip()
                        
                        if model.add_resultado(id_agendamento, resultados_exemplo, recomendacoes_exemplo):
                            print("✅ Resultado cadastrado com sucesso!")
                            print(f"   Resultados: {len(resultados_exemplo)} caracteres")
                            print(f"   Recomendações: {len(recomendacoes_exemplo)} caracteres")
                        else:
                            print("❌ Erro ao cadastrar resultado")
                    else:
                        print("❌ Erro ao atualizar status")
            else:
                print("❌ Erro ao criar agendamento")
        else:
            print("❌ Dados insuficientes para criar agendamento")
            print("   Verifique se há pacientes, exames e unidades cadastrados")
        
        print()
        
        # 5. Listar agendamentos atuais
        print("📅 === AGENDAMENTOS ATUAIS ===")
        agendamentos = model.get_agendamentos()
        if agendamentos:
            print(f"Total de agendamentos: {len(agendamentos)}")
            for i, agend in enumerate(agendamentos[-5:]):  # Últimos 5
                data_formatada = agend['data_hora'].strftime('%d/%m/%Y %H:%M')
                prof_nome = agend.get('profissional_nome', 'N/A') or 'N/A'
                print(f"   {i+1}. {agend['paciente_nome']} - {agend['exame_nome']}")
                print(f"      Data: {data_formatada} | Status: {agend['status']}")
                print(f"      Profissional: {prof_nome}")
        else:
            print("Nenhum agendamento encontrado")
        
        print()
        
        # 6. Listar resultados
        print("📋 === RESULTADOS CADASTRADOS ===")
        resultados = model.get_resultados()
        if resultados:
            print(f"Total de resultados: {len(resultados)}")
            for i, res in enumerate(resultados[-3:]):  # Últimos 3
                data_formatada = res['data_hora'].strftime('%d/%m/%Y')
                print(f"   {i+1}. {res['paciente_nome']} - {res['exame_nome']}")
                print(f"      Data: {data_formatada}")
                print(f"      Resultados: {res['resultados'][:100]}...")
        else:
            print("Nenhum resultado encontrado")
        
        print()
        
        # 7. Agendamentos realizados sem resultado
        print("🔍 === AGENDAMENTOS SEM RESULTADO ===")
        sem_resultado = model.get_agendamentos_realizados_sem_resultado()
        if sem_resultado:
            print(f"Agendamentos REALIZADOS sem resultado: {len(sem_resultado)}")
            for agend in sem_resultado:
                data_formatada = agend['data_hora'].strftime('%d/%m/%Y %H:%M')
                print(f"   • {agend['paciente_nome']} - {agend['exame_nome']} ({data_formatada})")
        else:
            print("Todos os exames realizados possuem resultado cadastrado")
        
        print()
        print("✅ === Exemplo executado com sucesso! ===")
        print()
        print("💡 Para usar a interface gráfica:")
        print("   python main.py")
        print()
        print("📖 Para mais informações:")
        print("   Consulte o README.md")
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        print("\nDetalhes do erro:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
