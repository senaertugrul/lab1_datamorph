import streamlit as st
import pandas as pd
import json

# Page configuration
st.set_page_config(page_title="DataMorph JSON", layout="wide", page_icon="🛠️")

st.title("🛠️ DataMorph JSON")
st.subheader("Instantly transform data structures to understand NoSQL flexibility.")

# Example JSON with 3 people having different fields (Step A) [cite: 64]
example_data = [
    {"id": 1, "name": "Alice", "role": "Admin", "premium": True},
    {"id": 2, "name": "Bob", "department": "Sales"},
    {"id": 3, "name": "Charlie", "skills": ["Python", "SQL"], "location": {"city": "Madrid"}}
]

# Split the screen into two columns (Step A) [cite: 62]
col1, col2 = st.columns(2)

with col1:
    st.header("JSON Input")
    json_input = st.text_area(
        "Paste your list of JSON objects here:",
        value=json.dumps(example_data, indent=2),
        height=400
    )

# Robust processing with try-except (Step C) [cite: 68]
if json_input.strip():
    try:
        # Parse and flatten JSON (Step A) [cite: 64]
        data = json.loads(json_input)
        df = pd.json_normalize(data)
        
        with col2:
            st.header("Tabular View")
            st.dataframe(df, use_container_width=True)
            
            # CSV Download option
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="datamorph_export.csv")

        # --- SCHEMA ANALYTICS (Step B) --- [cite: 66]
        st.divider()
        st.header("📊 Schema Analysis")
        
        columns = df.columns.tolist()
        total_nulls = df.isnull().sum().sum()
        
        m1, m2 = st.columns(2)
        m1.metric("Detected Columns", len(columns))
        m2.metric("Total Null Values (NaN)", int(total_nulls))
        
        st.write(f"**Column Names:** `{', '.join(columns)}` narratives")

        # Warning for Sparse Data (Step B) [cite: 66]
        if total_nulls > 0:
            st.warning(
                "⚠️ **Data Engineering Insight:** This dataset contains null values (Sparse Data). "
                "In SQL, this would be inefficient because tables are rigid 'prisons'[cite: 51]. "
                "In NoSQL, this is normal because the schema is dynamic and only stores existing fields[cite: 52]."
            )
        else:
            st.success("The schema is perfectly dense (no nulls). Ideal for traditional SQL structures.")

    except json.JSONDecodeError as e:
        with col2:
            st.error(f"🚨 **Malformed JSON!**\n\nError details: {e}")
            st.info("Check for missing commas, unquoted keys, or bracket mismatches.")
    except Exception as e:
        with col2:
            st.error(f"⚠️ An unexpected error occurred: {e}")
else:
    with col2:
        st.info("Waiting for JSON input in the left panel...")

# --- THEORY EXPANDER (Step C) --- [cite: 68]
st.divider()
with st.expander("🎓 Fixed Schema (SQL) vs. Flexible Schema (NoSQL)"):
    st.write("""
    Understanding the difference is key to modern data engineering:
    
    * **Fixed Schema (SQL):** Like a 'prison'[cite: 51]. You must define columns first. If a field wasn't defined at the start, you cannot store the data[cite: 51].
    * **Flexible Schema (NoSQL):** The schema is 'dynamic'[cite: 52]. If a record has a new field (like loyalty points), it is simply stored without affecting others[cite: 52].
    """)
