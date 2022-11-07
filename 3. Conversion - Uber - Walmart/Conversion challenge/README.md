## JEDHA PROJECT INFORMATION. SUPERVISED ML

## Conversion challenge

Participate in a machine learning competition among classmates, similar to Kaggle competitions (performances evaluated independently by teacher and put on a leaderboard).<br>
Context :
(Imbalanced) Data from a website publishing a newsletter. The goal is to build a model that predicts if a given user will subscribe to the newsletter with the little information available and analyze parameters of the model to highlight features most important to explain the behaviour of users.

Four steps:
- Make an EDA, all necessary preprocessings to the data and train a baseline model
- Improve the model's f1-score on test set (suggestions : feature engineering, regularization, non-linear models, hyperparameter optimization...)
- Once satisfied with the model's score, use it to make predictions with (unlabeled) test data and dump to a .csv file that will be sent to the teacher. Several submissions are allowed and trying different models is encouraged.
- Take some time to analyze the best model's parameters and determine if there are levers for actions that would help to improve the newsletter's conversion rate, make recommendations to the team.

Models used :
Logistic regression, Decision Tree, Random Forest, AdaBoost (DT & LR), XGBoost, Voting ensemble

Tools & metrics :
F1 score, Grid Search CV, Confusion matrices, ROC curve, Stratified K-fold

Visualization libraries :
Plotly, Matplotlib
