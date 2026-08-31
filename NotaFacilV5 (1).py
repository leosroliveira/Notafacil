import streamlit as st
import pandas as pd
import sqlite3
import os

# Configuração visual e layout da página
st.set_page_config(page_title="Controle Escolar - NotaFácil", page_icon="🎓", layout="wide")

DB_FILE = "notafacil.db"

# --- FUNÇÕES DE BANCO DE DADOS (SQLITE) ---
def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        turma TEXT NOT NULL,
        nota1 REAL,
        nota2 REAL,
        nota3 REAL,
        nota4 REAL,
        somatorio REAL,
        media REAL,
        status TEXT
    )
    """)
    
    # Verifica se deve inserir alunos padrão
    cursor.execute("SELECT COUNT(*) FROM alunos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO alunos (nome, turma, nota1, nota2, nota3, nota4, somatorio, media, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ("Maria Silva", "9º Ano", 8.5, 7.0, 9.0, 8.0, 32.5, 8.13, "Aprovado"))
        cursor.execute("""
        INSERT INTO alunos (nome, turma, nota1, nota2, nota3, nota4, somatorio, media, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ("João Souza", "8º Ano", 5.0, 6.0, 0.0, 0.0, 11.0, 5.5, "Reprovado"))
    conn.commit()
    conn.close()

# Executa inicialização
init_db()

def get_alunos():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM alunos", conn)
    conn.close()
    return df

# --- LÓGICA DE MÉDIA DINÂMICA (APENAS NOTAS DIFERENTES DE ZERO) ---
def calcular_soma_media_status(n1, n2, n3, n4):
    notas = [n1, n2, n3, n4]
    # Considera apenas notas preenchidas e diferentes de zero
    notas_validas = [n for n in notas if n != 0.0 and n is not None]
    
    if not notas_validas:
        return 0.0, 0.0, "Reprovado"
    
    somatorio = sum(notas_validas)
    media = somatorio / len(notas_validas)
    status = "Aprovado" if media >= 7.0 else "Reprovado"
    return round(somatorio, 2), round(media, 2), status

# Lista de turmas padrão do 1º ao 9º Ano
OPCOES_TURMAS = [f"{i}º Ano" for i in range(1, 10)]

# --- BARRA LATERAL (SIDEBAR) ---
# Identificação personalizada da Professora Rebeca Carvalho com imagem
st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if os.path.exists("professora_loira.png"):
    st.sidebar.image("professora_loira.png", use_container_width=True)
else:
    # Fallback caso a imagem não esteja no diretório de execução
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=120)

st.sidebar.markdown("<h3 style='text-align: center; color: #4F8BF9; margin-bottom: 5px;'>Prof.ª REBECA CARVALHO</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-style: italic; color: #888;'>Língua Portuguesa & Literatura</p>", unsafe_allow_html=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.title("Menu de Navegação")
menu = st.sidebar.radio(
    "Selecione uma opção:",
    [
        "📋 Cadastrar Aluno", 
        "✏️ Editar Alunos",
        "🔍 Visualizar Aluno (Boletim)",
        "📊 Painel Geral (Resultados)"
    ]
)

# --- ABA 1: CADASTRAR ALUNO ---
if menu == "📋 Cadastrar Aluno":
    st.title("📋 Cadastrar Novo Aluno")
    st.markdown("""
    Insira o nome do aluno, selecione a turma (1º ao 9º Ano) e adicione as notas.
    
    💡 **Nota:** O sistema calcula a média utilizando **apenas as notas preenchidas (maiores que zero)**. 
    Se você preencher apenas duas notas e deixar as outras como zero, a média será a divisão por 2.
    """)

    with st.form(key="form_aluno", clear_on_submit=True):
        col_cad_1, col_cad_2 = st.columns(2)
        with col_cad_1:
            nome = st.text_input("Nome Completo do Aluno:", placeholder="Ex: Carlos Henrique")
        with col_cad_2:
            turma = st.selectbox("Turma (Ano Escolar):", OPCOES_TURMAS)
            
        st.markdown("### 📝 Notas Divididas")
        col_n1, col_n2 = st.columns(2)
        col_n3, col_n4 = st.columns(2)
        
        with col_n1:
            nota1 = st.number_input("Nota 1:", min_value=0.0, max_value=10.0, value=0.0, step=0.1, help="Deixe 0.0 se não aplicada ainda")
        with col_n2:
            nota2 = st.number_input("Nota 2:", min_value=0.0, max_value=10.0, value=0.0, step=0.1, help="Deixe 0.0 se não aplicada ainda")
        with col_n3:
            nota3 = st.number_input("Nota 3:", min_value=0.0, max_value=10.0, value=0.0, step=0.1, help="Deixe 0.0 se não aplicada ainda")
        with col_n4:
            nota4 = st.number_input("Nota 4:", min_value=0.0, max_value=10.0, value=0.0, step=0.1, help="Deixe 0.0 se não aplicada ainda")
        
        submeter_aluno = st.form_submit_button("💾 Salvar no Banco de Dados")
        
    if submeter_aluno:
        if not nome.strip():
            st.error("Por favor, preencha o nome do aluno!")
        else:
            soma, media, status = calcular_soma_media_status(nota1, nota2, nota3, nota4)
            
            # Salva no SQLite
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO alunos (nome, turma, nota1, nota2, nota3, nota4, somatorio, media, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome.strip(), turma, nota1, nota2, nota3, nota4, soma, media, status))
            conn.commit()
            conn.close()
            
            st.success(f"🎉 Aluno **{nome}** cadastrado e salvo com sucesso no Banco de Dados!")

# --- ABA 2: EDITAR ALUNOS ---
elif menu == "✏️ Editar Alunos":
    st.title("✏️ Editar Alunos")
    st.markdown("Edite as notas e nomes individualmente ou diretamente usando a tabela interativa. Tudo é salvo permanentemente.")
    
    df_alunos = get_alunos()
    
    if not df_alunos.empty:
        # Método 1: Edição por formulário
        st.subheader("🔍 Selecione o Aluno para Editar")
        
        # Cria identificador único (nome + turma) usando colunas em minúsculo para evitar KeyError
        df_alunos["Identificador"] = df_alunos["nome"] + " (" + df_alunos["turma"] + ")"
        identificadores = df_alunos["Identificador"].tolist()
        aluno_selecionado = st.selectbox("Escolha o aluno:", identificadores)
        
        # Obtém o id correspondente do aluno
        aluno_dados = df_alunos[df_alunos["Identificador"] == aluno_selecionado].iloc[0]
        id_aluno = int(aluno_dados["id"])
        
        # Define índice inicial da turma na lista
        turma_atual = aluno_dados["turma"]
        index_turma = OPCOES_TURMAS.index(turma_atual) if turma_atual in OPCOES_TURMAS else 0
            
        with st.form(key="form_edicao_aluno"):
            col_ed_1, col_ed_2 = st.columns(2)
            with col_ed_1:
                novo_nome = st.text_input("Nome Completo:", value=aluno_dados["nome"])
            with col_ed_2:
                nova_turma = st.selectbox("Turma (Ano Escolar):", OPCOES_TURMAS, index=index_turma)
                
            st.markdown("### 📝 Notas Divididas")
            col_en1, col_en2 = st.columns(2)
            col_en3, col_en4 = st.columns(2)
            
            with col_en1:
                nova_nota1 = st.number_input("Nota 1:", min_value=0.0, max_value=10.0, value=float(aluno_dados["nota1"]), step=0.1)
            with col_en2:
                nova_nota2 = st.number_input("Nota 2:", min_value=0.0, max_value=10.0, value=float(aluno_dados["nota2"]), step=0.1)
            with col_en3:
                nova_nota3 = st.number_input("Nota 3:", min_value=0.0, max_value=10.0, value=float(aluno_dados["nota3"]), step=0.1)
            with col_en4:
                nova_nota4 = st.number_input("Nota 4:", min_value=0.0, max_value=10.0, value=float(aluno_dados["nota4"]), step=0.1)
                
            col_btns_1, col_btns_2 = st.columns(2)
            with col_btns_1:
                salvar_edicao = st.form_submit_button("💾 Salvar Alterações")
            with col_btns_2:
                excluir_aluno = st.form_submit_button("🗑️ Excluir Aluno")
                
        if salvar_edicao:
            if not novo_nome.strip():
                st.error("O nome não pode ficar vazio!")
            else:
                # Recalcula soma, média e situação (ignorando zeros)
                novo_somatorio, nova_media, nova_situacao = calcular_soma_media_status(nova_nota1, nova_nota2, nova_nota3, nova_nota4)
                
                # Salva no banco
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE alunos
                    SET nome=?, turma=?, nota1=?, nota2=?, nota3=?, nota4=?, somatorio=?, media=?, status=?
                    WHERE id=?
                """, (novo_nome.strip(), nova_turma, nova_nota1, nova_nota2, nova_nota3, nova_nota4, novo_somatorio, nova_media, nova_situacao, id_aluno))
                conn.commit()
                conn.close()
                
                st.success(f"Alterações para **{novo_nome}** salvas no Banco de Dados!")
                st.rerun()
                
        if excluir_aluno:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alunos WHERE id=?", (id_aluno,))
            conn.commit()
            conn.close()
            st.success(f"Aluno **{aluno_dados['nome']}** excluído do Banco de Dados com sucesso!")
            st.rerun()

        st.markdown("---")
        
        # Método 2: Edição direta na Planilha (st.data_editor)
        st.subheader("📊 Edição Direta via Planilha")
        st.markdown("Você também pode alterar valores dando **duplo clique** na tabela abaixo e depois clicar em salvar.")
        
        # Prepara dataframe para edição
        df_editor = df_alunos[["id", "nome", "turma", "nota1", "nota2", "nota3", "nota4", "somatorio", "media", "status"]].copy()
        df_editor.columns = ["ID", "Nome", "Turma", "Nota 1", "Nota 2", "Nota 3", "Nota 4", "Somatório (Automático)", "Média (Automática)", "Status"]
        
        edited_df = st.data_editor(
            df_editor,
            use_container_width=True,
            disabled=["ID", "Somatório (Automático)", "Média (Automática)", "Status"],
            column_config={
                "Turma": st.column_config.SelectboxColumn(
                    "Turma",
                    options=OPCOES_TURMAS,
                    required=True,
                )
            }
        )
        
        if st.button("💾 Salvar Alterações da Tabela"):
            conn = get_db_connection()
            cursor = conn.cursor()
            for _, row in edited_df.iterrows():
                try:
                    n1 = float(row["Nota 1"])
                    n2 = float(row["Nota 2"])
                    n3 = float(row["Nota 3"])
                    n4 = float(row["Nota 4"])
                except ValueError:
                    n1 = n2 = n3 = n4 = 0.0
                    
                soma, media, status = calcular_soma_media_status(n1, n2, n3, n4)
                
                cursor.execute("""
                    UPDATE alunos
                    SET nome=?, turma=?, nota1=?, nota2=?, nota3=?, nota4=?, somatorio=?, media=?, status=?
                    WHERE id=?
                """, (str(row["Nome"]).strip(), row["Turma"], n1, n2, n3, n4, soma, media, status, int(row["ID"])))
            conn.commit()
            conn.close()
            st.success("Todas as edições da tabela foram salvas com recálculo automático!")
            st.rerun()
            
    else:
        st.info("Nenhum aluno cadastrado no momento. Acesse '📋 Cadastrar Aluno' para registrar os dados.")

# --- ABA 3: VISUALIZAR ALUNO EM SEPARADO (BOLETIM) ---
elif menu == "🔍 Visualizar Aluno (Boletim)":
    st.title("🔍 Boletim Individual")
    st.markdown("Escolha um aluno abaixo para carregar seu boletim escolar completo, notas e desempenho gráfico.")
    
    df_alunos = get_alunos()
    if not df_alunos.empty:
        # Identificador exclusivo de alunos
        df_alunos["Identificador"] = df_alunos["nome"] + " (" + df_alunos["turma"] + ")"
        lista_nomes = df_alunos["Identificador"].unique()
        aluno_selecionado = st.selectbox("👉 Escolha o aluno para ver o boletim:", lista_nomes)
        
        st.markdown("---")
        
        # Filtra os dados do aluno escolhido e converte em Series usando .iloc[0]
        dados_aluno = df_alunos[df_alunos["Identificador"] == aluno_selecionado].iloc[0]
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            st.markdown(f"## 👤 {dados_aluno['nome']}")
            st.markdown(f"### 🏫 Turma: **{dados_aluno['turma']}**")
            
            # Exibe status colorido
            if dados_aluno["status"] == "Aprovado":
                st.success(f"🟢 **Status: Aprovado**")
            else:
                st.error(f"🔴 **Status: Reprovado**")
            
            # Métricas grandes
            st.markdown("---")
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.metric(label="🎓 Média de Notas Ativas", value=f"{dados_aluno['media']:.2f}")
            with col_met2:
                st.metric(label="➕ Somatório Total", value=f"{dados_aluno['somatorio']:.2f}")
                
            st.info("💡 **Atenção:** Média calculada dinamicamente desconsiderando notas zeradas.")
            
        with col_b2:
            st.markdown("### 📊 Notas Detalhadas")
            
            # Notas
            col_n1_i, col_n2_i, col_n3_i, col_n4_i = st.columns(4)
            col_n1_i.metric("Nota 1", f"{dados_aluno['nota1']:.1f}")
            col_n2_i.metric("Nota 2", f"{dados_aluno['nota2']:.1f}")
            col_n3_i.metric("Nota 3", f"{dados_aluno['nota3']:.1f}")
            col_n4_i.metric("Nota 4", f"{dados_aluno['nota4']:.1f}")
            
            st.markdown("---")
            # Gráfico de evolução de desempenho
            st.markdown("**📉 Evolução por Avaliação:**")
            
            # Filtra notas de interesse (apenas as maiores que zero para plotar evolução real)
            avaliacoes = []
            notas_plot = []
            if dados_aluno['nota1'] > 0:
                avaliacoes.append("Nota 1")
                notas_plot.append(dados_aluno['nota1'])
            if dados_aluno['nota2'] > 0:
                avaliacoes.append("Nota 2")
                notas_plot.append(dados_aluno['nota2'])
            if dados_aluno['nota3'] > 0:
                avaliacoes.append("Nota 3")
                notas_plot.append(dados_aluno['nota3'])
            if dados_aluno['nota4'] > 0:
                avaliacoes.append("Nota 4")
                notas_plot.append(dados_aluno['nota4'])
                
            if avaliacoes:
                df_temp = pd.DataFrame({
                    "Avaliação": avaliacoes,
                    "Nota": notas_plot
                })
                st.line_chart(data=df_temp, x="Avaliação", y="Nota")
            else:
                st.warning("Nenhuma nota lançada para este aluno ainda.")
                
    else:
        st.info("Nenhum aluno cadastrado no momento. Acesse '📋 Cadastrar Aluno' para registrar os dados.")

# --- ABA 4: PAINEL GERAL (RESULTADOS) ---
elif menu == "📊 Painel Geral (Resultados)":
    st.title("📊 Painel Geral de Resultados")
    st.markdown("Visualize dados consolidados de toda a escola, médias globais e faça o download de planilhas.")
    
    df_alunos = get_alunos()
    if not df_alunos.empty:
        # Estatísticas da Turma
        total_alunos = len(df_alunos)
        media_geral = df_alunos["media"].mean()
        aprovados = len(df_alunos[df_alunos["status"] == "Aprovado"])
        
        col_st1, col_st2, col_st3 = st.columns(3)
        with col_st1:
            st.metric("Total de Alunos", total_alunos)
        with col_st2:
            st.metric("Média Geral Escolar", f"{media_geral:.2f}")
        with col_st3:
            st.metric("Aprovados", f"{aprovados} ({aprovados/total_alunos*100:.0f}%)")
        
        st.markdown("---")
        
        st.subheader("📋 Tabela Geral de Notas")
        # Renomeia colunas para ficar profissional
        df_exibicao = df_alunos[["nome", "turma", "nota1", "nota2", "nota3", "nota4", "somatorio", "media", "status"]].copy()
        df_exibicao.columns = ["Nome", "Turma", "Nota 1", "Nota 2", "Nota 3", "Nota 4", "Somatório", "Média", "Status"]
        st.dataframe(df_exibicao, use_container_width=True)
        
        # Gráfico Geral
        st.markdown("### 📈 Comparação Gráfica das Médias")
        st.bar_chart(data=df_exibicao, x="Nome", y="Média")
        
        # Exportação
        st.markdown("### ⚙️ Opções de Exportação")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            csv = df_exibicao.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Baixar Planilha Consolidada (CSV)",
                data=csv,
                file_name="boletim_escolar_completo.csv",
                mime="text/csv"
            )
        with col_btn2:
            if st.button("🗑️ Resetar Banco de Dados (Excluir Alunos)"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM alunos")
                conn.commit()
                conn.close()
                st.warning("Todos os alunos foram excluídos.")
                st.rerun()
                
    else:
        st.info("Nenhum aluno cadastrado no momento. Acesse '📋 Cadastrar Aluno' para registrar os dados.")
