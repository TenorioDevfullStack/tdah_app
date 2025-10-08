import streamlit as st
import pandas as pd
import datetime
import os

# -----------------------------------------------------------------------------
# Funções utilitárias para leitura e gravação de dados
# -----------------------------------------------------------------------------

TASKS_FILE = "tasks.csv"
FINANCE_FILE = "finance.csv"
NOTES_FILE = "notes.txt"
POINTS_PER_TASK = 10

# categorias padrão para tarefas e finanças
DEFAULT_TASK_CATEGORIES = ["Trabalho", "Pessoal", "Finanças", "Saúde", "Estudos", "Outro"]
DEFAULT_FINANCE_CATEGORIES = ["Moradia", "Alimentação", "Saúde", "Transporte", "Lazer", "Educação", "Outros"]

# -----------------------------------------------------------------------------
# Carregar e salvar tarefas
# -----------------------------------------------------------------------------

def load_tasks():
    if os.path.exists(TASKS_FILE):
        df = pd.read_csv(TASKS_FILE)
        # Convert date columns to datetime
        if not df.empty:
            df["due_date"] = pd.to_datetime(df["due_date"])
        return df
    else:
        return pd.DataFrame(columns=["id", "description", "category", "priority", "due_date", "completed", "points"])

def save_tasks(df):
    df.to_csv(TASKS_FILE, index=False)

# -----------------------------------------------------------------------------
# Carregar e salvar transações financeiras
# -----------------------------------------------------------------------------

def load_finance():
    if os.path.exists(FINANCE_FILE):
        df = pd.read_csv(FINANCE_FILE)
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
        return df
    else:
        return pd.DataFrame(columns=["date", "type", "category", "description", "amount"])

def save_finance(df):
    df.to_csv(FINANCE_FILE, index=False)

# -----------------------------------------------------------------------------
# Carregar e salvar notas
# -----------------------------------------------------------------------------

def load_notes():
    notes = []
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                timestamp, content = line.split("|", 1)
                notes.append({"timestamp": timestamp.strip(), "content": content.strip()})
    return notes

def save_note(content: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}|{content}\n")

# -----------------------------------------------------------------------------
# Página de tarefas
# -----------------------------------------------------------------------------

def page_tasks():
    st.header("🗂️ Lista de Tarefas")
    tasks_df = load_tasks()

    # mostrar pontos acumulados
    total_points = tasks_df.loc[tasks_df["completed"] == True, "points"].sum()
    st.metric("Pontos acumulados", int(total_points))

    # mostrar tabela de tarefas
    if not tasks_df.empty:
        # aplicar cor vermelha para tarefas atrasadas
        def highlight_row(row):
            if not row["completed"] and row["due_date"] < pd.Timestamp.now():
                return ["background-color: #ffe6e6"] * len(row)
            return [""] * len(row)
        st.dataframe(
            tasks_df.style.apply(highlight_row, axis=1),
            height=300,
            use_container_width=True,
        )
    else:
        st.info("Nenhuma tarefa registrada.")

    # Formulário para adicionar nova tarefa
    with st.form("add_task"):
        st.subheader("Adicionar nova tarefa")
        description = st.text_input("Descrição")
        category = st.selectbox("Categoria", DEFAULT_TASK_CATEGORIES)
        priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        due_date = st.date_input("Data de vencimento", datetime.date.today())
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            if description:
                new_id = tasks_df["id"].max() + 1 if not tasks_df.empty else 1
                new_row = {
                    "id": new_id,
                    "description": description,
                    "category": category,
                    "priority": priority,
                    "due_date": pd.Timestamp(due_date),
                    "completed": False,
                    "points": POINTS_PER_TASK,
                }
                tasks_df = tasks_df.append(new_row, ignore_index=True)
                save_tasks(tasks_df)
                st.success("Tarefa adicionada com sucesso!")
            else:
                st.error("A descrição não pode ficar vazia.")

    # marcar tarefa como concluída
    st.subheader("Concluir tarefas")
    if not tasks_df.empty:
        incomplete_tasks = tasks_df[tasks_df["completed"] == False]
        if not incomplete_tasks.empty:
            task_to_complete = st.selectbox(
                "Selecione a tarefa a concluir", incomplete_tasks["description"].tolist()
            )
            if st.button("Marcar como concluída"):
                idx = tasks_df[tasks_df["description"] == task_to_complete].index[0]
                tasks_df.at[idx, "completed"] = True
                save_tasks(tasks_df)
                st.success(f"Tarefa '{task_to_complete}' marcada como concluída!")
        else:
            st.info("Não há tarefas pendentes.")

# -----------------------------------------------------------------------------
# Página do cronômetro Pomodoro
# -----------------------------------------------------------------------------

def page_pomodoro():
    st.header("⏱️ Timer Pomodoro")
    work_minutes = st.number_input("Minutos de trabalho (Pomodoro)", min_value=1, max_value=60, value=25)
    break_minutes = st.number_input("Minutos de pausa", min_value=1, max_value=30, value=5)

    if "pomodoro_started" not in st.session_state:
        st.session_state.pomodoro_started = False
        st.session_state.start_time = None
        st.session_state.work_duration = None
        st.session_state.break_duration = None
        st.session_state.phase = "work"  # work ou break

    if st.button("Iniciar/Pausar"):
        if not st.session_state.pomodoro_started:
            # iniciar
            st.session_state.pomodoro_started = True
            st.session_state.start_time = datetime.datetime.now()
            st.session_state.work_duration = datetime.timedelta(minutes=work_minutes)
            st.session_state.break_duration = datetime.timedelta(minutes=break_minutes)
            st.session_state.phase = "work"
        else:
            # pausar
            st.session_state.pomodoro_started = False

    # exibir tempo restante
    if st.session_state.pomodoro_started:
        now = datetime.datetime.now()
        elapsed = now - st.session_state.start_time
        # definir duração da fase atual
        if st.session_state.phase == "work":
            remaining = st.session_state.work_duration - elapsed
            if remaining.total_seconds() <= 0:
                st.session_state.phase = "break"
                st.session_state.start_time = now
                remaining = st.session_state.break_duration
        else:
            remaining = st.session_state.break_duration - elapsed
            if remaining.total_seconds() <= 0:
                st.session_state.phase = "work"
                st.session_state.start_time = now
                remaining = st.session_state.work_duration
        minutes, seconds = divmod(int(remaining.total_seconds()), 60)
        st.write(f"Fase atual: {'Trabalho' if st.session_state.phase == 'work' else 'Pausa'}")
        st.subheader(f"Tempo restante: {minutes:02d}:{seconds:02d}")
        # exibir progresso
        total_seconds = (
            st.session_state.work_duration.total_seconds()
            if st.session_state.phase == "work"
            else st.session_state.break_duration.total_seconds()
        )
        progress_fraction = max(0.0, remaining.total_seconds() / total_seconds)
        st.progress(1 - progress_fraction)
        # auto-refresh a cada segundo
        st.experimental_rerun()
    else:
        st.info("Pressione iniciar para começar o Pomodoro.")

# -----------------------------------------------------------------------------
# Página de finanças
# -----------------------------------------------------------------------------

def page_finances():
    st.header("💰 Finanças Pessoais")
    finance_df = load_finance()

    # mostrar resumo
    if not finance_df.empty:
        total_income = finance_df[finance_df["type"] == "Receita"]["amount"].sum()
        total_expense = finance_df[finance_df["type"] == "Despesa"]["amount"].sum()
        saldo = total_income - total_expense
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de receitas", f"R$ {total_income:,.2f}")
        col2.metric("Total de despesas", f"R$ {total_expense:,.2f}")
        col3.metric("Saldo", f"R$ {saldo:,.2f}", delta=None)

        st.dataframe(finance_df, height=300, use_container_width=True)

        # gráfico de despesas por categoria
        expenses = finance_df[finance_df["type"] == "Despesa"]
        if not expenses.empty:
            exp_cat = expenses.groupby("category")["amount"].sum()
            st.subheader("Distribuição de gastos por categoria")
            st.bar_chart(exp_cat)
    else:
        st.info("Nenhuma transação registrada.")

    # Formulário para adicionar transação
    with st.form("add_transaction"):
        st.subheader("Registrar transação")
        trans_type = st.selectbox("Tipo", ["Receita", "Despesa"])
        category = st.selectbox("Categoria", DEFAULT_FINANCE_CATEGORIES)
        description = st.text_input("Descrição")
        amount = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
        date = st.date_input("Data", datetime.date.today())
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            if amount > 0:
                new_row = {
                    "date": pd.Timestamp(date),
                    "type": trans_type,
                    "category": category,
                    "description": description,
                    "amount": amount,
                }
                finance_df = finance_df.append(new_row, ignore_index=True)
                save_finance(finance_df)
                st.success("Transação registrada com sucesso!")
            else:
                st.error("O valor deve ser maior que zero.")

# -----------------------------------------------------------------------------
# Página de anotações
# -----------------------------------------------------------------------------

def page_notes():
    st.header("📝 Anotações")
    notes = load_notes()

    # adicionar nova anotação
    with st.form("add_note"):
        st.subheader("Nova anotação")
        content = st.text_area("Escreva sua anotação aqui")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            if content.strip():
                save_note(content.strip())
                st.success("Anotação salva com sucesso!")
            else:
                st.error("A anotação não pode ficar vazia.")

    # busca nas anotações
    st.subheader("Anotações salvas")
    query = st.text_input("Pesquisar", "")
    filtered_notes = [n for n in notes if query.lower() in n["content"].lower()]
    if filtered_notes:
        for note in filtered_notes:
            st.markdown(f"**{note['timestamp']}** – {note['content']}")
            st.markdown("---")
    else:
        st.info("Nenhuma anotação encontrada.")

# -----------------------------------------------------------------------------
# Página de configurações
# -----------------------------------------------------------------------------

def page_settings():
    st.header("⚙️ Configurações")
    st.markdown("Nesta versão demonstrativa, algumas configurações dependem do tema padrão do Streamlit.")
    theme = st.selectbox("Tema", ["Claro", "Escuro"])
    font_size = st.slider("Tamanho da fonte (em px)", 14, 22, 16)

    # aplicar tema e tamanho de fonte usando CSS injetado
    # O tema claro/escuro não pode ser alterado dinamicamente em Streamlit sem recarregar a página,
    # mas aplicamos estilos de cor de fundo e texto para simular.
    if theme == "Claro":
        bg_color = "#ffffff"
        text_color = "#000000"
    else:
        bg_color = "#1e1e1e"
        text_color = "#ffffff"
    st.markdown(
        f"""
        <style>
        html, body, .reportview-container {{
            background-color: {bg_color};
            color: {text_color};
            font-size: {font_size}px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.info("As alterações de tema podem exigir recarregar a página no navegador para aplicar completamente.")

# -----------------------------------------------------------------------------
# Função principal
# -----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Gestão Pessoal TDAH", page_icon="✅", layout="centered")
    menu = st.sidebar.radio(
        "Menu", ("Tarefas", "Pomodoro", "Finanças", "Anotações", "Configurações"), index=0
    )

    if menu == "Tarefas":
        page_tasks()
    elif menu == "Pomodoro":
        page_pomodoro()
    elif menu == "Finanças":
        page_finances()
    elif menu == "Anotações":
        page_notes()
    else:
        page_settings()

if __name__ == "__main__":
    main()
