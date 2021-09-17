from django.shortcuts import render
from mycare.models import Survey
import pandas as pd
import json

# Create your views here.
def Chart(request):
    #DB안에 저장된 설문조사 결과 불러오기
    datas = Survey.objects.all()  
    
    lst = []
    for d in datas:
        dic = {}
        dic['성별'] = d.gender
        dic['연령'] = d.age
        dic['샴푸 사용빈도'] = d.shampoo
        dic['펌 주기'] = d.perm
        dic['염색 주기'] = d.dye
        dic['현재 모발상태'] = d.current_hair
        dic['현재 사용중인 제품'] = d.product
        dic['두피케어 선호여부'] = d.care_prefer
        dic['제품 선택시 고려사항'] = d.buying_point
        dic['label'] = d.label
        lst.append(dic)
    
    #데이터프레임으로 저장
    survey = pd.DataFrame(lst)
    #print(survey)
    
    #========[유형별 빈도 파이차트 작성]========
    type_dic = {}
    for lbl in set(survey['label']):
        df = survey[survey['label']==lbl].drop(['label'], axis=1)  #라벨컬럼 제외
        col_dic = {}
        for col in df.columns:
            x = df[col].value_counts()
            x_topn = x.head(4)
    
            if len(x) > 4:  #상위 4개만 표출 나머지는 묶음 처리 
                x_topn['remaining {0} items'.format(len(x) - 4)] = sum(x[4:])  
                x = x_topn
            data = list(x)
            label = list(x.index)
    
            col_datas = {
                'labels': label,
                'datasets': [{
                    'label': 'count',
                    'data': data,
                    'backgroundColor': [
                        'rgb(253, 111, 150)',
                        'rgb(255, 235, 161)',
                        'rgb(149, 218, 193)',
                        'rgb(111, 105, 172)',
                        'rgb(30, 49, 99)'
                    ],
                    'borderColor': [
                        'rgb(253, 111, 150)',
                        'rgb(255, 235, 161)',
                        'rgb(149, 218, 193)',
                        'rgb(111, 105, 172)',
                        'rgb(30, 49, 99)'
                    ],
                    'borderWidth': 1
                }]
            }
            col_dic[col] = col_datas
        type_dic[lbl] = col_dic
    
    pie_json = json.dumps(type_dic)  #json type으로 변환
    

    #=========[성별 두피유형 분포]=========
    type_male = survey[survey['성별'] == '남']
    m = type_male['label'].value_counts()  # counts
    m_percentage = type_male['label'].value_counts(normalize=True).mul(100).round(2)  # 백분율로

    female_type = survey[survey['성별'] == '여']
    fm = female_type['label'].value_counts()
    fm_percentage = female_type['label'].value_counts(normalize=True).mul(100).round(2)

    type_bysex_df = pd.concat([m, fm, m_percentage, fm_percentage], axis=1)
    type_bysex_df.columns = ["남성","여성","남성(%)", "여성(%)"]
    
    type_bysex_dic = {}
    for col in ['남성','여성']:
        x = type_bysex_df[col]
        x_topn = x.head(7)

        if len(x) > 7:  #상위 7개만 표출 나머지는 묶음 처리
                x_topn['remaining {0} items'.format(len(x) - 7)] = sum(x[7:])  
                x = x_topn
        data = list(x)
        label = list(x.index)
    
        type_bysex_datas = {
            'labels': label,
            'datasets': [{
                 'label': 'count',
                 'data': data,
                 'backgroundColor': [
                        'rgb(255, 222, 125)',
                        'rgb(246, 65, 108)',
                        'rgb(248, 243, 212)',
                        'rgb(0, 184, 169)',
                        'rgb(150, 186, 255)',
                        'rgb(111, 105, 172)',
                        'rgb(61, 8, 123)',
                        'rgb(185, 122, 149)'  
                ],
                 'borderColor': [
                        'rgb(255, 222, 125)',
                        'rgb(246, 65, 108)',
                        'rgb(248, 243, 212)',
                        'rgb(0, 184, 169)',
                        'rgb(150, 186, 255)',
                        'rgb(111, 105, 172)',
                        'rgb(61, 8, 123)',
                        'rgb(185, 122, 149)'        
                ],
                'borderWidth': 1
            }]
        }
        type_bysex_dic[col] = type_bysex_datas
    type_bysex_json = json.dumps(type_bysex_dic)  #json type으로 변환
    
    
    #========성별 샴푸 고르는 기준========
    male = survey[survey['성별'] == '남']
    mm = male['제품 선택시 고려사항'].value_counts(normalize=True).mul(100).round(2)
    choice_bysex = pd.DataFrame({'남성': mm}).T
    
    female = survey[survey['성별'] == '여']
    ff = female['제품 선택시 고려사항'].value_counts(normalize=True).mul(100).round(2)
    choice_bysex = choice_bysex.append(ff)
    choice_bysex.index = ['남성','여성']
    
    data1 = list(choice_bysex['세정력'])
    data2 = list(choice_bysex['두피자극'])
    data3 = list(choice_bysex['머리결'])
    data4 = list(choice_bysex['향'])
    data5 = list(choice_bysex['헹굼후느낌'])
    data6 = list(choice_bysex['가격'])

    choice_bysex_datas = {
        'labels': ['남성','여성'],
        'datasets': [{
            'label': '세정력',
            'data': data1,
            'backgroundColor': 'rgb(223, 46, 46)',
            'hoverBackgroundColor': 'rgb(223, 46, 46)',
            'borderWidth': 1,
            'stack': 'combined'
        },{
            'label': '두피자극',
            'data': data2,
            'backgroundColor': 'rgb(246, 209, 103)',
            'hoverBackgroundColor': 'rgb(246, 209, 103)',
            'borderWidth': 1,
            'stack': 'combined'      
        },{
            'label': '머리결',
            'data': data3,
            'backgroundColor': 'rgb(255, 247, 174)',
            'hoverBackgroundColor': 'rgb(255, 247, 174)',
            'borderWidth': 1,
            'stack': 'combined'        
        },{
            'label': '향',
            'data': data4,
            'backgroundColor': 'rgb(41, 127, 135)',
            'hoverBackgroundColor': 'rgb(41, 127, 135)',
            'borderWidth': 1,
            'stack': 'combined'        
        },{
            'label': '헹굼후느낌',
            'data': data5,
            'backgroundColor': 'rgb(81, 45, 109)',
            'hoverBackgroundColor': 'rgb(81, 45, 109)',
            'borderWidth': 1,
            'stack': 'combined'        
        },{
            'label': '가격',
            'data': data6,
            'backgroundColor': 'rgb(21, 0, 80)',
            'hoverBackgroundColor': 'rgb(21, 0, 80)',
            'borderWidth': 1,
            'stack': 'combined'        
        }]
    }
    choice_bysex_json = json.dumps(choice_bysex_datas)
    
    
    #========두피유형별 샴푸 고르는 기준========
    type1 = survey[survey['label'] == '양호']
    per1 = type1['제품 선택시 고려사항'].value_counts(normalize=True).mul(100).round(2)
    choice_byage_df = pd.DataFrame({'양호': per1}).T

    for i in ['건성','지성','민감성','지루성','염증성','비듬성','탈모성','복합성']:
        type_df = survey[survey['label'] == i]
        choice_byage_df = choice_byage_df.append(type_df['제품 선택시 고려사항'].value_counts(normalize=True).mul(100).round(2))

    choice_byage_df.index = ["양호","건성","지성","민감성","지루성","염증성","비듬성","탈모성","복합성"]
    choice_byage_df = choice_byage_df.fillna(0)
    
    label = list(choice_byage_df.index)
    data1 = list(choice_byage_df['세정력'])
    data2 = list(choice_byage_df['두피자극'])
    data3 = list(choice_byage_df['머리결'])
    data4 = list(choice_byage_df['향'])
    data5 = list(choice_byage_df['헹굼후느낌'])
    data6 = list(choice_byage_df['가격'])

    choice_byage_datas = {
        'labels': list(choice_byage_df.index),
        'datasets': [{
            'label': '세정력',
            'data': data1,
            'backgroundColor': 'rgba(63,103,126,1)',
            'hoverBackgroundColor': 'rgba(50,90,100,1)',
            'borderWidth': 1
        },{
            'label': '두피자극',
            'data': data2,
            'backgroundColor': 'rgba(163,11,126,1)',
            'hoverBackgroundColor': 'rgba(50,98,10,1)',
            'borderWidth': 1   
        },{
            'label': '머리결',
            'data': data3,
            'backgroundColor': 'rgba(63,103,16,1)',
            'hoverBackgroundColor': 'rgba(50,78,107,1)',
            'borderWidth': 1    
        },{
            'label': '향',
            'data': data4,
            'backgroundColor': 'rgba(63,103,126,1)',
            'hoverBackgroundColor': 'rgba(50,90,100,1)',
            'borderWidth': 1     
        },{
            'label': '헹굼후느낌',
            'data': data5,
            'backgroundColor': 'rgba(12,33,16,1)',
            'hoverBackgroundColor': 'rgba(50,100,11,1)',
            'borderWidth': 1
        },{
            'label': '가격',
            'data': data6,
            'backgroundColor': 'rgba(63,103,77,1)',
            'hoverBackgroundColor': 'rgba(5,9,100,1)',
            'borderWidth': 1       
        }]
    }
    choice_byage_json = json.dumps(choice_byage_datas)

    context = {'pie_json':pie_json, 'type_bysex_json':type_bysex_json, 'choice_bysex_json':choice_bysex_json,
               'choice_byage_json':choice_byage_json}
    return render(request, 'statistics.html', context)


def HealthInform(request):
    
    return render(request, 'healthInform.html')

