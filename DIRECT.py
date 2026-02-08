import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Chat to Excel AI", layout="centered")

st.title("🧠 Chat → Excel AI")
st.write("Example:")
st.code("Create excel for students with name raj ram rohan age 12 13 14")

# ---------------- CHAT INPUT ----------------
user_prompt = st.text_area(
    "Describe the Excel you want",
    placeholder="Create excel for students with name raj ram rohan age 12 13 14"
)

# ---------------- AI LOGIC (SAFE VERSION) ----------------
def ai_create_excel(prompt: str):
    prompt = prompt.lower()

    name_match = re.search(r"name\s+([a-z\s]+)", prompt)
    age_match = re.search(r"age\s+([\d\s]+)", prompt)

    names = name_match.group(1).split() if name_match else []
    ages  = list(map(int, age_match.group(1).split())) if age_match else []

    # 🔒 SAFETY: equal rows only
    rows = min(len(names), len(ages))

    if rows == 0:
        return pd.DataFrame({"Error": ["Could not understand input"]})

    data = {
        "Name": names[:rows],
        "Age": ages[:rows]
    }

    return pd.DataFrame(data)

# ---------------- BUTTON ----------------
if st.button("🚀 Generate Excel"):
    if user_prompt.strip() == "":
        st.warning("Please describe the Excel you want.")
    else:
        try:
            df = ai_create_excel(user_prompt)

            st.subheader("Generated Excel Preview")
            st.dataframe(df)

            file_name = "AI_Created_Excel.xlsx"
            df.to_excel(file_name, index=False)

            with open(file_name, "rb") as f:
                st.download_button(
                    "⬇ Download Excel",
                    data=f,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception as e:
            st.error(str(e))
