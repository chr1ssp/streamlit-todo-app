import streamlit as st
import sqlite3
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                 (id INTEGER PRIMARY KEY, task TEXT, completed INTEGER, created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

# Get all todos from database
def load_todos():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('SELECT id, task, completed FROM todos ORDER BY created_at DESC')
    todos = c.fetchall()
    conn.close()
    return todos

# Add new todo
def add_todo(task):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('INSERT INTO todos (task, completed, created_at) VALUES (?, ?, ?)',
              (task, 0, datetime.now()))
    conn.commit()
    conn.close()

# Mark todo as completed
def mark_completed(todo_id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('UPDATE todos SET completed = 1 WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()

# Delete todo
def delete_todo(todo_id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()

init_db()

st.title("To-Do App (Shared)")

# Input for new to-do
new_todo = st.text_input("Add a new to-do:")
if st.button("Add") and new_todo:
    add_todo(new_todo)
    st.rerun()

# Load and display todos
todos = load_todos()

st.subheader("Active To-Dos")
for todo_id, task, completed in todos:
    if completed == 0:
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
        with col1:
            st.write(task)
        with col2:
            if st.button("Done", key=f"done_{todo_id}"):
                mark_completed(todo_id)
                st.rerun()
        with col3:
            if st.button("Delete", key=f"del_{todo_id}"):
                delete_todo(todo_id)
                st.rerun()

st.subheader("Completed To-Dos")
for todo_id, task, completed in todos:
    if completed == 1:
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"~~{task}~~")
        with col2:
            if st.button("Delete", key=f"del_comp_{todo_id}"):
                delete_todo(todo_id)
                st.rerun()