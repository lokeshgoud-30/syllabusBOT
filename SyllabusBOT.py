# eduquery_ai.py

import openai
import streamlit as st
import sqlite3

# Set your API Key
openai.api_key = "YOUR_API_KEY"

# SQLite DB Setup (Optional)
def create_db():
    conn = sqlite3.connect("resources.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resources
                 (topic TEXT, link TEXT)''')
    c.execute("INSERT OR IGNORE INTO resources VALUES (?, ?)", 
              ("SQL Joins", "https://www.w3schools.com/sql/sql_join.asp"))
    conn.commit()
    conn.close()

def get_resource(topic):
    conn = sqlite3.connect("resources.db")
    c = conn.cursor()
    c.execute("SELECT link FROM resources WHERE topic=?", (topic,))
    data = c.fetchone()
    conn.close()
    return data[0] if data else None

# Streamlit UI
st.title("📚 EduQuery AI – Your Syllabus Helper")

question = st.text_input("Enter a topic or question from your syllabus:")

if question:
    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": f"Explain this to a college student in a simple way: {question}"}],
            temperature=0.5
        )
        answer = response['choices'][0]['message']['content']
        st.write("### ✨ Answer:")
        st.write(answer)

        resource = get_resource(question)
        if resource:
            st.write("🔗 Suggested Resource:", resource)

# Run once to set up DB
create_db()
