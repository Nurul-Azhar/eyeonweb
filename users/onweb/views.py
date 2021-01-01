from django.shortcuts import render
import pandas as pd
from eyeonwebs.settings import MEDIA_URL,MEDIA_ROOT
from django.http import HttpResponse
from django.conf.urls.static import static
from django.views.generic import TemplateView, View 

import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

# Create your views here.
def index(request):
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
    
    context = {"categories": categories, 'values': values, 'table_data':table_content,"x":x}
    return render(request, 'users/dashboard.html', context=context)

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
        writetocsv(datasetfilename)
        s.enter(300, 1, do_something, (sc,))

    s.enter(300, 1, do_something, (s,))
    s.run()           
    df.to_csv(filename, mode='a', header=False)

    return render(request, 'plotly.html', context={'plot_div':plot_div})

def datagraph(request):
    datasetfilename = "data/eyeonwebdataset.csv"
    df = pd.read_csv(datasetfilename)
    x_data="WebAddress"
    y_data="ResponseTime"
    plot_div=plot([px.scatter(df, x_data, y_data, color="StatusCode",hover_data=['StatusCode'],title='Web Status Response Time')], output_type='div')
    plot_div

    return render(request, 'users/plotly.html', context ={'plot_div': plot_div,"df":df,"x_data":x_data,"y_data":y_data})

class PlotlyChartView(TemplateView):
    def get(self, request, *args, **kwargs):
        x_data=df["WebAddress"]
        y_data=df["ResponseTime"]
        plot_div = plot([px.scatter(
            x=x_data, 
            y=y_data, 
            color="StatusCode",
            hover_data=df['StatusCode'],
            title='Web Status Response Time'
            )], output_type='div')
        plot_div.show()

        return render(request, 'plotly.html', context={'plot_div':plot_div})