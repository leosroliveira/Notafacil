import streamlit as st
import pandas as pd

# Configuração visual e layout da página
st.set_page_config(page_title="NotaFácil - Controle Escolar", page_icon="🎓", layout="wide")

# Inicializa as listas de dados na sessão do navegador (evita perder dados ao recarregar)
if "lista_alunos" not in st.session_state:
    st.session_state.lista_alunos = [
        {
            "Nome": "Maria Silva",
            "Turma": "9º Ano A",
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
            "Turma": "9º Ano B",
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

# --- MENU NA BARRA LATERAL (SIDEBAR) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=100) # Ícone decorativo acadêmico
st.sidebar.title("NotaFácil v1.0")
menu = st.sidebar.radio(
    "Selecione uma opção:",
    [
        "📋 Cadastro de Alunos", 
        "👩‍🏫 Cadastro de Professores", 
        "📊 Painel de Resultados"
    ]
)

# --- ABA 1: CADASTRO DE ALUNOS ---
if menu == "📋 Cadastro de Alunos":
    st.title("📋 Cadastro de Alunos")
    st.markdown("Insira o nome do aluno, a turma correspondente e adicione suas notas divididas.")

    with st.form(key="form_aluno", clear_on_submit=True):
        col_cad_info = st.columns(2)
        with col_cad_info:
            nome = st.text_input("Nome Completo do Aluno:", placeholder="Ex: Ana Oliveira")
        with col_cad_info:
            turma = st.text_input("Turma:", placeholder="Ex: 9º Ano A")
            
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
        elif not turma.strip():
            st.error("Por favor, preencha a turma do aluno!")
        else:
            # Cálculo automático de soma e média
            notas = [nota1, nota2, nota3, nota4]
            somatorio = sum(notas)
            media = somatorio / len(notas)
            
            # Situação com base na média (Aprovação com 7.0 ou mais)
            situacao = "Aprovado" if media >= 7.0 else "Reprovado"
            
            # Novo registro
            novo_aluno = {
                "Nome": nome.strip(),
                "Turma": turma.strip(),
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

# --- ABA 2: CADASTRO DE PROFESSORES ---
elif menu == "👩‍🏫 Cadastro de Professores":
    st.title("👩‍🏫 Cadastro de Professores")
    st.markdown("Registre novos professores e suas respectivas disciplinas no sistema.")
    
    col_form_prof, col_list_prof = st.columns()
    
    with col_form_prof:
        st.subheader("📝 Novo Cadastro")
        with st.form(key="form_professor", clear_on_submit=True):
            nome_prof = st.text_input("Nome do Professor:", placeholder="Ex: Profa. Adriana Ramos")
            materia_prof = st.text_input("Matéria / Disciplina:", placeholder="Ex: Biologia")
            
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

# --- ABA 3: PAINEL DE RESULTADOS ---
elif menu == "📊 Painel de Resultados":
    st.title("📊 Painel de Resultados")
    st.markdown("Consulte as notas escolares coletivamente ou de forma individualizada por aluno.")
    
    if st.session_state.lista_alunos:
        df_alunos = pd.DataFrame(st.session_state.lista_alunos)
        
        # Filtro de exibição pedido pelo usuário
        tipo_filtro = st.radio(
            "Selecione o modo de exibição:",
            ["Mostrar Todos os Alunos (Tabela Completa)", "Filtrar e Ver Aluno em Separado"],
            horizontal=True
        )
        
        st.markdown("---")
        
        # MODO 1: TABELA COMPLETA
        if tipo_filtro == "Mostrar Todos os Alunos (Tabela Completa)":
            st.subheader("📋 Boletim Geral")
            
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
            
            st.markdown("### 📊 Tabela Geral de Notas")
            st.dataframe(df_alunos, use_container_width=True)
            
            # Gráfico Geral
            st.markdown("### 📈 Comparação Gráfica das Médias")
            st.bar_chart(data=df_alunos, x="Nome", y="Média")
            
            # Exportação
            csv = df_alunos.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Baixar Planilha Consolidada (CSV)",
                data=csv,
                file_name="boletim_escolar_completo.csv",
                mime="text/csv"
            )
            
            if st.button("🗑️ Limpar Todos os Alunos"):
                st.session_state.lista_alunos = []
                st.warning("Lista de alunos apagada.")
                st.rerun()
                
        # MODO 2: VER ALUNO EM SEPARADO
        else:
            st.subheader("🔍 Filtro Individual de Aluno")
            lista_nomes = df_alunos["Nome"].unique()
            aluno_selecionado = st.selectbox("Escolha o aluno para ver o boletim individual:", lista_nomes)
            
            # Filtra os dados do aluno escolhido
            dados_aluno = df_alunos[df_alunos["Nome"] == aluno_selecionado].iloc[0]
            
            # Exibe o Boletim Individual de forma elegante e estruturada
            col_b1, col_b2 = st.columns()
            
            with col_b1:
                st.markdown(f"### 👤 {dados_aluno['Nome']}")
                st.markdown(f"**🏫 Turma:** {dados_aluno['Turma']}")
                
                # Exibe status colorido
                if dados_aluno["Status"] == "Aprovado":
                    st.success(f"🟢 **Status: Aprovado**")
                else:
                    st.error(f"🔴 **Status: Reprovado**")
                
                st.metric("Média Final", f"{dados_aluno['Média']:.2f}")
                st.metric("Soma Total das Notas", f"{dados_aluno['Somatório']:.2f}")
                
            with col_b2:
                st.markdown("### 📊 Notas Detalhadas")
                
                # Criação de métricas pequenas para as 4 notas
                col_n1_i, col_n2_i, col_n3_i, col_n4_i = st.columns(4)
                col_n1_i.metric("Nota 1", dados_aluno["Nota 1"])
                col_n2_i.metric("Nota 2", dados_aluno["Nota 2"])
                col_n3_i.metric("Nota 3", dados_aluno["Nota 3"])
                col_n4_i.metric("Nota 4", dados_aluno["Nota 4"])
                
                # Gráfico individual para o aluno selecionado
                st.markdown("**Desempenho por Avaliação:**")
                df_temp = pd.DataFrame({
                    "Avaliação": ["Nota 1", "Nota 2", "Nota 3", "Nota 4"],
                    "Nota": [dados_aluno["Nota 1"], dados_aluno["Nota 2"], dados_aluno["Nota 3"], dados_aluno["Nota 4"]]
                })
                st.line_chart(data=df_temp, x="Avaliação", y="Nota")
                
    else:
        st.info("Nenhum aluno cadastrado para exibir no painel. Vá até o menu 'Cadastro de Alunos' para adicionar.")
