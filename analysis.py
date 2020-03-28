'''
Summer Data Scientist Data Assessment
Crime and Education Lab New York
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
from statsmodels.discrete.discrete_model import Probit

#Part 1: Variable Creation
arrests = pd.read_csv('arrests.csv')
demo = pd.read_csv('demo.csv')
demo['bdate'] = pd.to_datetime(demo['bdate'], utc=False)
arrests['arrest_date'] = pd.to_datetime(arrests['arrest_date'], utc=False)
arrests_post = arrests[arrests['arrest_date'] >= '2010-01-01'].copy()
tr = pd.merge(arrests,
              arrests_post.rename(columns={'arrest_date':'date_post', 
                                            'arrest_id':'aid_post', 
                                            'law_code':'code_post'}), 
              on='person_id')

twoyear = tr[(tr['arrest_date'] >= tr['date_post']-pd.DateOffset(years=2)) & (tr['arrest_id'] != tr['aid_post'])]
sixmonth = tr[(tr['arrest_date'] >= tr['date_post'] - pd.DateOffset(months=6)) & (tr['arrest_id'] != tr['aid_post'])]
twoyear =  twoyear.groupby(['aid_post', 'law_code']).size().unstack().reset_index().fillna(0)
twoyear.rename(columns = {'aid_post':'arrest_id', 'felony': 'fel_2y', 'misdemeanor': 'mis_2y'}, inplace=True)
sixmonth = sixmonth.groupby(['aid_post', 'law_code']).size().unstack().reset_index().fillna(0)
sixmonth.rename(columns = {'aid_post':'arrest_id', 'felony': 'fel_6m', 'misdemeanor': 'mis_6m'}, inplace=True)
year_ahead = tr[(tr['arrest_date'] >= tr['date_post']) & (tr['arrest_id'] != tr['aid_post'])]
year_ahead = year_ahead[year_ahead['arrest_date'] <= year_ahead['date_post'] + pd.DateOffset(years=1)]
year_ahead = year_ahead.groupby(['aid_post', 'law_code']).size().unstack().reset_index().fillna(0)
year_ahead.rename(columns = {'aid_post':'arrest_id', 'felony': 'felony_arrests' }, inplace=True)
year_ahead[['arrest_id', 'felony_arrests']]
year_ahead['re_arrest'] = np.where(year_ahead['felony_arrests'] > 0,1,0)


arrests_post = arrests_post.merge(twoyear, on='arrest_id', how='left').fillna(0)
arrests_post = arrests_post.merge(sixmonth, on='arrest_id', how='left').fillna(0)
arrests_post = arrests_post.merge(year_ahead[['arrest_id', 're_arrest']], on='arrest_id', how='left').fillna(0)

arrests_post

final = pd.merge(arrests_post, demo, on='person_id')
final['age'] = ((final['arrest_date'] - final['bdate']) / np.timedelta64(1, 'Y')).round().astype(int)
final.drop(['bdate', 'arrest_id',], axis=1, inplace=True)

final.gender.unique()
final.loc[final['gender'] == 'male', 'gender'] = 'M'
final.loc[final['gender'] == 'female', 'gender'] = 'F'
print(final.gender.unique())
final

#Part 2: Statistical Analysis » Program Evaluation
treat = pd.read_csv('treatment_assignment.csv')
treat.rename(columns={'precinct' : 'home_precinct'}, inplace=True)

first = final.groupby('person_id').agg({'arrest_date':min}).reset_index()
first =  first.merge(final, on=['person_id', 'arrest_date'])

print('Treatment-control precincts: {}'.format(len(treat.home_precinct.unique())))
print('Arrests post-implementation precincts: {}'.format(len(first.home_precinct.unique())))

data_eval = first.merge(treat, on=['home_precinct'], how='right')
data_eval.drop(['person_id', 'arrest_date'], axis=1, inplace=True)
data_eval

data_eval['gender'] = np.where(data_eval['gender']== 'M', 1, 0)
data_eval['treatment_status'] = np.where(data_eval['treatment_status']== 'control', 0, 1)
data_eval['law_code'] = np.where(data_eval['law_code']== 'felony', 1, 0)

IND_VARS = ['treatment_status', 'age', 'gender', 'law_code', 'fel_2y', 'mis_2y', 'fel_6m', 'mis_6m']
all_ = sm.add_constant(data_eval[IND_VARS])
model1 = sm.OLS(data_eval['re_arrest'], all_).fit(cov_type='HC1')
model1.summary()

plt.figure(figsize=(10,6))
sns.scatterplot(data_eval['fel_6m'],data_eval['re_arrest'], label='Real values')
sns.scatterplot(data_eval['fel_6m'],model1.fittedvalues, label='Estimated values')
plt.xlabel("Prior felony arrests (in the last 6 months)")
plt.ylabel("Felony re-arrest")
plt.show()

probitm = Probit(data_eval['re_arrest'], all_).fit()
probitm.summary()


plt.figure(figsize=(10,6))
sns.scatterplot(data_eval['fel_6m'],data_eval['re_arrest'], label='Real values')
sns.scatterplot(data_eval['fel_6m'],model1.fittedvalues, label='Estimated values with OLS')
sns.scatterplot(data_eval['fel_6m'],probitm.predict(all_), label='Estimated values with Probit')
plt.xlabel("Prior felony arrests (in the last 6 months)")
plt.ylabel("Felony re-arrest")
plt.show()
