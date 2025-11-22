🔮 NexusAI: Market Intelligence Graph

NexusAI is a next-generation Market Intelligence tool designed to transform unstructured competitor text into actionable visual knowledge.

By leveraging Natural Language Processing (NLP) and Graph Theory, NexusAI reads text (such as news articles, reviews, or competitor reports) and automatically maps the relationships between Companies, Features, and Pricing.

🚀 Features
Live demo : https://nexus-ai-sumanta.streamlit.app

Knowledge Graph Visualization: Automatically builds a network graph connecting organizations, product features, and pricing points.

Smart Entity Extraction: Uses spaCy to identify:

ORG: Competitors & Companies

MONEY: Pricing & Costs

FEATURE: Custom tech-focused keywords (API, Cloud, AI, SSO, etc.)

Interactive Dashboard: A "Power BI-style" analytics tab using Plotly to visualize entity distribution and top mentions.

Power BI Integration: Dedicated slot to embed live Microsoft Power BI reports.

Custom UI: Features a top-aligned "Command Center" header for controlling visuals, dimensions, and filters.

🛠️ Tech Stack

Frontend: Streamlit

NLP Engine: spaCy (en_core_web_sm)

Graphing: NetworkX & Matplotlib

Analytics: Plotly Express & Pandas

📦 Installation

Clone the repository:

git clone [https://github.com/yourusername/nexus-ai.git](https://github.com/yourusername/nexus-ai.git)
cd nexus-ai


Install Dependencies:
We use a requirements.txt file to manage all libraries, including the specific spaCy model.

pip install -r requirements.txt


Note: If you encounter an issue with the spaCy model download, run:

python -m spacy download en_core_web_sm


🚦 Usage

Navigate to the project folder in your terminal.

Run the Streamlit app:

streamlit run nexus_ai.py


The app will open in your browser at http://localhost:8501.

📖 How to Use

Paste Text: Copy a paragraph about competitors (e.g., from a tech blog or news site) into the text area.

Generate Graph: Click the "Generate Nexus Graph" button.

Explore:

Tab 1 (Network Graph): View the visual connections. Use the top header to change layout (Spring/Circular) or filter out Pricing/Features.

Tab 2 (Analytics): View pie charts and bar graphs breaking down the data.

Tab 3 (Power BI): Paste a published Power BI URL to view external reports.

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

📄 License


MIT
