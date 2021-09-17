from django.shortcuts import render

# Create your views here.
def MainFunc(request):
    # pass
    return render(request, 'main.html')


def SurveyFunc(request):
    return render(request, 'survey.html')

# Survey_result_Func
def SurveyresultFunc(request):
    print("되는거니....?")
    if request.method == "POST":
        gender= request.POST.get("gender")
        age= request.POST.get("age")
        shampoo_count = request.POST.get("shampoo_count")
        now_hair=request.POST.getlist("now_hair[ ]")
        hair_product=request.POST.getlist("hair_product[ ]")
        perm = request.POST.get("perm")
        color_count= request.POST.get("color_count")
        shampoo_buy= request.POST.get("shampoo_buy")
        product_want= request.POST.get("product_want")
        
        now_hair=','.join(now_hair)
        print(now_hair)
        hair_product=','.join(hair_product)
        print(hair_product)
    return render(request, "surveyresult.html",{"hair_product":hair_product,"now_hair":now_hair,"gender": gender, "age":age, "shampoo_count":shampoo_count, "perm":perm, "color_count":color_count, "shampoo_buy":shampoo_buy, "product_want":product_want})
    

