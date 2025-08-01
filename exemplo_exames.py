#!/usr/bin/env python3
"""
Exemplo de uso da funcionalidade de cadastro de exames
Sistema de Agendamento de Exames - Clínica
"""

from models import ClinicaModel
from datetime import datetime, date
import traceback

def main():
    print("🔬 === Exemplo de Cadastro de Exames ===")
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
        # 1. Mostrar exames existentes
        print("📋 === EXAMES EXISTENTES ===")
        exames_existentes = model.get_exames()
        if exames_existentes:
            print(f"Total de exames: {len(exames_existentes)}")
            for i, exame in enumerate(exames_existentes):
                print(f"   {i+1}. {exame['nome']} ({exame['tipo']}) - {exame['tempo_estimado']}min")
        else:
            print("Nenhum exame encontrado")
        
        print()
        
        # 2. Exemplos de cadastro por tipo
        print("🧪 === CADASTRANDO NOVOS EXAMES ===")
        
        # Exemplo 1: Exame LABORATORIAL
        print("\n1. Cadastrando exame LABORATORIAL...")
        laboratorial_success = model.add_exame(
            nome="Colesterol Total",
            descricao="Dosagem de colesterol total no sangue",
            requisitos="Jejum de 12 horas",
            tempo_estimado=25,
            tipo="LABORATORIAL",
            tempo_coleta_analise=20,
            restricoes_alimentares="Evitar alimentos gordurosos 24h antes do exame"
        )
        
        if laboratorial_success:
            print("   ✅ Exame laboratorial cadastrado com sucesso!")
        else:
            print("   ❌ Erro ao cadastrar exame laboratorial")
        
        # Exemplo 2: Exame IMAGEM
        print("\n2. Cadastrando exame IMAGEM...")
        imagem_success = model.add_exame(
            nome="Tomografia Computadorizada",
            descricao="Exame de imagem por tomografia",
            requisitos="Sem objetos metálicos",
            tempo_estimado=35,
            tipo="IMAGEM",
            tecnologia_utilizada="Tomógrafo Multislice 64",
            preparos_especiais="Jejum de 4 horas. Retirar todos os objetos metálicos."
        )
        
        if imagem_success:
            print("   ✅ Exame de imagem cadastrado com sucesso!")
        else:
            print("   ❌ Erro ao cadastrar exame de imagem")
        
        # Exemplo 3: Exame CLINICO
        print("\n3. Cadastrando exame CLÍNICO...")
        clinico_success = model.add_exame(
            nome="Consulta Neurológica",
            descricao="Avaliação neurológica completa",
            requisitos="Trazer exames neurológicos anteriores",
            tempo_estimado=60,
            tipo="CLINICO",
            tempo_medio_consulta=45,
            especialidade_medica="Neurologia"
        )
        
        if clinico_success:
            print("   ✅ Exame clínico cadastrado com sucesso!")
        else:
            print("   ❌ Erro ao cadastrar exame clínico")
        
        # Exemplo 4: Exame com campos mínimos
        print("\n4. Cadastrando exame com campos mínimos...")
        minimo_success = model.add_exame(
            nome="Teste Rápido",
            descricao=None,
            requisitos=None,
            tempo_estimado=15,
            tipo="LABORATORIAL"
        )
        
        if minimo_success:
            print("   ✅ Exame com campos mínimos cadastrado com sucesso!")
        else:
            print("   ❌ Erro ao cadastrar exame com campos mínimos")
        
        print()
        
        # 3. Listar exames após cadastros
        print("📋 === EXAMES APÓS CADASTROS ===")
        exames_atualizados = model.get_exames()
        if exames_atualizados:
            print(f"Total de exames: {len(exames_atualizados)}")
            print("\nÚltimos exames cadastrados:")
            
            # Mostrar apenas os últimos 5
            for i, exame in enumerate(exames_atualizados[-5:]):
                print(f"\n   📋 {exame['nome']}")
                print(f"      Tipo: {exame['tipo']}")
                print(f"      Tempo: {exame['tempo_estimado']} minutos")
                print(f"      Descrição: {exame['descricao'] or 'N/A'}")
                print(f"      Requisitos: {exame['requisitos'] or 'N/A'}")
                
                # Mostrar campos específicos por tipo
                if exame['tipo'] == 'LABORATORIAL':
                    if exame['tempo_coleta_analise']:
                        print(f"      Tempo Coleta/Análise: {exame['tempo_coleta_analise']} min")
                    if exame['restricoes_alimentares']:
                        print(f"      Restrições: {exame['restricoes_alimentares']}")
                
                elif exame['tipo'] == 'IMAGEM':
                    if exame['tecnologia_utilizada']:
                        print(f"      Tecnologia: {exame['tecnologia_utilizada']}")
                    if exame['preparos_especiais']:
                        print(f"      Preparos: {exame['preparos_especiais']}")
                
                elif exame['tipo'] == 'CLINICO':
                    if exame['tempo_medio_consulta']:
                        print(f"      Tempo Consulta: {exame['tempo_medio_consulta']} min")
                    if exame['especialidade_medica']:
                        print(f"      Especialidade: {exame['especialidade_medica']}")
                
                print(f"      Intervalo Limpeza: {exame['intervalo_limpeza']} min")
        
        print()
        
        # 4. Demonstrar busca por ID
        print("🔍 === TESTANDO BUSCA POR ID ===")
        if exames_atualizados:
            ultimo_exame = exames_atualizados[-1]
            exame_detalhado = model.get_exame_by_id(ultimo_exame['id_exame'])
            
            if exame_detalhado:
                print(f"✅ Exame encontrado: {exame_detalhado['nome']}")
                print(f"   ID: {exame_detalhado['id_exame']}")
                print(f"   Tipo: {exame_detalhado['tipo']}")
            else:
                print("❌ Exame não encontrado")
        
        print()
        
        # 5. Estatísticas por tipo
        print("📊 === ESTATÍSTICAS POR TIPO ===")
        tipos = {}
        for exame in exames_atualizados:
            tipo = exame['tipo']
            if tipo not in tipos:
                tipos[tipo] = {'count': 0, 'tempo_total': 0}
            tipos[tipo]['count'] += 1
            tipos[tipo]['tempo_total'] += exame['tempo_estimado']
        
        for tipo, stats in tipos.items():
            tempo_medio = stats['tempo_total'] / stats['count']
            print(f"   {tipo}: {stats['count']} exames (tempo médio: {tempo_medio:.1f} min)")
        
        print()
        
        # 6. Validações e erros comuns
        print("⚠️  === TESTANDO VALIDAÇÕES ===")
        
        # Teste com nome vazio
        print("Testando nome vazio...")
        erro1 = model.add_exame("", "desc", "req", 30, "LABORATORIAL")
        print(f"   Resultado: {'❌ Rejeitado corretamente' if not erro1 else '✅ Aceito (inesperado)'}")
        
        # Teste com tempo inválido  
        print("Testando tempo negativo...")
        erro2 = model.add_exame("Teste Inválido", "desc", "req", -10, "LABORATORIAL")
        print(f"   Resultado: {'❌ Rejeitado corretamente' if not erro2 else '✅ Aceito (inesperado)'}")
        
        print()
        print("✅ === Exemplo de cadastro de exames executado com sucesso! ===")
        print()
        print("💡 Para usar a interface gráfica:")
        print("   python main.py")
        print("   → Vá para a aba 'Exames'")
        print("   → Clique em '➕ Novo Exame'")
        print()
        print("🎯 Funcionalidades demonstradas:")
        print("   ✅ Cadastro de exames LABORATORIAL, IMAGEM e CLÍNICO")
        print("   ✅ Campos específicos por tipo de exame")
        print("   ✅ Campos opcionais e obrigatórios")
        print("   ✅ Busca de exames por ID")
        print("   ✅ Listagem completa de exames")
        print("   ✅ Validações de entrada")
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        print("\nDetalhes do erro:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
