
from keras.models import Model
from keras.layers import Embedding, Dropout
from keras.layers import Dense, Input, LSTM, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras import initializers, regularizers, constraints, optimizers, layers
from keras.layers import Dropout, BatchNormalization, ELU
from scipy import sparse
from scipy.sparse import vstack
from sklearn.metrics import roc_curve, auc, classification_report, confusion_matrix, roc_auc_score
import seaborn as sns

class Pseudolabel_NN:
  
  def __init__(self, unlabel_data, sample_rate=0.3, batch_size=128):
    
    self.unlabel_data = unlabel_data
    self.sample_rate = sample_rate
    self.batch_size = batch_size

   
  def get_params(self, deep=True):
    return {
            "sample_rate": self.sample_rate,            
            "unlabel_data": self.unlabel_data,
           
        }
    
  def set_params(self, **parameters):
    for parameter, value in parameters.items():
            setattr(self, parameter, value)
    return self
  


  def fit(self, model, X, y):
    
    augmented_X, augmented_y = self.create_augment_data(model, X, y)
    
    model.fit(augmented_X, augmented_y, batch_size=self.batch_size, epochs=2, validation_split=0.1)
    
    self.model = model
    
    return self
  
  def create_augment_data(self, model, X, y):
    
    sample_number = int((self.unlabel_data.shape[0]) * self.sample_rate)
    
    sample_row =  np.random.choice(range(self.unlabel_data.shape[0]), sample_number, replace=False)
    
    sample_unlabel = self.unlabel_data[sample_row]
    
    model.fit(X, y, batch_size=self.batch_size, epochs=2, validation_split=0.1)
    
    pseudo_data = model.predict(sample_unlabel, batch_size=1024, verbose=1)
    
    pseudo_data[pseudo_data >= 0.5] = 1
    pseudo_data[pseudo_data < 0.5] = 0
    
    if sparse.issparse(X):
      
      aug_X = vstack([X, sample_unlabel])
      
    if isinstance(X, np.ndarray):
      
      aug_X = np.concatenate([X, sample_unlabel])    
    
    aug_y = np.concatenate([y, np.transpose(pseudo_data)[0]])
    
    return aug_X, aug_y
  
  def predict_proba(self, X):   
     
 
    return self.model.predict(X, batch_size=1024, verbose=1)
  
  def predict(self, y_pred):
    
    y_prob = y_pred.copy()
    
    y_prob[y_prob >= 0.5] = 1
    y_prob[y_prob < 0.5] = 0
 
    return y_prob

  def metric(self, y_true, y_pred, y_prob):

      #labels = ['1', '0']

      cm = confusion_matrix(y_true, y_pred)
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


      fpr, tpr, _ = roc_curve(y_true, y_prob)
      plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
      plt.plot(fpr, tpr)
      plt.xlabel('False Positive Rate')
      plt.ylabel('True Positive Rate')
      plt.title('ROC CURVE')
      plt.show()

  def nn_emb(self, weights, embed_size):  
    text_input = Input(shape=(embed_size,), name='embed_input')
    x = Embedding(weights.shape[0], weights.shape[1],
                    weights=[weights], input_length=embed_size,
                    trainable=False)(text_input)    
    x = LSTM(50, dropout=0.4, recurrent_dropout=0.1, return_sequences=True)(x)
    x = GlobalMaxPool1D()(x)
    x = Dense(50, activation="relu", kernel_regularizer=regularizers.l2(0.01))(x)
    x = Dropout(0.4)(x)
    x = Dense(1, activation='sigmoid')(x) 
    model = Model(inputs=text_input, outputs=x)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

  def nn_emb_batch(self, weights, embed_size):  
    text_input = Input(shape=(embed_size,), name='embed_input')
    x = Embedding(weights.shape[0], weights.shape[1],
                    weights=[weights], input_length=embed_size,
                    trainable=False)(text_input)    
    x = LSTM(50, dropout=0.4, recurrent_dropout=0.1, return_sequences=False)(x)
    x = Dense(300, activation='relu', kernel_regularizer=regularizers.l2(0.01))(x)
    x = Dropout(0.4)(x)
    x = BatchNormalization()(x)
    x = ELU()(x)
    x = Dense(1, activation="sigmoid")(x)

    model = Model(inputs=text_input, outputs=x)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model
  
  def dnn(self, X_train):

    text_input = Input(shape=(X_train.shape[1],), dtype='float32', sparse=True)
    x = Dense(8192, activation='relu', kernel_regularizer=regularizers.l2(0.01))(text_input)
    x = Dense(2056, activation='relu')(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    x = Dense(1, activation='sigmoid')(x)

    model = Model(text_input, x)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

