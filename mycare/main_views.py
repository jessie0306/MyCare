from django.shortcuts import render
from PIL import Image
import os
import csv
import pandas as pd
import tensorflow as tf
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
import json

# Create your views here.
def MainFunc(request):
    return render(request, 'main.html')

def ImageInputFunc(request):
    return render(request, 'imageinput.html')

def ImageResultFunc(request):
    image = request.POST.get('fileInput')
    
    # 이미지 이동시키기C:/Users/acorn/Desktop/최종프젝/dataset/features
    # path = "C:/Users/acorn/Desktop/최종프젝/dataset/features"
    path = "C:/work/유형별 두피 이미지/Validation_image"
    img_path = os.path.join(path, image)
    # 이미지 열기
    im = Image.open(img_path)
 
    # 이미지 크기 출력
    print(im.size)
 
    # 이미지 PNG로 저장     
    im.save('care/mycare/static/images/image1.jpg')
    """
    # json 파일 읽어서 DataFrame화 하기(validation)
    pd.set_option('max_columns', None)
    # C:/Users/acorn/Desktop/최종프젝/유형별 두피 이미지/Validation/라벨링
    path = 'C:/Users/acorn/Desktop/최종프젝/유형별 두피 이미지/Validation/라벨링/'
    file_list = os.listdir(path)
    file_list_py = [file for file in file_list if file.endswith('.json')]
    
    import json
    
    dict_list = []
    for i in file_list_py:
        for line in open((path+i),"r"):
            dict_list.append(json.loads(line))
    df = pd.DataFrame(dict_list)
    df['image_file_name'] = df['image_file_name'].str.replace('.jpg','_META.json')
    print(df.head(3))
    print("df길이:", len(df)) # 23568
    
    # json파일끼리 1:1만들어주기(meta)
    # C:/Users/acorn/Desktop/최종프젝/유형별 두피 이미지/Meta/META_DATA/
    path = "C:/Users/acorn/Desktop/최종프젝/유형별 두피 이미지/Meta/META_DATA/" 
    
    dict_list2 = []
    for i in range(len(df)):
        file_list = df['image_file_name'][i]
        img_path = os.path.join(path, file_list)
        with open(img_path, "r", encoding='UTF8') as f:
            contents = json.loads(f.read())
            dict_list2.append(contents)
    df2 = pd.DataFrame(dict_list2)
    print(df2.head(3))
    print("df2길이:", len(df2)) # 23568
    
    # 0->0, 1,2,3->1로 바꾸는 작업
    df['value_1'] = df['value_1'].map({'0':0,'1':1,'2':1,'3':1})
    df['value_2'] = df['value_2'].map({'0':0,'1':1,'2':1,'3':1})
    df['value_3'] = df['value_3'].map({'0':0,'1':1,'2':1,'3':1})
    df['value_4'] = df['value_4'].map({'0':0,'1':1,'2':1,'3':1})
    df['value_5'] = df['value_5'].map({'0':0,'1':1,'2':1,'3':1})
    df['value_6'] = df['value_6'].map({'0':0,'1':1,'2':1,'3':1})
    df['구분'] = '복합성'


    # 구분 지정
    # +  : 123
    # -   : 0
    # +- : 0123     
    for i in range(len(df)):
      if df.iloc[i][2:8].sum() == 0:
        df['구분'][i] = '양호'
      elif (df['value_1'][i] == 1) & (df['value_2'][i] == 0) & (df['value_3'][i] == 0) & (df['value_4'][i] == 0) & (df['value_5'][i] == 0) & (df['value_6'][i] == 0):
        df['구분'][i] = '건성'
      elif (df['value_1'][i] == 0) & (df['value_2'][i] == 1) & (df['value_3'][i] == 0) & (df['value_4'][i] == 0) & (df['value_5'][i] == 0) & (df['value_6'][i] == 0):
        df['구분'][i] = '지성'
      elif (df['value_1'][i] in [0,1]) & (df['value_2'][i] == 0) & (df['value_3'][i] == 1) & (df['value_4'][i] == 0) & (df['value_5'][i] == 0) & (df['value_6'][i] == 0):
        df['구분'][i] = '민감성'
      elif (df['value_1'][i] in [0,1]) & (df['value_2'][i] == 1) & (df['value_3'][i] == 1) & (df['value_4'][i] == 0) & (df['value_5'][i] in [0,1]) & (df['value_6'][i] == 0):
        df['구분'][i] = '지루성'
      elif (df['value_1'][i] in [0,1]) & (df['value_2'][i] in [0,1]) & (df['value_3'][i] == 0) & (df['value_4'][i] == 1) & (df['value_5'][i] in [0,1]) & (df['value_6'][i] == 0):
        df['구분'][i] = '염증성'
      elif (df['value_1'][i] in [0,1]) & (df['value_2'][i] in [0,1]) & (df['value_3'][i] == 0) & (df['value_4'][i] == 0) & (df['value_5'][i] == 1) & (df['value_6'][i] == 0):
        df['구분'][i] = '비듬성'
      elif (df['value_1'][i] == 0) & (df['value_2'][i] == 0) & (df['value_3'][i] == 0) & (df['value_4'][i] == 0) & (df['value_5'][i] == 0) & (df['value_6'][i] == 1):
        df['구분'][i] = '탈모성'
      else:
        df['구분'][i] = '복합성'
    df3 = pd.concat([df2, df['구분']], axis=1, sort=False)
    df3 = pd.concat([df3, df['image_file_name']], axis=1, sort=False)
    print(df3.head(3))
    df3.to_csv('care/mycare/static/images/df3.csv', encoding='euc-kr')
    """
    df3 = pd.read_csv('care/mycare/static/images/df3.csv', encoding='euc-kr')
    print(df3.head(3))
    print(df3['image_file_name'])
    
    # 이미지 이름에 따라 두피유형 다르게 출력하기  
    image = image.replace('.jpg','_META.json')
    a = df3.loc[(df3['image_file_name']==image)]
    b = a['구분'].values
    
    
    # 모델 불러오기
    img = load_img(img_path, target_size=(250, 250))
    img_tensor = img_to_array(img)
    
    # 차원확장 (3D -> 4D)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    print(img_tensor.shape)
    
    # 정규화
    img_tensor /= 255.
    model = tf.keras.models.load_model('care/mycare/static/images/mobile_model_62.h5')  
    
    # 모델의 예측값, 예측값에 따라 두피유형 부여
    print('실제값 : ', a['구분'].values)
    print('예측값 : ', np.argmax(model.predict(img_tensor)))
    if np.argmax(model.predict(img_tensor)) == 0:
        b = '양호'
    elif np.argmax(model.predict(img_tensor)) == 1:
        b = '건성'   
    elif np.argmax(model.predict(img_tensor)) == 2:
        b = '지성'   
    elif np.argmax(model.predict(img_tensor)) == 3:
        b = '민감성'   
    elif np.argmax(model.predict(img_tensor)) == 4:
        b = '지루성'   
    elif np.argmax(model.predict(img_tensor)) == 5:
        b = '염증성'   
    elif np.argmax(model.predict(img_tensor)) == 6:
        b = '비듬성'   
    elif np.argmax(model.predict(img_tensor)) == 7:
        b = '탈모성'   
    else:
        b = '복합성'
           
    return render(request, 'imageresult.html',{'A':b, 'pie_json':json})