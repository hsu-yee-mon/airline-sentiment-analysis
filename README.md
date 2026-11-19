# Airline Customer Feedback: Sentiment and Service Issue Analysis

A customer-feedback analysis combining sentiment classification, keyword-based service topics, and manual error analysis using historical airline tweets.

## Business Question

How can sentiment analysis help a customer experience team understand and organize airline feedback?

The project explores how text classification and service-topic rules can support feedback review. It emphasizes data quality, leakage prevention, reproducibility, and clear reporting of limitations.

## Key Results

| Measure | Result |
|---|---:|
| Source records | 14,640 |
| Modelling representatives | 7,551 |
| Training / test records | 6,040 / 1,511 |
| Majority-class baseline accuracy | 61.2% |
| Final model accuracy | 79.6% |
| Final model macro-F1 | 0.7315 |
| Final model multiclass log loss | 0.5132 |
| Records assigned at least one keyword topic | 4,177 — 28.5% |
| Unmatched records | 10,463 — 71.5% |

Negative sentiment accounted for **62.7% of source records**. These results describe the collected historical sample, not current passenger satisfaction.

## Dataset

Source: [CrowdFlower Twitter US Airline Sentiment on Kaggle](https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment).

The dataset contains tweets from February 2015 concerning six airlines: American, Delta, Southwest, United, US Airways, and Virgin America.

The project uses tweet text for sentiment prediction. Source sentiment annotations serve as reference labels. Annotation-derived fields, including negative complaint reasons and sentiment-confidence scores, are excluded from predictors.

Download `Tweets.csv` from the source and place it at:

`data/twitter_airline_sentiment/Tweets.csv`

## Approach

### Data Quality and Leakage Prevention

- Retained all 14,640 source records for descriptive analysis.
- Excluded 36 records belonging to 18 tweet-ID groups with conflicting sentiment labels from modelling.
- Grouped tweets into connected components using shared authors or identical normalized text.
- Selected the earliest eligible tweet per component, producing 7,551 modelling representatives.
- Created a stratified 80/20 training/test split with seed `961731`.
- Fitted vocabulary and IDF weights within each training fold during cross-validation.

Selecting one representative per component reduces overlap between related observations across splits, but also excludes distinct feedback within the same component.

### Text Processing

Text normalization includes Unicode normalization, URL and mention replacement, lowercasing, contraction expansion, and whitespace normalization. Hashtag words and negation are retained.

### Sentiment Classification

The final model combines:

- TF-IDF features, with a maximum of 5,000 features and minimum document frequency of 2.
- Logistic regression with L2 regularization.
- Three-fold stratified training-only cross-validation.
- Selection by mean macro-F1 across unigram and unigram-plus-bigram configurations and `C ∈ {0.3, 1, 3}`.

The selected configuration used **unigrams and C = 3**, achieving a mean cross-validation macro-F1 of **0.7059**.

### Keyword-Based Topic Exploration

Contextual keyword rules identify five overlapping service topics:

- Delay
- Baggage
- Staff
- Refund
- Customer support

A 50-record development audit informed rule revisions. Thirteen predictions changed and 37 remained unchanged. The revised rules were not independently validated.

`no_match` means no defined rule matched. It does not automatically indicate an error or an absence of service concerns.

## Sentiment Evaluation

| Sentiment | Precision | Recall | F1 | Test support |
|---|---:|---:|---:|---:|
| Negative | 0.8242 | 0.9222 | 0.8704 | 925 |
| Neutral | 0.7004 | 0.5488 | 0.6154 | 328 |
| Positive | 0.7717 | 0.6550 | 0.7086 | 258 |

The majority-class baseline predicted every tweet as negative. Although it achieved 61.2% accuracy, it identified no neutral or positive tweets.

The final model recognized all three classes, with weaker performance on neutral feedback. Error inspection highlighted challenges involving questions, implied meaning, and ambiguous or corrupted wording.

Earlier baseline results were inspected on the same test split before final evaluation. The final results therefore should not be described as coming from a completely untouched final holdout.

## Service-Topic Findings

The following figures use source sentiment annotations, not model predictions.

| Keyword topic | Matching source rows | Negative sentiment |
|---|---:|---:|
| Delay | 947 | 91.8% |
| Baggage | 1,105 | 86.8% |
| Staff | 1,192 | 74.2% |
| Refund | 271 | 84.9% |
| Customer support | 1,196 | 89.5% |

Topics overlap, so their counts cannot be summed as unique records. Sentiment describes the whole tweet, rather than sentiment specifically directed toward the matched topic.

Staff-related feedback also included praise: 20.4% of matching records were positive.

## Potential Business Use

The classifier could support an initial feedback-review queue, while topic tags could help reviewers locate feedback about service areas.

The findings suggest investigating disruptions, customer-contact difficulties, baggage, and reimbursement. Staff-related praise could provide examples of positive service experiences.

Human review remains useful, particularly for neutral questions, ambiguous messages, and unmatched feedback. The project does not establish root causes or measure operational savings.

## Running the Analysis

Dependencies are managed with **Pipenv**. Use the committed `Pipfile` and `Pipfile.lock` to recreate the project environment.

### Setup

Install Pipenv if needed:

```bash
python -m pip install pipenv
```

From the project root, install the locked dependencies, including development tools:

```bash
pipenv sync --dev
```

Use the Python version specified in the `Pipfile`.

### Run the Notebook

1. Download `Tweets.csv` and place it at:
   `data/twitter_airline_sentiment/Tweets.csv`
2. Ensure the completed manual audit workbook is available at:
   `outputs/topic_audit_development_audited.xlsx`
   with a sheet named `Tweet Audit`.
3. Launch Jupyter:

   ```bash
   pipenv run jupyter notebook
   ```

4. Open `social-media-sentiment-analysis-visualization.ipynb`.
5. Select the project environment as the notebook kernel, restart the kernel, and run all cells in order.

The completed audit workbook is a manually annotated input. Running the notebook generates a blank review template but does not recreate the manual annotations.

The audit comparison cell expects:

`outputs/topic_audit_development_audited.xlsx`

with a sheet named `Tweet Audit`. This is a manually annotated input; generating the blank audit template does not recreate the annotations.

## Limitations

- The dataset is historical and does not represent current customers or all airline passengers.
- Descriptive analysis retains repeated source records.
- Modelling representatives cover a different population from the full descriptive registry.
- Sentiment annotations may contain ambiguity or errors.
- Neutral and positive sentiment are harder to identify than negative sentiment.
- The split does not establish performance on future feedback.
- Topic rules cover only five service areas and can produce false matches or miss relevant wording.
- The topic audit is development work with no independent validation.
- Coverage measures how often rules assign a topic, not tagging accuracy.
- Business impact has not been measured.

## Tools

Python · pandas · NumPy · scikit-learn · Matplotlib · Seaborn · Jupyter

## Author

Hsu Yee Mon

This portfolio project adapts an academic assignment into a reproducible customer-feedback case study.