from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report, roc_curve, precision_score
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import seaborn as sns


import warnings
warnings.filterwarnings("ignore")


class ML_Model:
  
  def __init__(self, model, X, y):
    self.model = model
    self.X = X
    self.y = y
    
  def split_data(self):
    
    X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test
  
     
  def fit(self, nn=False):
    
    X_trn, X_tst, y_trn, y_tst = self.split_data()
    
    #for model in self.models:
    if nn:
      cv_score = 'N/A'
    else:
      cv_score = cross_val_score(self.model, X_trn, y_trn, cv=5, scoring='accuracy')
    self.model.fit(X_trn, y_trn)
    test_score = self.model.score(X_tst, y_tst)
    name = self.model.__class__.__name__
    print('{model:25} CV-5 CV_SCORE: {cv_score}  TEST_SCORE: {test_score}'.format(
          model=name,
          cv_score=cv_score,
          test_score = test_score
      ))
      
      #models[name] = test_score
      
    return self
  
  def predict(self, X):
    
    return self.model.predict(X)
  
  def predict_probas(self, X):    
    
    return self.model.predict_proba(X)
  
  def metric(self, y_true, X_test):
    
    #labels = ['1', '0']
    
    cm = confusion_matrix(y_true, self.model.predict(X_test))
    print(cm)
    
    sns.heatmap(cm, annot=True)
    plt.show()
    
    tn, fp, fn, tp = cm.ravel()
    
    precision = tp/(tp + fp)
    
    recall = tp/(tp + fn)
    
    f1_score = 2* precision * recall/(precision + recall) 
                    
    
    print('Accuracy:', (tn + tp)/(tn + fp + fn + tp))
    
    print('Precision:', precision)
    
    print('Recall:', recall)
    
    print('f1 score:', f1_score)
    
    
    fpr, tpr, _ = roc_curve(y_true, self.predict_proba(X_test)[::,1])
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.plot(fpr, tpr)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC CURVE')
    plt.show() 