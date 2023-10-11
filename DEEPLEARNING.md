# Web Vulnerability Detection with Deep Learning

This is a detection method that using combine Convolutional Neural Network (CNN) and a family of Recurrent Neural Network (RNN) to analyze features and relationships in requests from users and predict whether they are vulnerability or not.

## Model Architecture

This is a compact architectural model with two channels. For channel A, I using three layer include Conv1D - MaxPooling - GlobalMaxPooling. And for channel B, I using two layer of the RNN family (RNN, LSTM, GRU). With extremely large data sets, the model can scale with multiple channels and multiple layers to be able to respond to the size of the dataset.

## Vulnerabilities Detection

- Cross-Site Scripting
- SQL Injection
- Path Traversal (LFI)
- Command Injection
- Remote File Inclusion (RFI)
- Json & XML Injection
- HTML5 Injection
- Server Side Includes (SSI) Injection

## Datasets

The training dataset is split 70:30 for training and testing. With 70% of the district training, I use k-fold cross validation with k=5 to train the model.

| Dataset | Sample | Access |
|---|---|---|
| CISC2010 | 61065 (SQLi, XSS, CSRF, ...) | [Public](https://www.kaggle.com/datasets/ispangler/csic-2010-web-application-attacks) |
| HTTPPram | 31066 -> 10852(SQLi) 532(XSS) 89(CMDi) 290(LFI) | [Public](https://github.com/Morzeux/HttpParamsDataset) |
| Shah's | 44605 -> 13686(XSS) 30919(SQLi) | [Public](https://www.kaggle.com/syedsaqlainhussain/datasets) |
| Generate Dataset | 592479 -> 332131 (Normal) 260348 (Abnormal) | Private |

<img width="1312" alt="image" src="https://github.com/noobpk/gemini-web-vulnerability-detection/assets/31820707/975bc53a-4f4a-4545-95d3-0a0da7baa847">

## Data Decoder

The decoder was built with multiple decode layers including base64 - URL - Unicode - utf8 - clean data - ....

| Original | Decoded |
|---|---|
| ```<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="></object>``` | ```<objectdata="data:text/html;base64,<script>alert(1)</script>"></object>```|

## Data Processing

Using SentenceTransformers. A Python framework for state-of-the-art sentence, text and image embeddings.
