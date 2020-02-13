

# Arabic Social Media News Post Categorization model.
This is a release includes model for categorizing news topics (12 categories) for Arabic social media news posts, trained using posts from different online platforms of a well-know News media agency. The model is trained on dataset collected from post 2015 social media (Twitter, Facebook, Youtube, Instagram), in addition the model also included news titles extracted from <dataset> for 6 classes including

The model classifies a news post into either of these 12 categories.
The categories are:
* Culture, Art and Entertainment
* Business and Economy
* Crime, War and Conflict
* Education
* Environment
* Health
* Human Rights and Freedom of Speech
* Politics
* Science and Technology
* Religion
* Sports
* Others Categories - representing categories that are not mentioned above like travel blogs, news related to fashion among others.

The model use a traditional SVM designed using character ngrams. The motivation for using Support Vector model is to handle the skewneess present in the dataset (see Table 2, for more details) and also to handle different dialectal Arabic present in the text.
The model is evaluated using:
* 5-fold cross validation for evaluating in-domain data performance
* Official test set for separated from the annotated data containing 1103 social media posts.


To train the model, we annotated ~8500 amount of data.
The contents are collected from the following sources:
* Twitter
* Youtube
* Facebook
* Instagram

The annotation of the collected dataset is obtained using Amazon Mechanical Turk (AMT). To ensure the quality of the annotation and language proficiency, we utilized two different evaluation criteria of the annotator. For more details, check the below paper:

**Comming Soon**
Cite [the Arxiv paper](https://arxiv.org/):
Containing details of data collection method, annotation guideline, with link to dataset and model performance.
<!-- ```
@inproceedings{shammur2020offensive,
  title={A Multi-Platform Arabic News Comment Dataset for Offensive Language Detection},
  author={Chowdhury, Shammur Absar  and Mubarak, Hamdy and Abdelali, Ahmed and Jung, Soon-gyo and Jansen, Bernard J and Salminen, Joni},
  booktitle={Proceedings of the International Conference on Language Resources and Evaluation (LREC'20)},
  year={2020}
}
``` -->
In addition to the dataset mentioned in the above paper, we also added SANAD_SUBSET [] train data.

## Training the models

### SVM
For the training the classifier with SVM, we used TF-IDF representations for character ngrams (1,8). The reason to choose SVM with TF-IDF is their simplicity and execution time while having comparable performance for such dataset nature.

## Data Format
### Input data format
The input file should have the following fields, including
`<Input ID>\t<Text>\t<Class_Label>`
however when the model is not used to evaluate the performance, `<Class_Label>` is optional field.
*!!! The text/input should have each datapoint in a single line, if the intend post contain new lines (\n), this should be preprocessed seperately before using the model !!!*

### Output data format
The output of the file will include the following fields

* While running the model just for prediction:
`<id>\t<text>\t<class_label>`
* Output of the model when reference label is mentioned
`<id>\t<text>\t<class_label>\t<predicted_class_label>`
here predicted_class_label is the output of the model

The output are mapped to make label for readable (see Table 2 for more details).


## Predicting using the models
To run the classification model please use python version 3.7, install dependencies

To install the requirements:
```
pip install -r requirements.txt
```

The model can be used in two ways, either using batch of data or single data points. Even though for single datapoint the batch processing script can be used, we suggest to use the example provided in `run_ar_news_cat_models_for_single_text.ipynb`

For batch classification of data:

```
python bin/prediction_model.py -c models/news_categorization_arabic_svm.config -d sample_data/sample_tst.tsv -o results/sample_tst_only_prediction.tsv
```
For evaluation of batch with reference label, just add
the following flag to `prediction_model.py`

```
  --eval yes
```

The results of the model on the given dataset will be printed in the i/o
Example:
```
python bin/prediction_model.py.py -c models/ar_offensive_detection_svm.config -d sample_data/sample_tst_with_ref.tsv -o results/sample_tst_predicted.tsv --eval yes &> logs/result_dataset_with_reflab.log
```

### Classification Results

As mentioned earlier, the performance of the model is tested using 1) 5-fold CV on training data 2) official test set separated from the annotated social media post data

Table 1: Overall Performance of the model on cross-validation and official test set settings.
Overall	| CV-Exp	| On Test Set
--------| :------: | :------: | :------:
Macro	F1 | **0.74** |	**0.69**
Weighted F1	| 0.9	| 0.76
Accuracy |	0.9 |	0.76
--------| :------: | :------: | :------:
Total Instances	| 56453 |	1103
--------| :------: | :------: | :------:

Table 2: Class wise Performance of the model on cross-validation and official test set settings.

Output |	Classes	 | CV-Exp |	# In Train Set	| On Test Set	| # In Test Set
------------| :------: | :------: | :------:| :------: | :------:
Culture, Art and Entertainment | art-and-entertainment | 0.63 | 374 | 0.7 | 57
------------| :------: | :------: | :------:| :------: | :------:
Business and Economy | business-and-economy | 0.88 | 9394 | 0.6 | 27
------------| :------: | :------: | :------:| :------: | :------:
Crime, War and Conflict | crime-war-conflict | 0.55 | 965 | 0.61 | 147
------------| :------: | :------: | :------:| :------: | :------:
Education | education | 0.44 | 70 | 0.67 | 11
------------| :------: | :------: | :------:| :------: | :------:
Environment | environment | 0.6 | 132 | 0.63 | 20
------------| :------: | :------: | :------:| :------: | :------:
Health | health | 0.94 | 9529 | 0.75 | 26
------------| :------: | :------: | :------:| :------: | :------:
Human Rights and Freedom of Speech | human-rights-press-freedom | 0.45 | 365 | 0.53 | 56
------------| :------: | :------: | :------:| :------: | :------:
Politics | politics | 0.87 | 13027 | 0.84 | 559
------------| :------: | :------: | :------:| :------: | :------:
Science and Technology | science-and-technology | 0.92 | 9541 | 0.61 | 28
------------| :------: | :------: | :------:| :------: | :------:
Religion | spiritual | 0.9 | 2654 | 0.73 | 13
------------| :------: | :------: | :------:| :------: | :------:
Sports | sports | 0.96 | 9563 | 0.79 | 32
------------| :------: | :------: | :------:| :------: | :------:
Others Categories | others | 0.75 | 839 | 0.77 | 127
------------| :------: | :------: | :------:| :------: | :------:
