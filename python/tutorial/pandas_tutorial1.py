
# coding: utf-8

# In[2]:

import csv as csv
import numpy as np

csv_file_object = csv.reader(open('data/train.csv', 'rb')) 
header = csv_file_object.next() 
data=[] 

for row in csv_file_object:
    data.append(row)
data = np.array(data) 


# In[3]:

data[0:15,5]


# In[4]:

type(data[0::,5]) 


# In[5]:

import pandas as pd


# In[6]:

df = pd.read_csv('data/train.csv', header=0)


# In[7]:

df.head(3)


# In[8]:

df.dtypes


# In[9]:

df.info()


# In[10]:

df.describe()


# In[11]:

df.Age[0:10]


# In[12]:

type(df['Age'])


# In[13]:

df.Age.median()


# In[14]:

df[df['Age'] > 60][['Sex', 'Pclass', 'Age', 'Survived']]


# In[15]:

for i in range(1,4):
    print i, len(df[ (df['Sex'] == 'male') & (df['Pclass'] == i) ])


# In[19]:

df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)
df.head(3)


# In[ ]:



