"""
Demonstração das Funcionalidades do Sistema
==========================================

Este arquivo demonstra como usar todas as funcionalidades do sistema
de agendamento de exames através de exemplos práticos.
"""

from database import DatabaseConnection
from models import ClinicaModel
from datetime import datetime, date
import json

def demonstrar_conexao():
    """Demonstra como gerenciar a conexão com o banco"""
    print("=== CONEXÃO COM BANCO DE DADOS ===\n")
    
    # Criar instância da conexão
    db = DatabaseConnection()
    
    # Mostrar configuração atual
    print("Configuração atual:")
    print(json.dumps(db.config, indent=2))
    
    # Testar conexão
    print(f"\nTeste de conexão: {'✅ Sucesso' if db.test_connection() else '❌ Falha'}")
    
    # Exemplo de atualização de configuração
    print("\nPara alterar configuração:")
    print("db.update_config('localhost', 'clinica_exames', 'root', 'sua_senha')")

def demonstrar_pacientes():
    """Demonstra operações com pacientes"""
    print("\n=== GESTÃO DE PACIENTES ===\n")
    
    model = ClinicaModel()
    
    # Listar pacientes existentes
    print("📋 Pacientes cadastrados:")
    pacientes = model.get_pacientes()
    if pacientes:
        for i, pac in enumerate(pacientes[:3]):  # Mostrar apenas 3
            empresa = pac.get('empresa_nome', 'Sem empresa')
            print(f"   {i+1}. {pac['nome']} - {pac['cpf']} - {empresa}")
        
        if len(pacientes) > 3:
            print(f"   ... e mais {len(pacientes) - 3} pacientes")
    else:
        print("   Nenhum paciente encontrado")
    
    # Exemplo de busca específica
    if pacientes:
        primeiro_paciente = model.get_paciente_by_id(pacientes[0]['id_paciente'])
        print(f"\n🔍 Detalhes do paciente ID {pacientes[0]['id_paciente']}:")
        print(f"   Nome: {primeiro_paciente['nome']}")
        print(f"   Endereço: {primeiro_paciente['endereco']}")
        print(f"   Data Nasc: {primeiro_paciente['data_nasc']}")
    
    # Exemplo de como adicionar paciente
    print("\n➕ Exemplo de cadastro de paciente:")
    print("""
    model.add_paciente(
        nome="João Silva",
        endereco="Rua das Flores, 123",
        telefone="(53)1234-5678",
        cpf="12345678901",
        data_nasc=date(1990, 5, 15),
        id_empresa=None  # Opcional
    )
    """)

def demonstrar_exames():
    """Demonstra operações com exames"""
    print("\n=== GESTÃO DE EXAMES ===\n")
    
    model = ClinicaModel()
    
    # Listar exames por tipo
    exames = model.get_exames()
    if exames:
        tipos = {}
        for exame in exames:
            tipo = exame['tipo']
            if tipo not in tipos:
                tipos[tipo] = []
            tipos[tipo].append(exame)
        
        print("🔬 Exames por tipo:")
        for tipo, lista in tipos.items():
            print(f"\n   📌 {tipo}:")
            for exame in lista:
                print(f"      • {exame['nome']} ({exame['tempo_estimado']} min)")
    
    # Exemplo de cadastro de exame laboratorial
    print("\n➕ Exemplo de exame LABORATORIAL:")
    print("""
    model.add_exame(
        nome="Hemograma Completo",
        descricao="Análise completa do sangue",
        requisitos="Jejum de 8 horas",
        tempo_estimado=30,
        tipo="LABORATORIAL",
        tempo_coleta_analise=15,
        restricoes_alimentares="Sem álcool 24h antes"
    )
    """)
    
    # Exemplo de cadastro de exame de imagem
    print("\n➕ Exemplo de exame de IMAGEM:")
    print("""
    model.add_exame(
        nome="Ultrassonografia Abdominal",
        descricao="Exame de imagem do abdome",
        requisitos="Bexiga cheia",
        tempo_estimado=45,
        tipo="IMAGEM",
        tecnologia_utilizada="Ultrassom HD",
        preparos_especiais="Ingerir 1L de água 1h antes"
    )
    """)

def demonstrar_agendamentos():
    """Demonstra operações com agendamentos"""
    print("\n=== GESTÃO DE AGENDAMENTOS ===\n")
    
    model = ClinicaModel()
    
    # Mostrar agendamentos recentes
    agendamentos = model.get_agendamentos()
    if agendamentos:
        print("📅 Agendamentos recentes:")
        for i, agend in enumerate(agendamentos[:3]):
            data_hora = agend['data_hora'].strftime('%d/%m/%Y %H:%M')
            status_emoji = {
                'AGENDADO': '🟡',
                'REALIZADO': '✅', 
                'CANCELADO': '❌'
            }.get(agend['status'], '⚪')
            
            print(f"   {i+1}. {status_emoji} {agend['paciente_nome']}")
            print(f"      Exame: {agend['exame_nome']}")
            print(f"      Data: {data_hora}")
            print(f"      Status: {agend['status']}")
            print()
    
    # Exemplo de criação de agendamento
    print("➕ Exemplo de novo agendamento:")
    print("""
    # Primeiro, obtenha os IDs necessários:
    pacientes = model.get_pacientes()
    exames = model.get_exames()
    unidades = model.get_unidades()
    
    # Depois crie o agendamento:
    data_hora = datetime(2024, 8, 15, 9, 30)  # 15/08/2024 às 09:30
    
    model.add_agendamento(
        id_paciente=pacientes[0]['id_paciente'],
        id_exame=exames[0]['id_exame'],
        id_unidade=unidades[0]['id_unidade'],
        data_hora=data_hora,
        id_profissional=None  # Opcional
    )
    """)
    
    # Exemplo de atualização de status
    print("\n✏️ Exemplo de atualização de status:")
    print("""
    model.update_agendamento_status(
        id_agendamento=1,
        status='REALIZADO',
        documentos_ok=True,
        requisitos_ok=True
    )
    """)

def demonstrar_resultados():
    """Demonstra operações com resultados"""
    print("\n=== GESTÃO DE RESULTADOS ===\n")
    
    model = ClinicaModel()
    
    # Mostrar resultados existentes
    resultados = model.get_resultados()
    if resultados:
        print("📋 Resultados cadastrados:")
        for i, res in enumerate(resultados[:2]):
            data = res['data_hora'].strftime('%d/%m/%Y')
            print(f"   {i+1}. {res['paciente_nome']} - {res['exame_nome']}")
            print(f"      Data: {data}")
            print(f"      Resultado: {res['resultados'][:50]}...")
            if res.get('recomendacoes'):
                print(f"      Recomendações: {res['recomendacoes'][:50]}...")
            print()
    
    # Exemplo de cadastro de resultado
    print("➕ Exemplo de cadastro de resultado:")
    print("""
    model.add_resultado(
        id_agendamento=1,
        resultados="Todos os valores dentro da normalidade. "
                  "Hemoglobina: 14.2 g/dL, Leucócitos: 7.500/μL",
        recomendacoes="Manter hábitos saudáveis. "
                     "Retorno em 6 meses para acompanhamento."
    )
    """)

def demonstrar_relatorios():
    """Demonstra os relatórios disponíveis"""
    print("\n=== RELATÓRIOS DISPONÍVEIS ===\n")
    
    model = ClinicaModel()
    
    # Relatório de exames próximos
    print("📅 Exames Próximos (View):")
    exames_proximos = model.get_exames_proximos()
    if exames_proximos:
        for exame in exames_proximos[:3]:
            prioridade_emoji = {
                'URGENTE': '🔴',
                'PRÓXIMO': '🟡',
                'FUTURO': '🟢'
            }.get(exame['prioridade'], '⚪')
            
            data_hora = exame['data_hora'].strftime('%d/%m/%Y %H:%M')
            print(f"   {prioridade_emoji} {exame['prioridade']}: {exame['paciente']}")
            print(f"      {exame['exame']} em {data_hora}")
    else:
        print("   Nenhum exame próximo")
    
    # Relatório por profissional
    print(f"\n👨‍⚕️ Agendamentos por Profissional:")
    por_prof = model.get_agendamentos_por_profissional()
    if por_prof:
        for item in por_prof[:3]:
            print(f"   • {item['profissional']}: {item['total']} agendamentos de {item['exame']}")
    else:
        print("   Nenhum dado disponível")
    
    # Relatório por empresa
    print(f"\n🏢 Pacientes por Empresa:")
    por_empresa = model.get_pacientes_por_empresa()
    if por_empresa:
        empresa_atual = ""
        count = 0
        for item in por_empresa:
            if item['empresa'] != empresa_atual:
                if empresa_atual:  # Se não é a primeira empresa
                    print()
                empresa_atual = item['empresa']
                print(f"   📊 {empresa_atual}:")
                count = 0
            
            count += 1
            if count <= 2:  # Mostrar apenas 2 pacientes por empresa
                print(f"      • {item['paciente']} - {item['cpf']}")
            elif count == 3:
                print("      • ...")
    else:
        print("   Nenhum paciente vinculado a empresas")

def demonstrar_interface():
    """Demonstra como usar a interface gráfica"""
    print("\n=== INTERFACE GRÁFICA ===\n")
    
    print("🖥️ Como executar a interface:")
    print("   python main.py")
    print()
    
    print("🎨 Funcionalidades da interface:")
    print("   • ⚙️ Configuração do banco via interface")
    print("   • 👥 Gestão completa de pacientes")
    print("   • 🔬 Cadastro de exames por tipo")
    print("   • 📅 Criação e controle de agendamentos")
    print("   • 📋 Registro de resultados")
    print("   • 📊 Relatórios em tempo real")
    print()
    
    print("📋 Estrutura da interface:")
    print("   1. Aba Pacientes - CRUD completo")
    print("   2. Aba Exames - Catálogo por tipos")
    print("   3. Aba Agendamentos - Controle de status")
    print("   4. Aba Resultados - Para exames realizados")
    print("   5. Aba Relatórios - Visões gerenciais")
    print()
    
    print("💡 Dicas:")
    print("   • Interface adapta-se automaticamente")
    print("   • Validações em tempo real")
    print("   • Mensagens claras de erro/sucesso")
    print("   • Double-click para editar registros")

def main():
    """Demonstração principal"""
    print("🏥 DEMONSTRAÇÃO DO SISTEMA DE AGENDAMENTO")
    print("=" * 60)
    
    try:
        # Verificar se sistema está configurado
        model = ClinicaModel()
        if not model.test_connection():
            print("❌ Sistema não configurado ou banco indisponível")
            print("   Execute primeiro: python exemplo_uso.py")
            return
        
        # Executar demonstrações
        demonstrar_conexao()
        demonstrar_pacientes()
        demonstrar_exames()
        demonstrar_agendamentos()
        demonstrar_resultados()
        demonstrar_relatorios()
        demonstrar_interface()
        
        print("\n" + "=" * 60)
        print("✅ DEMONSTRAÇÃO CONCLUÍDA")
        print("   Para usar o sistema: python main.py")
        print("   Para testes: python exemplo_uso.py")
        
    except Exception as e:
        print(f"❌ Erro durante demonstração: {e}")
        print("   Verifique se o banco está configurado corretamente")

if __name__ == "__main__":
    main()
