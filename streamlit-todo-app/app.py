import streamlit as st

# Initialize session state for to-dos
if 'todos' not in st.session_state:
    st.session_state.todos = []
if 'completed' not in st.session_state:
    st.session_state.completed = []

st.title("To-Do App")

# Input for new to-do
new_todo = st.text_input("Add a new to-do:")
if st.button("Add") and new_todo:
    st.session_state.todos.append(new_todo)
    st.rerun()

# Display active to-dos
st.subheader("Active To-Dos")
for i, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.write(todo)
    with col2:
        if st.button(f"Mark Done {i}", key=f"done_{i}"):
            st.session_state.completed.append(st.session_state.todos.pop(i))
            st.rerun()

# Display completed to-dos with strikethrough
st.subheader("Completed To-Dos")
for todo in st.session_state.completed:
    st.markdown(f"~~{todo}~~")