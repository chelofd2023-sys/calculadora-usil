import streamlit as st
import sqlite3
import json

st.set_page_config(page_title="Calculadora de Promedio", layout="centered")

def init_db():
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS notas (id INT PRIMARY KEY, dat TEXT)")
    conn.commit()
    conn.close()

def get_data():
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT dat FROM notas WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return {}

def save_data(d):
    conn = sqlite3.connect("db.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO notas (id, dat) VALUES (1, ?)", (json.dumps(d),))
    conn.commit()
    conn.close()

init_db()
data = get_data()

st.title("Calculadora de Promedio - USIL")
st.caption("Integración de Estructura y Función del Organismo Humano")

st.header("1. Evaluación Permanente (70%)")

def get_p(n):
    st.subheader(f"Práctica {n}")
    c1, c2, c3 = st.columns(3)
    
    v_pc = data.get(f"pc_{n}", 0.0)
    v_pr = data.get(f"pr_{n}", 0.0)
    v_pre = data.get(f"pre_{n}", 0.0)
    v_post = data.get(f"post_{n}", 0.0)
    v_sem = data.get(f"sem_{n}", 0.0)

    pc = c1.number_input(f"PC Teórico P{n}", 0.0, 20.0, float(v_pc), step=0.5, key=f"pc_{n}")
    pr = c2.number_input(f"Examen Práctico P{n}", 0.0, 20.0, float(v_pr), step=0.5, key=f"pr_{n}")
    pre = c3.number_input(f"Pre Test P{n}", 0.0, 20.0, float(v_pre), step=0.5, key=f"pre_{n}")

    c4, c5 = st.columns(2)
    post = c4.number_input(f"Post Test P{n}", 0.0, 20.0, float(v_post), step=0.5, key=f"post_{n}")
    sem = c5.number_input(f"Seminario P{n}", 0.0, 20.0, float(v_sem), step=0.5, key=f"sem_{n}")

    return (pc * 0.40) + (pr * 0.30) + (pre * 0.10) + (post * 0.10) + (sem * 0.10)

p1 = get_p(1)
p2 = get_p(2)
p3 = get_p(3)

prom_p = (p1 * 0.3333) + (p2 * 0.3333) + (p3 * 0.3334)

st.write("---")
st.subheader("Prueba Final de Teoría")
v_pf = data.get("pf", 0.0)
pf = st.number_input("Examen Final Teórico", 0.0, 20.0, float(v_pf), step=0.5, key="pf")

ep = round((prom_p * 0.60) + (pf * 0.40))

st.header("2. Evaluación Final (30%)")
v_ef = data.get("ef", 0.0)
ef = st.number_input("Producto Acreditable (Estaciones)", 0.0, 20.0, float(v_ef), step=0.5, key="ef")

nf = round((ep * 0.70) + (round(ef) * 0.30))

st.write("---")

if st.button("Guardar Mis Notas", type="primary"):
    cur_d = {
        "pc_1": st.session_state.pc_1, "pr_1": st.session_state.pr_1, "pre_1": st.session_state.pre_1, "post_1": st.session_state.post_1, "sem_1": st.session_state.sem_1,
        "pc_2": st.session_state.pc_2, "pr_2": st.session_state.pr_2, "pre_2": st.session_state.pre_2, "post_2": st.session_state.post_2, "sem_2": st.session_state.sem_2,
        "pc_3": st.session_state.pc_3, "pr_3": st.session_state.pr_3, "pre_3": st.session_state.pre_3, "post_3": st.session_state.post_3, "sem_3": st.session_state.sem_3,
        "pf": st.session_state.pf, "ef": st.session_state.ef
    }
    save_data(cur_d)
    st.success("¡Notas guardadas correctamente!")

st.header("Resumen de Notas")

col1, col2, col3 = st.columns(3)
col1.metric("Prom. Prácticas", f"{prom_p:.2f}")
col2.metric("Ev. Permanente (70%)", f"{ep}")
col3.metric("Nota Final", f"{nf}")

if nf >= 11:
    st.success(f"Aprobado con {nf}")
else:
    st.error(f"Desaprobado con {nf}")