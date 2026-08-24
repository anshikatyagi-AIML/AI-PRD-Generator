import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

def clean_output(content):
    """Cleanly extracts text from string, list, or dict content."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list) and len(content) > 0:
        first_item = content[0]
        if isinstance(first_item, dict) and "text" in first_item:
            return first_item["text"]
        elif hasattr(first_item, "text"):
            return first_item.text
    return str(content)

# Title of your web app
st.title("AI Product Requirement Generator")

# Enter your Gemini API Key
api_key = st.text_input("Enter your Gemini API Key:", type="password")

# Box where user enters the idea
idea = st.text_area("Enter your product idea:", "Build a mobile healthcare platform")

if st.button("Generate PRD"):
    if not api_key:
        st.error("Please enter your API Key first!")
    else:
        try:
            # Connect to Gemini Model using gemini-3.6-flash
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.6-flash", 
                google_api_key=api_key
            )
            
            # Step A: Business Analyst Agent converts idea to problems & personas
            st.write("🤖 **Business Analyst Agent is working...**")
            ba_prompt = f"You are a Business Analyst. Take this idea: '{idea}'. Write a Problem Statement and Target Personas."
            ba_response = llm.invoke(ba_prompt)
            ba_output = clean_output(ba_response.content)
            
            # Step B: Product Manager Agent creates full PRD
            st.write("🤖 **Product Manager Agent is working...**")
            pm_prompt = f"You are a Product Manager. Based on this analysis:\n{ba_output}\n\nGenerate: 1. User Stories, 2. Functional Requirements, 3. Non-functional Requirements, 4. Risks."
            pm_response = llm.invoke(pm_prompt)
            pm_output = clean_output(pm_response.content)
            
            # Show output on screen cleanly formatted
            st.subheader("Final PRD Output")
            st.markdown(ba_output)
            st.markdown(pm_output)
        except Exception as e:
            st.error(f"Error: {e}")