import Data_Visualization as dv
import Data_Extraction_and_Cleaning as dec
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt


dffh = dec.fighthistory1
X = dffh[['Kd_fighter', 'Td_fighter', 'Round']]
y = dffh['Str_fighter']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#train model
lm = LinearRegression()
#lm.fit(given, expected)
test = lm.fit(X_train, y_train)

#predictions
predictions = lm.predict(X_test)
print(predictions)
sns.scatterplot(x=predictions, y=y_test)
plt.xlabel('Predictions')
plt.show()