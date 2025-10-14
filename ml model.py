import Data_Visualization as dv
import Data_Extraction_and_Cleaning as dec
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt


dffh = dec.fighthistory1
avg_strikes_per_round = []

X = dffh[['SLPM', 'avg_Str_fighter', 'Round', 'TIM']]
y = dffh['Str_fighter']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#train model
lm = LinearRegression()
#lm.fit(given, expected)
test = lm.fit(X_train, y_train)


#predictions
predictions = lm.predict(X_test)
#print(predictions)

mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
sns.scatterplot(x=predictions, y=y_test)
plt.xlabel('Predictions')
plt.show()
