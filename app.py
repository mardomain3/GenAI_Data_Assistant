from dotenv import load_dotenv
import os
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


# CONFIGURE LANGCHAIN + GEMINI
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature= 0
)


# LOAD DATASET

df = pd.read_excel("data/Enhanced_pizza_sell_data_2024-25.xlsx")

print("\n✅ Dataset Loaded Successfully!")
print(f"   Rows: {len(df)} | Columns: {len(df.columns)}")
print(f"   Columns: {list(df.columns)}\n")


# PROMPT 1: NATURAL LANGUAGE → PANDAS QUERY
query_prompt = PromptTemplate(
    input_variables=["columns", "question"],
    template="""
You are a pandas expert.

The dataframe is named df and has these columns:
{columns}

Convert the user's question into ONLY a valid pandas query expression.

Rules:
1. Use df as the dataframe name
2. Return ONLY the pandas code, nothing else
3. Do not explain anything
4. Do not use markdown or code fences
5. Do not use print() — just the expression

User Question: {question}
"""
)


# PROMPT 2: RESULT → BUSINESS INSIGHT
insight_prompt = PromptTemplate(
    input_variables=["question", "result"],
    template="""
You are a business data analyst.

The user asked: {question}

The query returned this result:
{result}

Give a short, clear business insight (3-5 sentences) based on this data.
Focus on what this means for the business.
"""
)


# BUILD CHAINS (LCEL style)
query_chain = query_prompt | llm | StrOutputParser()
insight_chain = insight_prompt | llm | StrOutputParser()

# ==========================================
# MAIN LOOP
# ==========================================

print("=" * 50)
print("  GenAI Query Assistant")
print("=" * 50)
print("Type 'exit' to quit.\n")

while True:
    question = input("Ask your question: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue

    # --- Step 1: Generate pandas query ---
    print("\n🔄 Generating query...\n")

    pandas_query = query_chain.invoke({
        "columns": list(df.columns),
        "question": question
    }).strip()

    print(f"Generated Query:\n  {pandas_query}\n")

    # --- Step 2: Execute the query ---
    try:
        result = eval(pandas_query)

        if isinstance(result, pd.DataFrame):
            display_result = result.head(20)
        else:
            display_result = result

        print("Query Result:")
        print(display_result)
        print()

        # --- Step 3: Generate business insight ---
        print("🔄 Generating business insight...\n")

        insight = insight_chain.invoke({
            "question": question,
            "result": str(display_result)
        })

        print("💡 AI Business Insight:")
        print(insight)
        print("\n" + "-" * 50 + "\n")

    except Exception as e:
        print(f"\n❌ Error executing query: {e}")
        print("Try rephrasing your question.\n")