# 📌 Company Atlas: Industry Clustering & Exploration  

## 📝 Introduction  
This project builds a complete **Data Engineering, NLP, and Machine Learning pipeline**, culminating in an interactive **Streamlit application** called *Company Atlas*.  

The goal is to take a massive raw dataset of companies (**3.5 GB+**), analyze it, clean and process it, generate embeddings from company descriptions, reduce dimensionality, perform hierarchical clustering, auto-label clusters using an **LLM**, and finally make the dataset explorable through a sleek web UI.  

This project highlights skills in **data engineering, large-scale processing, NLP, clustering, and LLM-powered automation** — end-to-end from raw data to production-ready application.  

---

## ⚙️ Project Roadmap  

### 1️⃣ Exploratory Data Analysis (EDA)  
- **Files:** `eda-day(1-5).ipynb`  
- Performed initial analysis on sampled dataset to understand distributions, missing values, and schema.  
- Dataset size: **3.5 GB+**, required sampling and performance tuning.  
- **Deliverable:** A summary of dataset characteristics and challenges.  

---

### 2️⃣ Data Cleaning & Joining  
- **File:** `data-cleaning-joining.py`  
- **Tasks:**  
  - Handled missing values, standardized the format for descriptions etc.  
  - Joined two related CSV datasets into a single **cleaned, merged dataset**.  
  - Ensured consistency across `uuid`, `name`, `description`, and labels.  
- **Deliverable:** `crunchbase_merged.csv`  

---

### 3️⃣ Embeddings, Dimensionality Reduction & Clustering  
- **File:** `embeddings_dim_reduction_clustering.py`  
- **NLP Pipeline:**  
  - Used **Sentence-Transformers (SBERT)** to embed company descriptions.  
  - Applied **UMAP** for dimensionality reduction.  
  - Performed **Agglomerative Clustering** for hierarchical structure.  
- **Auto-labeling:**  
  - Sampled cluster data and used an **LLM (via prompt engineering)** to assign human-readable labels.  
- **Deliverable:** A labeled clustered dataset with `fine_label` and `coarse_label` named as `organizations_with_hierarchial_clusters.csv`.  

---

### 4️⃣ Final Dataset Preparation  
- **File:** `final-app-dataset_prep.py`  
- **Tasks:**  
  - Generated `final_dataset.csv`, containing company details and cluster labels.  
  - Made dataset compatible with Streamlit app.  
- **Deliverable:** `final_dataset.csv`  

---

### 5️⃣ Interactive Streamlit Application  
- **File:** `final_app.py`  
- **How to Run:**  
  ```bash
  streamlit run final_app.py

**Steps:**

- Upload the final_dataset.csv (provided in repo).

- Explore companies via coarse clusters (industries).

- Drill down into fine clusters (sub-industries).

- Search, filter, and download company groups.

**Features:**

- Dark-themed, professional UI.

- Cluster overview bar chart.

- Clean navigation between industry levels.

- Outliers displayed as “General” instead of Unclustered for readability.

## 🛠️ Tech Stack & Tools

**Data Engineering:** Pandas, Polars, PySpark

**NLP:** Sentence-Transformers (SBERT)

**Dimensionality Reduction:** UMAP

**Clustering:** Agglomerative Clustering

**LLM:** Auto-labeling clusters with prompt-engineered LLMs

**App Framework:** Streamlit

**Visualization:** Matplotlib, Seaborn, Altair

## 📊 Summary

This project represents a full data lifecycle pipeline:
➡️ From raw 3.5 GB dataset → cleaned & merged dataset → embeddings → clustering → LLM labeling → interactive UI.

It demonstrates practical expertise in:

- Data Engineering (large-scale processing with Pandas, Polars, PySpark)

- NLP (SBERT embeddings for company descriptions)

- Machine Learning (UMAP + Agglomerative clustering)

- LLMs (auto-labeling clusters)

- App Development (Streamlit + visualization)

**The final deliverable is Company Atlas, a project showcasing the ability to take raw industry data and transform it into an intelligent, user-friendly application integrating AI,NLP and ML.**

Note: Some csv files such as the main dataset files which were initially used are not uploaded in this repo due to extremely large size, however `final dataset.csv` is the one required for running on provided streamlit app in file `final_app.py` 
