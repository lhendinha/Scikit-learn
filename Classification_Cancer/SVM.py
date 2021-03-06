#Bibliotecas
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import confusion_matrix, auc, roc_curve, roc_auc_score
from sklearn.model_selection import GridSearchCV

#DataFrame
df = pd.read_csv('cancer.csv')
print(len(df.columns))

df.head()

df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})


#Pre-analise
df.drop(['id'], axis=1, inplace=True)

df.isnull().sum()

#X e y
x = df.iloc[:, 1:28].values
y = df.iloc[:, 0].values

#Divisão de Treino e Teste
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

#Normalizacao dos dados
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#Modelo
clf = svm.SVC()

params = {'kernel': ['linear', 'poly', 'rbf', 'sigmoid']}

grid = GridSearchCV(estimator = clf,   
                    param_grid = params, 
                    cv = 20)

#Treino
grid.fit(x_train, y_train)

#Analise do modelo
pd.DataFrame(grid.cv_results_)
pd.DataFrame(grid.cv_results_)[['params','rank_test_score','mean_test_score']]
grid.best_params_

grid.best_score_

y_preds = grid.predict(x_test)

#Metrica
print(confusion_matrix(y_test, y_preds))
fpr, tpr, thresholds = roc_curve(y_test, y_preds)
auc(fpr, tpr)
roc_auc_score(y_test, y_preds)