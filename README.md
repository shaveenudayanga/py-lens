# the-wheels-in-motion
Analyze public passenger vehicle data and Kia reviews to extract insights using data preparation, NLP classification, sentiment analysis, and interactive visualizations.

## Model Deployment

The task focuses on analyzing customer reviews of Kia vehicles using Hugging Face models for zero-shot classification and sentiment analysis.

Rationale for Selecting facebook/bart-large-mnli for Zero-Shot Classification:

    Designed for Zero-Shot Classification:
        The facebook/bart-large-mnli model is specifically fine-tuned on the Multi-Genre Natural Language Inference (MNLI) dataset.
        This makes it highly suitable for tasks where text needs to be classified into predefined categories without additional training.

    Versatility Across Domains:
        The model can classify text across multiple domains, making it effective for analyzing customer reviews, which may cover diverse topics like driving experience, features, and value for money.

    High Accuracy:
        BART (Bidirectional and Auto-Regressive Transformers) achieves state-of-the-art performance in natural language processing tasks, including inference and classification.

    Handles Ambiguity Well:
        The model excels at identifying the most probable category for ambiguous text by scoring each candidate label, ensuring accurate classification even for complex reviews.

    Scalable and Efficient:
        Despite its large size (406 million parameters), the model is efficient in inference tasks, especially when run on GPU, making it suitable for processing the large review dataset.

    Support for Custom Categories:
        The model accepts any custom label set, allowing flexibility to define specific categories (e.g., driving experience, features, issues).

    Proven Success:
        facebook/bart-large-mnli is widely adopted in NLP applications requiring zero-shot classification, with well-documented performance and community support.