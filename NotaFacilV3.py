import streamlit as st
import pandas as pd

# Configuração visual e layout da página
st.set_page_config(page_title="Controle Escolar - NotaFácil", page_icon="🎓", layout="wide")

# Inicializa as listas de dados na sessão do navegador
if "lista_alunos" not in st.session_state:
    st.session_state.lista_alunos = [
        {
            "Nome": "Maria Silva",
            "Turma": "9º Ano",
            "Nota 1": 8.5,
            "Nota 2": 7.0,
            "Nota 3": 9.0,
            "Nota 4": 8.0,
            "Somatório": 32.5,
            "Média": 8.13,
            "Status": "Aprovado"
        },
        {
            "Nome": "João Souza",
            "Turma": "8º Ano",
            "Nota 1": 5.0,
            "Nota 2": 6.0,
            "Nota 3": 4.5,
            "Nota 4": 6.5,
            "Somatório": 22.0,
            "Média": 5.5,
            "Status": "Reprovado"
        }
    ]

if "lista_professores" not in st.session_state:
    st.session_state.lista_professores = [
        {
            "Nome": "Fernanda Lima",
            "Matéria": "Matemática"
        },
        {
            "Nome": "Roberto Alencar",
            "Matéria": "História"
        }
    ]

# Lista de opções de turma (do 1º ao 9º Ano)
OPCOES_TURMAS = [f"{i}º Ano" for i in range(1, 10)]

# --- MENU NA BARRA LATERAL (SIDEBAR) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=100) # Ícone decorativo acadêmico
st.sidebar.title("NotaFácil V3")
menu = st.sidebar.radio(
    "Selecione uma opção:",
    [
        "📋 Cadastrar Aluno", 
        "✏️ Editar Alunos",
        "👩‍🏫 Cadastrar Professor", 
        "🔍 Visualizar Aluno (Boletim)",
        "📊 Painel Geral (Resultados)"
    ]
)

# --- ABA 1: CADASTRO DE ALUNOS ---
if menu == "📋 Cadastrar Aluno":
    st.title("📋 Cadastrar Novo Aluno")
    st.markdown("Insira o nome do aluno, selecione a turma (1º ao 9º Ano) e adicione suas notas divididas.")

    with st.form(key="form_aluno", clear_on_submit=True):
        col_cad_info_1, col_cad_info_2 = st.columns(2)
        with col_cad_info_1:
            nome = st.text_input("Nome Completo do Aluno:", placeholder="Ex: Ana Oliveira")
        with col_cad_info_2:
            turma = st.selectbox("Turma (Ano Escolar):", OPCOES_TURMAS)
            
        st.markdown("### 📝 Notas Divididas")
        col_n1, col_n2 = st.columns(2)
        col_n3, col_n4 = st.columns(2)
        
        with col_n1:
            nota1 = st.number_input("Nota 1:", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        with col_n2:
            nota2 = st.number_input("Nota 2:", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        with col_n3:
            nota3 = st.number_input("Nota 3:", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        with col_n4:
            nota4 = st.number_input("Nota 4:", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        
        submeter_aluno = st.form_submit_button("💾 Salvar Aluno")
        
    if submeter_aluno:
        if not nome.strip():
            st.error("Por favor, preencha o nome do aluno!")
        else:
            # Cálculo automático de soma e média
            notas = [nota1, nota2, nota3, nota4]
            somatorio = sum(notas)
            media = somatorio / len(notas)
            
            # Situação com base na média
            situacao = "Aprovado" if media >= 7.0 else "Reprovado"
            
            # Novo registro
            novo_aluno = {
                "Nome": nome.strip(),
                "Turma": turma,
                "Nota 1": nota1,
                "Nota 2": nota2,
                "Nota 3": nota3,
                "Nota 4": nota4,
                "Somatório": round(somatorio, 2),
                "Média": round(media, 2),
                "Status": situacao
            }
            
            st.session_state.lista_alunos.append(novo_aluno)
            st.success(f"🎉 Aluno **{nome}** da turma **{turma}** cadastrado com sucesso!")

# --- ABA 2: EDITAR ALUNOS ---
elif menu == "✏️ Editar Alunos":
    st.title("✏️ Editar Alunos")
    st.markdown("Escolha um aluno específico para editar seus dados ou utilize a tabela interativa abaixo para realizar edições rápidas.")
    
    if st.session_state.lista_alunos:
        # Método 1: Edição por formulário (Mais seguro e detalhado)
        st.subheader("🔍 Selecione o Aluno para Editar")
        nomes_alunos = [aluno["Nome"] for aluno in st.session_state.lista_alunos]
        aluno_selecionado = st.selectbox("Escolha o aluno:", nomes_alunos)
        
        # Encontra o índice do aluno na lista da sessão
        idx_aluno = next(i for i, aluno in enumerate(st.session_state.lista_alunos) if aluno["Nome"] == aluno_selecionado)
        aluno_dados = st.session_state.lista_alunos[idx_aluno]
        
        # Garante que a turma do aluno esteja nas opções, se não estiver, adicionamos
        turma_atual = aluno_dados.get("Turma", "1º Ano")
        if turma_atual not in OPCOES_TURMAS:
            index_turma = 0
        else:
            index_turma = OPCOES_TURMAS.index(turma_atual)
            
        with st.form(key="form_edicao_aluno"):
            col_ed_1, col_ed_2 = st.columns(2)
            with col_ed_1:
                novo_nome = st.text_input("Nome Completo:", value=aluno_dados["Nome"])
            with col_ed_2:
                nova_turma = st.selectbox("Turma (Ano Escolar):", OPCOES_TURMAS, index=index_turma)
                
            st.markdown("### 📝 Notas Divididas")
            col_en1, col_en2 = st.columns(2)
            col_en3, col_en4 = st.columns(2)
            
            with col_en1:
                nova_nota1 = st.number_input("Nota 1:", min_value=0.0, max_value=10.0, value=float(aluno_dados["Nota 1"]), step=0.1)
            with col_en2:
                nova_nota2 = st.number_input("Nota 2:", min_value=0.0, max_value=10.0, value=float(aluno_dados["Nota 2"]), step=0.1)
            with col_en3:
                nova_nota3 = st.number_input("Nota 3:", min_value=0.0, max_value=10.0, value=float(aluno_dados["Nota 3"]), step=0.1)
            with col_en4:
                nova_nota4 = st.number_input("Nota 4:", min_value=0.0, max_value=10.0, value=float(aluno_dados["Nota 4"]), step=0.1)
                
            col_btns = st.columns([1, 1, 4])
            with col_btns[0]:
                salvar_edicao = st.form_submit_button("💾 Salvar")
            with col_btns[1]:
                excluir_aluno = st.form_submit_button("🗑️ Excluir Aluno")
                
        if salvar_edicao:
            if not novo_nome.strip():
                st.error("O nome não pode ficar vazio!")
            else:
                # Recalcula soma, média e situação
                novas_notas = [nova_nota1, nova_nota2, nova_nota3, nova_nota4]
                novo_somatorio = sum(novas_notas)
                nova_media = novo_somatorio / len(novas_notas)
                nova_situacao = "Aprovado" if nova_media >= 7.0 else "Reprovado"
                
                # Atualiza na sessão
                st.session_state.lista_alunos[idx_aluno] = {
                    "Nome": novo_nome.strip(),
                    "Turma": nova_turma,
                    "Nota 1": nova_nota1,
                    "Nota 2": nova_nota2,
                    "Nota 3": nova_nota3,
                    "Nota 4": nova_nota4,
                    "Somatório": round(novo_somatorio, 2),
                    "Média": round(nova_media, 2),
                    "Status": nova_situacao
                }
                st.success(f"Alterações para **{novo_nome}** salvas com sucesso!")
                st.rerun()
                
        if excluir_aluno:
            st.session_state.lista_alunos.pop(idx_aluno)
            st.success(f"Aluno **{aluno_selecionado}** excluído com sucesso!")
            st.rerun()

        st.markdown("---")
        
        # Método 2: Edição em lote (Planilha Interativa)
        st.subheader("📊 Edição Rápida via Planilha")
        st.markdown("Dica: Você pode dar duplo clique em qualquer célula de Nome, Turma ou Notas na tabela abaixo para editar diretamente!")
        
        df_editavel = pd.DataFrame(st.session_state.lista_alunos)
        
        # Usamos o st.data_editor para permitir alterações diretas na tabela de uma vez
        edited_df = st.data_editor(
            df_editavel,
            use_container_width=True,
            disabled=["Somatório", "Média", "Status"], # Desabilita as colunas automáticas
            column_config={
                "Turma": st.column_config.SelectboxColumn(
                    "Turma",
                    help="Selecione o ano escolar",
                    width="medium",
                    options=OPCOES_TURMAS,
                    required=True,
                )
            }
        )
        
        if st.button("💾 Salvar Alterações da Tabela"):
            # Recalcula somatório e média para cada linha modificada
            nova_lista_alunos = []
            for _, row in edited_df.iterrows():
                try:
                    n1 = float(row["Nota 1"])
                    n2 = float(row["Nota 2"])
                    n3 = float(row["Nota 3"])
                    n4 = float(row["Nota 4"])
                except:
                    n1 = n2 = n3 = n4 = 0.0
                    
                soma = n1 + n2 + n3 + n4
                media = soma / 4.0
                status = "Aprovado" if media >= 7.0 else "Reprovado"
                
                nova_lista_alunos.append({
                    "Nome": str(row["Nome"]).strip(),
                    "Turma": row["Turma"],
                    "Nota 1": round(n1, 2),
                    "Nota 2": round(n2, 2),
                    "Nota 3": round(n3, 2),
                    "Nota 4": round(n4, 2),
                    "Somatório": round(soma, 2),
                    "Média": round(media, 2),
                    "Status": status
                })
            
            st.session_state.lista_alunos = nova_lista_alunos
            st.success("Tabela de alunos atualizada e salva!")
            st.rerun()
            
    else:
        st.info("Nenhum aluno cadastrado para editar. Vá para a aba de Cadastro primeiro.")

# --- ABA 3: CADASTRO DE PROFESSORES ---
elif menu == "👩‍🏫 Cadastrar Professor":
    st.title("👩‍🏫 Cadastro de Professores")
    st.markdown("Registre novos professores e suas respectivas disciplinas no sistema.")
    
    col_form_prof, col_list_prof = st.columns(2)
    
    with col_form_prof:
        st.subheader("📝 Novo Cadastro")
        with st.form(key="form_professor", clear_on_submit=True):
            nome_prof = st.text_input("Nome do Professor:", placeholder="Ex: Profa. Adriana Ramos")
            materia_prof = st.text_input("Matéria / Disciplina:", placeholder="Ex: Biologia, Geografia...")
            
            submeter_prof = st.form_submit_button("💾 Salvar Professor")
            
        if submeter_prof:
            if not nome_prof.strip():
                st.error("Por favor, digite o nome do professor!")
            elif not materia_prof.strip():
                st.error("Por favor, digite a matéria que este professor leciona!")
            else:
                novo_professor = {
                    "Nome": nome_prof.strip(),
                    "Matéria": materia_prof.strip()
                }
                st.session_state.lista_professores.append(novo_professor)
                st.success(f"🎉 Professor(a) **{nome_prof}** cadastrado(a) para **{materia_prof}** com sucesso!")
                st.rerun()

    with col_list_prof:
        st.subheader("📋 Professores Cadastrados")
        if st.session_state.lista_professores:
            df_prof = pd.DataFrame(st.session_state.lista_professores)
            st.dataframe(df_prof, use_container_width=True)
            
            if st.button("🗑️ Limpar Todos os Professores"):
                st.session_state.lista_professores = []
                st.warning("Lista de professores esvaziada.")
                st.rerun()
        else:
            st.info("Nenhum professor cadastrado.")

# --- ABA 4: VISUALIZAR ALUNO EM SEPARADO (BOLETIM INDIVIDUAL) ---
elif menu == "🔍 Visualizar Aluno (Boletim)":
    st.title("🔍 Boletim e Visualização Individual")
    st.markdown("Selecione um aluno na caixa abaixo para visualizar suas informações, notas e gráficos de desempenho de forma clara.")
    
    if st.session_state.lista_alunos:
        df_alunos = pd.DataFrame(st.session_state.lista_alunos)
        
        # Caixa clara de seleção de alunos
        lista_nomes = df_alunos["Nome"].unique()
        aluno_selecionado = st.selectbox("👉 Escolha o aluno para carregar o boletim detalhado:", lista_nomes)
        
        st.markdown("---")
        
        # Filtra os dados do aluno escolhido e converte em Series usando .iloc[0] para evitar erros de indexação
        dados_aluno = df_alunos[df_alunos["Nome"] == aluno_selecionado].iloc[0]
        
        # Exibe o Boletim Individual de forma elegante e estruturada
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            st.markdown(f"## 👤 {dados_aluno['Nome']}")
            st.markdown(f"### 🏫 Turma: **{dados_aluno['Turma']}**")
            
            # Exibe status colorido
            if dados_aluno["Status"] == "Aprovado":
                st.success(f"🟢 **Status: Aprovado**")
            else:
                st.error(f"🔴 **Status: Reprovado**")
            
            # Métricas grandes
            st.markdown("---")
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.metric(label="🎓 Média Final", value=f"{dados_aluno['Média']:.2f}")
            with col_met2:
                st.metric(label="➕ Somatório Total", value=f"{dados_aluno['Somatório']:.2f}")
            
        with col_b2:
            st.markdown("### 📊 Notas Detalhadas")
            
            # Criação de métricas pequenas para as 4 notas
            col_n1_i, col_n2_i, col_n3_i, col_n4_i = st.columns(4)
            col_n1_i.metric("Nota 1", f"{dados_aluno['Nota 1']:.1f}")
            col_n2_i.metric("Nota 2", f"{dados_aluno['Nota 2']:.1f}")
            col_n3_i.metric("Nota 3", f"{dados_aluno['Nota 3']:.1f}")
            col_n4_i.metric("Nota 4", f"{dados_aluno['Nota 4']:.1f}")
            
            st.markdown("---")
            # Gráfico individual para o aluno selecionado
            st.markdown("**📉 Curva de Desempenho por Avaliação:**")
            df_temp = pd.DataFrame({
                "Avaliação": ["Nota 1", "Nota 2", "Nota 3", "Nota 4"],
                "Nota": [dados_aluno["Nota 1"], dados_aluno["Nota 2"], dados_aluno["Nota 3"], dados_aluno["Nota 4"]]
            })
            st.line_chart(data=df_temp, x="Avaliação", y="Nota")
            
    else:
        st.info("Nenhum aluno cadastrado no momento. Acesse '📋 Cadastrar Aluno' para registrar os dados.")

# --- ABA 5: PAINEL GERAL DE RESULTADOS (LISTAGEM INTEIRA) ---
elif menu == "📊 Painel Geral (Resultados)":
    st.title("📊 Painel Geral e Listagem Inteira")
    st.markdown("Consulte as estatísticas coletivas da escola, baixe planilhas e confira a tabela geral com todos os registros.")
    
    if st.session_state.lista_alunos:
        df_alunos = pd.DataFrame(st.session_state.lista_alunos)
        
        # Estatísticas da Turma
        total_alunos = len(df_alunos)
        media_geral = df_alunos["Média"].mean()
        aprovados = len(df_alunos[df_alunos["Status"] == "Aprovado"])
        
        col_st1, col_st2, col_st3 = st.columns(3)
        with col_st1:
            st.metric("Total de Alunos", total_alunos)
        with col_st2:
            st.metric("Média Geral do Colégio", f"{media_geral:.2f}")
        with col_st3:
            st.metric("Aprovados", f"{aprovados} ({aprovados/total_alunos*100:.0f}%)")
        
        st.markdown("---")
        
        st.subheader("📋 Tabela Geral de Notas")
        st.dataframe(df_alunos, use_container_width=True)
        
        # Gráfico Geral
        st.markdown("### 📈 Comparação Gráfica das Médias")
        st.bar_chart(data=df_alunos, x="Nome", y="Média")
        
        # Exportação
        st.markdown("### ⚙️ Opções Adicionais")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            csv = df_alunos.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Baixar Planilha Completa (CSV)",
                data=csv,
                file_name="boletim_escolar_completo.csv",
                mime="text/csv"
            )
        with col_btn2:
            if st.button("🗑️ Limpar Todos os Alunos"):
                st.session_state.lista_alunos = []
                st.warning("Lista de alunos apagada.")
                st.rerun()
                
    else:
        st.info("Nenhum aluno cadastrado no momento. Acesse '📋 Cadastrar Aluno' para registrar os dados.")
