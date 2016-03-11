import csv as csv

csv_file_object = csv.reader(open('data/train.csv', 'rb'))
header = csv_file_object.next()
data=[]

for row in csv_file_object:
    data.append(row)
data = np.array(data)
data[0:15,5]
type(data[0::,5])


import numpy as np
import pandas as pd
df = pd.read_csv('data/train.csv', header=0)
df.head(3)
df.dtypes
df.info()
df.describe()
df.Age[0:10]
type(df['Age'])
df.Age.median()

df[df['Age'] > 60][['Sex', 'Pclass', 'Age', 'Survived']]

for i in range(1,4):
    print i, len(df[ (df['Sex'] == 'male') & (df['Pclass'] == i) ])

df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)
df.head(3)

#
median_ages = np.zeros((2,3))
for i in range(0, 2):
    for j in range(0, 3):
        median_ages[i,j] = df[(df['Gender'] == i) & \
                              (df['Pclass'] == j+1)]['Age'].dropna().median()

median_ages

#
df['AgeFill'] = df['Age']
df[ df['Age'].isnull() ][['Gender','Pclass','Age','AgeFill']].head(10)

#
for i in range(0, 2):
    for j in range(0, 3):
        df.loc[ (df.Age.isnull()) & (df.Gender == i) & (df.Pclass == j+1),\
                'AgeFill'] = median_ages[i,j]

#
df['AgeIsNull'] = pd.isnull(df.Age).astype(int)

df['Age*Class'] = df.AgeFill * df.Pclass

#
df['Age*Class'].hist()
P.show

#
df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1)
df = df.drop(['Age'], axis=1)
train_data = df.values
train_data