import streamlit as st
from internal_data import *

phone_number = '(512) 729-9486'

# Define question placeholders

questions = [
    "What is your company's country of origin?",
    "What industry does your company operate in?",
    "What type of products do you export to the U.S.?",
    "What is the size of your operation? (e.g., Small, Medium, Large)",
    "How many employees does your company have?",
    "What is your average export frequency to the U.S. per month?",
    "What shipping modalities do you use? (e.g., Air Freight, Ocean Freight, Trucking, etc.)",
    "What are your primary compliance challenges, or gaps in traceability, if any?",
    "What traceability systems or documentation methods do you currently use?",
    "Are you currently making any upgrades or changes to improve FDA compliance?"
]

# Customer Data Answers
answer_sets = {
    "Empty": [
        "" for i in range(len(questions))
    ],
    # "Iberian Orchard Exports": [
    #     "Spain", "Fresh Fruits", "High-quality apples",
    #     "Mid-sized", 150, 4.5, 
    #     "Refrigerated Trucking,Ocean Freight",
    #     "None; proactively upgrades systems", 
    #     "Highly automated traceability systems",
    #     "Continuously monitors temperature and storage conditions"
    # ],
    # "BellaCarota Organics": [
    #     "Italy", "Organic Vegetables", "Premium organic carrots",
    #     "Small-to-Medium", 50, 2.5, 
    #     "Road Freight, Air Freight",
    #     "Gaps in traceability data", 
    #     "Transitioning from paper to digital recordkeeping",
    #     "Actively streamlining coordination with local suppliers"
    # ],
    # "Le Bœuf Exquis": [
    #     "France", "Premium Meat", "High-quality beef cuts",
    #     "Mid-sized", 200, 5.5, 
    #     "Refrigerated Ocean Freight",
    #     "None; strict compliance", 
    #     "State-of-the-art traceability systems",
    #     "Continuous process refinement for quality control"
    # ],
    # "AlpenKäse Delights": [
    #     "Germany", "Artisanal Dairy", "Gourmet handcrafted cheeses",
    #     "Mid-sized", 100, 3.5, 
    #     "Refrigerated Air Freight, Ocean Freight",
    #     "None; adheres strictly to protocols", 
    #     "Robust documentation and quality assurance programs",
    #     "Maintains high-quality assurance for U.S. market entry"
    # ],
    # "Nordic Salmon Select": [
    #     "Norway", "Seafood", "Wild-caught salmon",
    #     "Large-scale", 250, 8, 
    #     "Air Freight, Refrigerated Sea Containers",
    #     "Sporadic traceability challenges", 
    #     "Significant investment in traceability technology",
    #     "Recent digital upgrades and staff training"
    # ],
    # "Moroccan Sun Citrus": [
    #     "Morocco", "Citrus Fruits", "Diverse high-quality citrus mix",
    #     "Small-to-Medium", 50, 2.5, 
    #     "Refrigerated Trucking, Ocean Freight",
    #     "Scaling operations while ensuring compliance", 
    #     "Gradual digital adoption", 
    #     "Investing in process monitoring for traceability"
    # ],
    # "Anatolian Harvest Organics": [
    #     "Turkey", "Organic Vegetables", "High-quality organic tomatoes",
    #     "Mid-sized", 120, 4.5, 
    #     "Road Transport, Air Freight",
    #     "None; strong compliance commitment", 
    #     "Advanced digital traceability systems",
    #     "Coordination with local farmers for comprehensive data"
    # ],
    # "Frango Fino Brazil": [
    #     "Brazil", "Poultry", "High-quality chicken breasts",
    #     "Large", 300, 6.5, 
    #     "Refrigerated Ocean Freight, Air Freight",
    #     "Past packaging compliance issues", 
    #     "Significant investment in automation and quality control",
    #     "Continuous upgrades to mitigate risks"
    # ],
    # "Nile Artisan Breads": [
    #     "Egypt", "Artisan Bakery", "Handcrafted breads and baked goods",
    #     "Small", 25, 1.5, 
    #     "Ground Transport, Air Freight",
    #     "None; hands-on traceability approach", 
    #     "Small-batch production with detailed tracking",
    #     "Focuses on heritage and authenticity for niche markets"
    # ],
    "Belgian Velvet Chocolates": [
        "Belgium", "Confectionery", "Gourmet artisanal chocolates",
        "Small-to-Medium", 60, 2.5, 
        "Air Freight",
        "None; strict traceability adherence", 
        "Advanced traceability systems",
        "Preserves brand image and proprietary data security"
    ]
}


st.write(f"# Epic FDA Compliance Chatbot 🥕")

st.write(f"## Export Management Software/ERP Integration")
st.write(f"#### Thank you for integrating your internal records ✅")


st.write(f"## Answer some questions so we can know you")

# Select answer set
selected_set = st.selectbox("Choose a preset answer set:", list(answer_sets.keys()))

# Store current answers
answers = answer_sets[selected_set]

# Display form with preloaded answers
with st.form("user_form"):
    user_inputs = []
    for i, question in enumerate(questions):
        user_input = st.text_input(question, value=answers[i])
        user_inputs.append(user_input)
    
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"### Thank you for submitting! Your chatbot is ready to use. Please call {phone_number}")
    # for question, answer in zip(questions, user_inputs):
        # st.write(f"**{question}**: {answer}")



x = lambda i: "Q: " + questions[i] + "\nA: " + f"{answer_sets[selected_set][i]}" + "\n\n"

# generate thing to paste into prompt
prompt_paste = f"""
{''.join(x(i) for i in range(len(questions)))}
"""

print(prompt_paste)


print("\n * 10")

print(DATA.get(selected_set))

throw = """
You are an AI-powered compliance assistant specializing in FDA Food Traceability Final Rule regulations. Your goal is to help exporters navigate regulatory requirements, providing clear, actionable guidance while ensuring accuracy based on official FDA sources."""