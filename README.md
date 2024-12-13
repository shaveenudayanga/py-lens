# the-wheels-in-motion
Analyze public passenger vehicle data and Kia reviews to extract insights using data preparation, NLP classification, sentiment analysis, and interactive visualizations.



## Full Vehicle Statistics Analysis

Provides a comprehensive analysis of passenger vehicle statistics by processing and exploring data from `.csv` files.

### Features
- **Data Loading**: Reads and concatenates multiple `.csv` files from a specified directory.
- **Data Exploration**: Includes descriptive statistics, data type information, and basic summaries of the dataset.
- **Visualization and Insights**: (Assumed further analysis and visualizations based on cell structure).

### Dependencies
The notebook requires the following Python packages:
- `pandas` (for data manipulation and analysis)
- `os` (for file path operations)

Ensure you have these packages installed before running the notebook.

### Usage
1. Place your `.csv` files in a directory named `PassengerVehicle_Stats` relative to the notebook file.
2. Open the notebook and run the cells sequentially to process and analyze the data.
3. View summary statistics and explore additional insights provided by the notebook.

### Structure
- **Data Loading**: The notebook reads data from all `.csv` files in the `PassengerVehicle_Stats` directory.
- **Data Cleaning and Exploration**: Provides methods to inspect and summarize the data (`info`, `describe`, `dtypes`).
- **Further Analysis**: Additional code cells may include data transformations and visualizations.

### Notes
- Ensure that all `.csv` files are correctly formatted and consistent in structure.
- Modify the `file_path` variable in the notebook if using a different directory.




## Model Deployment

The task focuses on analyzing customer reviews of Kia vehicles using Hugging Face models for zero-shot classification and sentiment analysis.

Rationale for Selecting facebook/bart-large-mnli for Zero-Shot Classification:

### Designed for Zero-Shot Classification:
        The facebook/bart-large-mnli model is specifically fine-tuned on the Multi-Genre Natural Language Inference (MNLI) dataset.
        This makes it highly suitable for tasks where text needs to be classified into predefined categories without additional training.

### Versatility Across Domains:
        The model can classify text across multiple domains, making it effective for analyzing customer reviews, which may cover diverse topics like driving experience, features, and value for money.

### High Accuracy:
        BART (Bidirectional and Auto-Regressive Transformers) achieves state-of-the-art performance in natural language processing tasks, including inference and classification.

### Handles Ambiguity Well:
        The model excels at identifying the most probable category for ambiguous text by scoring each candidate label, ensuring accurate classification even for complex reviews.

### Scalable and Efficient:
        Despite its large size (406 million parameters), the model is efficient in inference tasks, especially when run on GPU, making it suitable for processing the large review dataset.

### Support for Custom Categories:
        The model accepts any custom label set, allowing flexibility to define specific categories (e.g., driving experience, features, issues).

### Proven Success:
        facebook/bart-large-mnli is widely adopted in NLP applications requiring zero-shot classification, with well-documented performance and community support.
