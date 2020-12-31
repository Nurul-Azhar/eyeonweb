from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from django.views.generic import TemplateView
# Create your views here.
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

def dashboard(request):
    # weblist = pd.read_csv('data/weblist.csv') 
    # dataset filename
#     # datasetfilename = "data/eyeonwebdataset.csv"
#     df = pd.read_csv("data/eyeonwebdataset.csv")
    
#     # fig = px.scatter(df, x="WebAddress", y="ResponseTime", color="StatusCode",hover_data=['StatusCode'],title='Web Status Response Time')
#     # fig.show()

#     return render(request, 'plotly.html', context={'plot_div':plot_div})

# class PlotlyChartView(TemplateView):
#     def get(self, request, *args, **kwargs):
#         x_data="WebAddress"
#         y_data="ResponseTime"
#         plot_div = plot([go.Scatter(
#             x=x_data,
#             y=y_data,
#             color="StatusCode",
#             name='Web Status Response Time',
#             opacity=0.8,
#             hover_data=['StatusCode']
#         )], output_type='div')

#         return render(request, 'plotly.html', context={'plot_div':plot_div})
    
# def index(request):
    # df = pd.read_csv(r'data/eyeonwebdataset.csv')
    df = pd.read_csv("users/data/eyeonwebdataset.csv")
    rs = df.groupby("WebAddress")["ResponseTime"].agg('sum')
    categories = list(rs.index)
    values = list(rs.values)
    x = 1
    table_content = df.to_html(index=None)
    table_content = table_content.replace("","")
    table_content = table_content.replace('class="dataframe"',"class='table table-striped'")
    table_content = table_content.replace('border="1"',"")
    
    context = {"categories": categories, 'values': values, 'table_data':table_content}
    return render(request, 'users/dashboard.html', context=context)

    # return render(request, "users/dashboard.html",{"x":x})

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
