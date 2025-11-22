# --- CRITICAL FIX FOR OMP ERROR ---
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# ----------------------------------

import streamlit as st
import spacy
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px  # NEW: For Power BI style charts

# --- 1. APP CONFIGURATION & CUSTOM CSS ---
st.set_page_config(layout="wide", page_title="NexusAI: Market Intelligence Graph")

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .control-panel {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNCTIONS (The "Brain") ---

@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.error("spaCy model not found. Please run: python -m spacy download en_core_web_sm")
        return None

def extract_entities(text, nlp):
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "MONEY", "DATE", "GPE", "PRODUCT"]:
            entities.append((ent.text, ent.label_))
            
    feature_keywords = ["api", "dashboard", "analytics", "security", "sso", "cloud", "mobile", "integration", "ai", "automation"]
    for token in doc:
        if token.text.lower() in feature_keywords:
            entities.append((token.text, "FEATURE"))
            
    return entities

def build_graph(entities, edge_threshold):
    G = nx.Graph()
    for entity, label in entities:
        G.add_node(entity, label=label)
    for i in range(len(entities) - 1):
        source = entities[i][0]
        target = entities[i+1][0]
        if source != target:
            G.add_edge(source, target)
    return G

# --- 3. THE "HEADER AREA" ---

st.title("🔮 NexusAI") 
st.markdown("### Market Intelligence Graph")

with st.container():
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("🎨 Visuals")
        layout_type = st.selectbox("Graph Layout", ["spring", "circular", "kamada_kawai", "shell"])
        
    with col2:
        st.subheader("📏 Dimensions")
        node_size = st.slider("Node Size", 10, 200, 50)
        font_size = st.slider("Font Size", 5, 20, 10)
        
    with col3:
        st.subheader("🔍 Filters")
        show_features = st.checkbox("Show Features", value=True)
        show_money = st.checkbox("Show Pricing", value=True)
        
    with col4:
        st.subheader("⚙️ Export")
        if st.button("Download Data"):
            st.toast("Data ready for export!")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MAIN CONTENT AREA ---

nlp = load_nlp()

default_text = """
Salesforce launched a new AI automation feature priced at $5000. 
HubSpot competes with Salesforce offering similar CRM integration but better mobile analytics.
Zoho aims for the small business market with low cost cloud security and API access.
Microsoft Dynamics integrates deep security features and enterprise SSO.
"""

# Layout: Two Tabs (Graph vs Dashboard)
tab1, tab2, tab3 = st.tabs(["🕸️ Network Graph", "📊 Analytics Dashboard", "🔌 Power BI Integration"])

with tab1:
    user_text = st.text_area("Paste Competitor Text / Article / Review:", value=default_text, height=150)
    
    if st.button("Generate Nexus Graph", type="primary"):
        if nlp:
            with st.spinner("NexusAI is analyzing market patterns..."):
                # Extraction
                raw_entities = extract_entities(user_text, nlp)
                
                # Filtering
                filtered_entities = []
                for ent, label in raw_entities:
                    if label == "FEATURE" and not show_features: continue
                    if label == "MONEY" and not show_money: continue
                    filtered_entities.append((ent, label))
                
                # Save data for Tab 2
                st.session_state['entities'] = filtered_entities
                
                # Graphing
                G = build_graph(filtered_entities, 0.5)
                if G.number_of_nodes() > 0:
                    fig, ax = plt.subplots(figsize=(12, 8))
                    
                    if layout_type == "spring": pos = nx.spring_layout(G, k=0.5)
                    elif layout_type == "circular": pos = nx.circular_layout(G)
                    elif layout_type == "kamada_kawai": pos = nx.kamada_kawai_layout(G)
                    else: pos = nx.shell_layout(G)

                    color_map = []
                    for node in G:
                        label = G.nodes[node]['label']
                        if label == "ORG": color_map.append('#ff9999')
                        elif label == "FEATURE": color_map.append('#99ff99')
                        elif label == "MONEY": color_map.append('#ffcc99')
                        else: color_map.append('#99ccff')

                    nx.draw(G, pos, with_labels=True, node_color=color_map, 
                            node_size=node_size * 10, font_size=font_size, 
                            edge_color="#e0e0e0", width=1.5, alpha=0.9)
                    st.pyplot(fig)
                else:
                    st.warning("No entities found.")

with tab2:
    st.subheader("Market Analytics")
    
    if 'entities' in st.session_state and st.session_state['entities']:
        df = pd.DataFrame(st.session_state['entities'], columns=["Entity", "Category"])
        
        # KPI Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Competitors", len(df[df['Category']=='ORG']))
        m2.metric("Key Features", len(df[df['Category']=='FEATURE']))
        m3.metric("Pricing Points", len(df[df['Category']=='MONEY']))
        
        st.divider()
        
        # Charts Layout
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("### Entity Distribution")
            # Donut Chart like Power BI
            fig_pie = px.pie(df, names='Category', title='Breakdown by Category', hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with chart_col2:
            st.markdown("### Top Mentions")
            # Bar Chart
            top_entities = df['Entity'].value_counts().head(10).reset_index()
            top_entities.columns = ['Entity', 'Count']
            fig_bar = px.bar(top_entities, x='Entity', y='Count', color='Count', title='Most Frequent Terms')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Go to the 'Network Graph' tab and click Generate to see analytics.")

with tab3:
    st.subheader("Embed Microsoft Power BI")
    st.markdown("If you have a published Power BI report URL, paste it below to view it here.")
    
    power_bi_url = st.text_input("Power BI Report URL", placeholder="https://app.powerbi.com/reportEmbed?reportId=...")
    
    if power_bi_url:
        st.markdown(f'<iframe width="100%" height="600" src="{power_bi_url}" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)
    else:
        st.image("https://community.powerbi.com/t5/image/serverpage/image-id/86481i8E532C0CF0158974?v=v2", width=100)
        st.caption("No URL provided. Charts above (in Analytics Dashboard) are generated automatically from your text.")

# --- 5. FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px; color: #666;">
        Powered by <b>Sumanta Pani</b>
    </div>
    """, 
    unsafe_allow_html=True
)