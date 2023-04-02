from fastapi import FastAPI, Form, Request,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import pickle
import json

import warnings
warnings.filterwarnings('ignore')

pred_model=pickle.load(open('stoke_prediction.pkl','rb'))
scalar=pickle.load(open('scaler.pkl','rb'))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')



@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/predict',response_class=HTMLResponse)
async def predict(request: Request,gender:str=Form(...),
                  Age: str = Form(...),
                  hypertension:str=Form(...),
                  heart:str=Form(...),
                  married:str=Form(...),
                  work:str=Form(...),
                  res:str=Form(...),
                  glu:float=Form(...),
                  bmi:float=Form(...),
                  som:str=Form(...)):
    if (gender=='Male'):
        gender_male=1
        gender_other=0
    elif (gender=='other'):
        gender_male=0
        gender_other=1
    else:
        gender_male=0
        gender_other=0

    if (hypertension=='Yes'):
        hypertension=1
    else:
        hypertension=0

    if (heart=='Yes'):
        heart=1
    else:
        heart=0

    if (married=='Yes'):
        married=1
    else:
        married=0

    if (res=='Rural'):
        res=1
    else:
        res=0

    if (work=='Private'):
        work_type_Private=1
        work_type_Never_worked=0
        work_type_Self_employed =0
        work_type_children=0
    elif(work=='Self-employed'):
        work_type_Private=0
        work_type_Never_worked=0
        work_type_Self_employed=1
        work_type_children=0
    elif(work=='Never_worked'):
        work_type_Private=0
        work_type_Never_worked=1
        work_type_Self_employed=0
        work_type_children=0
    elif(work=='children'):
        work_type_Private=0
        work_type_Never_worked=0
        work_type_Self_employed=0
        work_type_children=1
    else:
        work_type_Private=0
        work_type_Never_worked=0
        work_type_Self_employed=0
        work_type_children=0

    if(som=='Formerly Smoked'):
        formerly_smoked=1
        never_smoked=0
        smokes=0
    elif(som=='Never Smoked'):
        formerly_smoked=0
        never_smoked=1
        smokes=0
    elif(som=='Smokes'):
        formerly_smoked=0
        never_smoked=0
        smokes=1
    else:
        formerly_smoked=0
        never_smoked=0
        smokes=0


    prediction_value=[[Age,
                    hypertension,
                    heart,
                    glu,
                    bmi,
                    gender_male,
                    gender_other,
                    married,
                    work_type_Private,
                    work_type_Never_worked,
                    work_type_Self_employed,
                    work_type_children,
                    res,
                    formerly_smoked,
                    never_smoked,
                    smokes]]
    #print(Age)
    #print(hypertension)
    #print(bmi)
    #print(gender_male)
    
    new_scale_data=scalar.transform(prediction_value)
    #print(new_scale_data)
    result=pred_model.predict(new_scale_data)
    if result == 1:
        return  templates.TemplateResponse('index.html', context={'request': request, 'prediction_message': "Yes, you may be likely to have a stroke. Please see a doctor."})
    elif result == 0:
        return templates.TemplateResponse('index.html', context={'request': request, 'prediction_message': "No, you are not likely to have a stroke"})

    