

# Airline Social Media Post Categorization model.
This release includes model for categorizing topics (12 categories) for social media posts from comercial Airline companies. The model is trained on dataset collected from different online platforms (e.g., Twitter, Facebook, Youtube) of a well-know airline company. It includes posts from 2016 to Jan, 2020.

The categories are:
* Aircrafts
* Business and Partnerships
* Cabin Crew
* Charity Programs
* Destinations and Airports
* Events
* Food and Comfort in Air
* Promotion
* Branding
* Sports
* Travel Blogs
* Others Categories - representing categories that are not mentioned above like travel blogs, news related to fashion among others.


## Data Annotation
To train the model, we annotated ~4500 amount of data.
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

## Model training and evaluation
The model use a traditional SVM designed using word ngrams. The motivation for using Support Vector model is to handle the size and the imbalanced class distribution present in the dataset (see Table 2, for more details).

The model is evaluated using:
* 5-fold cross validation for evaluating in-domain data performance

## SVM
For the training the classifier with SVM, we used TF-IDF representations for word ngrams. The reason to choose SVM with TF-IDF is their simplicity, and effectiveness when dealing with imbalanced small dataset.

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


## Prediction using the models
To run the classification model please use python version 3.7, install dependencies

To install the requirements:
```
pip install -r requirements.txt
```

The model can be used in two ways, either using batch of data or single data points. Even though for single datapoint the batch processing script can be used, we suggest to use the example provided in `run_airline_post_cat_models_for_single_text.ipynb`

For batch classification of data:

```
python bin/prediction_model.py -c models/airline_post_categorization_svm.config -d sample_data/sample_test.tsv -o results/sample_tst_predicted.tsv
```
For evaluation of batch with reference label, just add
the following flag to `prediction_model.py`

```
  --eval yes
```

The results of the model on the given dataset will be printed in the i/o
Example:
```
python bin/prediction_model.py.py -c models/ar_offensive_detection_svm.config -d sample_data/sample_tst_with_ref.tsv -o results/sample_tst_predicted.tsv --eval yes
```

## Classification Results

As mentioned earlier, the performance of the model is tested using 5-fold CV on training data

Table 1: Overall Performance of the model on cross-validation


Overall| Macro	F1| Weighted F1
--------| :------: | :------:
CV-Exp | 0.57 | 0.69
Total Instances	| 4404 |	-


Table 2: Class wise Performance of the model on cross-validation

Output |	Classes	 | CV-Exp |	# In Train Set
------------| :------: | :------: | :------:
Aircrafts | aircrafts | 0.72 | 278
Branding | branding | 0.3 | 143
Business and Partnerships | business_parnership | 0.4 | 135
Cabin Crew | cabin_crew | 0.42 | 62
Charity Programs | charity_programs | 0.54 | 81
Destinations and Airports | dest_and_airports | 0.66 | 740
Events | events | 0.61 | 357
Food and Comfort in Air | food_and_comfort | 0.61 | 256
Promotion | promotion | 0.55 | 411
Sports | sports | 0.89 | 786
Travel Blogs | travel_blogs | 0.29 | 104
Other Categories | other | 0.84 | 1051
