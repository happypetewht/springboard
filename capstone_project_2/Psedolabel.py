
from scipy.sparse import vstack
from sklearn.metrics import roc_curve, auc, classification_report, confusion_matrix, roc_auc_score
import seaborn as sns

class Pseudolabel:
  
  def __init__(self, model, unlabel_data, sample_rate=0.3):
    
    self.model = model
    self.unlabel_data = unlabel_data
    self.sample_rate = sample_rate

   
  def get_params(self, deep=True):
    return {
            "sample_rate": self.sample_rate,            
            "model": self.model,
            "unlabel_data": self.unlabel_data,
           
        }
    
  def set_params(self, **parameters):
    for parameter, value in parameters.items():
            setattr(self, parameter, value)
    return self
  


  def fit(self, X, y):
    
    augmented_X, augmented_y = self.create_augment_data(X, y)
    
    self.model.fit(augmented_X, augmented_y)
    
    return self
  
  def create_augment_data(self, X, y):
    
    sample_number = int((self.unlabel_data.shape[0]) * self.sample_rate)
    
    sample_row =  np.random.choice(range(self.unlabel_data.shape[0]), sample_number, replace=False)
    
    sample_unlabel = self.unlabel_data[sample_row]
    
    model = self.model.fit(X, y)
    
    pseudo_data = model.predict(sample_unlabel)
      
      
    aug_X = vstack([X, sample_unlabel])
    
    aug_y = np.concatenate([y, pseudo_data])
    
    return aug_X, aug_y
  
  def predict_proba(self, X):
    
 
    return self.model.predict_proba(X)
  
  def predict(self, X):
    
 
    return self.model.predict(X)
  
  def get_model_name(self):

      
    return self.model.__class__.__name__
  
  def score(self, X_test, y_test):
    
    return self.model.score(X_test, y_test)
  
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



    