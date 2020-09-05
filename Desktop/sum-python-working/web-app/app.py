from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
import pandas as pd 
import numpy as np
import os 
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

df = pd.read_excel("final.xlsx")
Final=df.copy()
Final = Final[['Defect_desc','Type of Defect']]
df = df['Defect_desc']
df = pd.DataFrame({'Desc':df})

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():
      SearchStr=form.num1.data
      TOD="Business Logic"
          
    k=0
          
    for a in df.index:

        X=df['Desc'][a]
        # tokenization 


        X_list = word_tokenize(X.lower())  
        Y_list = word_tokenize(SearchStr.lower()) 


      # Fetching all stop words
        sw = stopwords.words('english')  
        V1 =[];V2 =[] 


        # Stop word removal 
        X_set = {lemmatizer.lemmatize(w) for w in X_list if not w in sw}  
        Y_set = {lemmatizer.lemmatize(w) for w in Y_list if not w in sw} 


        UV = X_set.union(Y_set)  
        for w in UV:


            if w in X_set: V1.append(1) 


            else: V1.append(0) 
            if w in Y_set: V2.append(1) 
            else: V2.append(0) 
            c = 0
       
            

            
    # Calculating cosine similarity  
        for i in range(len(UV)): 


          c+= V1[i]*V2[i] 
         
        cosine = c / float((sum(V1)*sum(V2))**0.5) 
        
        
        Final.loc[Final['Defect_desc']== X,'Similarity']=cosine
        df_Final=Final.copy()
        

          #sum=form.num1.data+form.num2.data
        df_Final=Final[(Final['Similarity']>0) & (Final['Type of Defect']==TOD)].sort_values(by='Similarity',ascending=False).head(3).head(3)
        #print(df_Final)
        df_Final=pd.DataFrame.to_html(df_Final)
        #print(df_Final)
        form.abc=df_Final
        #print(form.abc)
        pd.show_versions()
    return render_template('index.html', form=form)         

       
       







