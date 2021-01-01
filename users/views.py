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
from plotly.offline import plot
def dashboard(request):
    df = pd.read_csv("users/data/eyeonwebdataset.csv")
    rs = df.groupby("WebAddress")["ResponseTime"].agg('sum')
    categories = list(rs.index)
    values = list(rs.values)
    table_content = df.to_html(index=None)
    table_content = table_content.replace("","")
    table_content = table_content.replace('class="dataframe"',"class='table table-striped'")
    table_content = table_content.replace('border="1"',"")
    
    context = {"categories": categories, 'values': values, 'table_data':table_content}
    return render(request, 'users/dashboard.html', context=context)

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

def datascrap(request):
    weblist = pd.read_csv('users/data/weblist.csv') 
    datasetfilename = MEDIA_ROOT+ "users/data/eyeonwebdataset.csv"
    df = pd.read_csv(datasetfilename)
    
    #function to access the Web and ask for status
    def writetocsv(filename):
        start_time = time.time()
        df = pd.DataFrame(columns = ['WebAddress', 'AccessTime', 'Status','ResponseTime']) 
        for web in weblist.index:
            try:
                page = requests.get(weblist['WebList'][web])
            except requests.exceptions.ConnectionError:
                page.status_code = "400"
            new_row = {'WebAddress': str(weblist['WebList'][web]) , 'AccessTime': str(datetime.now()) , 'Status': str(page.status_code), 'ResponseTime':time.time() - start_time}
            df = df.append(new_row, ignore_index=True)

    #program that call write to csv every 5 minutes
    import sched, time
    s = sched.scheduler(time.time, time.sleep)
    def do_something(sc): 
        print("Doing stuff...")
        writetocsv(datasetfilename)
        s.enter(300, 1, do_something, (sc,))

    s.enter(300, 1, do_something, (s,))
    s.run()           
    df.to_csv(filename, mode='a', header=False)


    return render(request, 'plotly.html', context={'plot_div':plot_div})

def datagraph(request):
    datasetfilename = "users/data/eyeonwebdataset.csv"
    df = pd.read_csv(datasetfilename)
    x_data="WebAddress"
    y_data="ResponseTime"
    plot_div=plot(px.scatter(df, x_data, y_data, color="StatusCode",hover_data=['StatusCode'],title='Web Status Response Time'), output_type='div')
    plot_div

    return render(request, 'users/plotly.html', context ={'plot_div': plot_div,"df":df,"x_data":x_data,"y_data":y_data})


def datagraph_date(request):
    datasetfilename = "users/data/eyeonwebdataset.csv"
    df = pd.read_csv(datasetfilename)
    x_data="AccessTime"
    y_data="ResponseTime"
    plot_div_date = plot(px.line(df, x_data, y_data, color='WebAddress',hover_data=['StatusCode'],title='Web Monitor Access Time'), output_type='div')
    plot_div_date

    return render(request, 'users/plotly.html', context ={'plot_div_date': plot_div_date,"df":df,"x_data":x_data,"y_data":y_data})
