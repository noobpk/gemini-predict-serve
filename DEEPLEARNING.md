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
| Generate Dataset | 592479 -> 331129 (Normal) 261350 (Abnormal) | Private |

<img width="1240" alt="image" src="https://github.com/noobpk/gemini-web-vulnerability-detection/assets/31820707/66787d6d-36b2-4477-8918-44bf8a6ff5f2">


## Data Decoder

The decoder was built with multiple decode layers including base64 - URL - Unicode - utf8 - clean data - ....

| Original | Decoded |
|---|---|
| ```<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="></object>``` | ```<objectdata="data:text/html;base64,<script>alert(1)</script>"></object>```|

## Data Processing

Using SentenceTransformers. A Python framework for state-of-the-art sentence, text and image embeddings.

| Original | Encoder |
|---|---|
| ```/etc/mixmaster/remailer/pgponly.hlp``` | ```[-2.79157665e-02  7.86799937e-02 -1.95519626e-02 -4.09332477e-02 9.84075591e-02 -8.66753384e-02 -4.61700819e-02 -2.39454824e-02 ...]```|

## Model Summary

```
Model: "model_3"
__________________________________________________________________________________________________
 Layer (type)                Output Shape                 Param #   Connected to
==================================================================================================
 input_4 (InputLayer)        [(None, 384)]                0         []

 reshape_3 (Reshape)         (None, 384, 1)               0         ['input_4[0][0]']

 conv1d_15 (Conv1D)          (None, 382, 32)              128       ['reshape_3[0][0]']

 max_pooling1d_15 (MaxPooli  (None, 380, 32)              0         ['conv1d_15[0][0]']
 ng1D)

 conv1d_16 (Conv1D)          (None, 378, 64)              6208      ['max_pooling1d_15[0][0]']

 max_pooling1d_16 (MaxPooli  (None, 376, 64)              0         ['conv1d_16[0][0]']
 ng1D)

 conv1d_17 (Conv1D)          (None, 374, 128)             24704     ['max_pooling1d_16[0][0]']

 max_pooling1d_17 (MaxPooli  (None, 372, 128)             0         ['conv1d_17[0][0]']
 ng1D)

 conv1d_18 (Conv1D)          (None, 370, 256)             98560     ['max_pooling1d_17[0][0]']

 gru_15 (GRU)                (None, 384, 32)              3360      ['reshape_3[0][0]']

 max_pooling1d_18 (MaxPooli  (None, 368, 256)             0         ['conv1d_18[0][0]']
 ng1D)

 gru_16 (GRU)                (None, 384, 64)              18816     ['gru_15[0][0]']

 conv1d_19 (Conv1D)          (None, 366, 512)             393728    ['max_pooling1d_18[0][0]']

 gru_17 (GRU)                (None, 384, 128)             74496     ['gru_16[0][0]']

 max_pooling1d_19 (MaxPooli  (None, 364, 512)             0         ['conv1d_19[0][0]']
 ng1D)

 gru_18 (GRU)                (None, 384, 256)             296448    ['gru_17[0][0]']

 global_max_pooling1d_3 (Gl  (None, 512)                  0         ['max_pooling1d_19[0][0]']
 obalMaxPooling1D)

 gru_19 (GRU)                (None, 512)                  1182720   ['gru_18[0][0]']

 dropout_9 (Dropout)         (None, 512)                  0         ['global_max_pooling1d_3[0][0]
                                                                    ']

 dropout_10 (Dropout)        (None, 512)                  0         ['gru_19[0][0]']

 multiply_3 (Multiply)       (None, 512)                  0         ['dropout_9[0][0]',
                                                                     'dropout_10[0][0]']

 dropout_11 (Dropout)        (None, 512)                  0         ['multiply_3[0][0]']

 dense_18 (Dense)            (None, 512)                  262656    ['dropout_11[0][0]']

 dense_19 (Dense)            (None, 256)                  131328    ['dense_18[0][0]']

 dense_20 (Dense)            (None, 128)                  32896     ['dense_19[0][0]']

 dense_21 (Dense)            (None, 64)                   8256      ['dense_20[0][0]']

 dense_22 (Dense)            (None, 32)                   2080      ['dense_21[0][0]']

 dense_23 (Dense)            (None, 1)                    33        ['dense_22[0][0]']

==================================================================================================
Total params: 2536417 (9.68 MB)
Trainable params: 2536417 (9.68 MB)
Non-trainable params: 0 (0.00 Byte)
__________________________________________________________________________________________________
```

## Evaluate

```
1852/1852 [==============================] - 86s 45ms/step - loss: 0.0604 - accuracy: 0.9761
1852/1852 [==============================] - 80s 42ms/step

Accuracy: 97.61%
              precision    recall  f1-score   support

           0       0.97      0.98      0.98     33261
           1       0.98      0.97      0.97     25987

    accuracy                           0.98     59248
   macro avg       0.98      0.98      0.98     59248
weighted avg       0.98      0.98      0.98     59248
```
