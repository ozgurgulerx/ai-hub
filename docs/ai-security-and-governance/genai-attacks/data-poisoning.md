# Data Poisoning

Attacks that corrupt model behavior by injecting malicious data into training or retrieval pipelines.

## Types

### Training Data Poisoning
Inject malicious examples into training data to create backdoors or bias model behavior.

### RAG Poisoning
Plant malicious documents in retrieval corpus to influence model outputs when retrieved.

## Attack Vectors

- Public datasets
- User-contributed content
- Web scraping sources
- Document uploads
- Knowledge base edits

## Mitigations

- Data provenance and integrity checks
- Anomaly detection in training data
- Retrieval filtering and ranking
- Content verification before indexing
- Regular audits of data sources
