from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
import urllib.parse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
plot_data = ""

class Calc(db.Model):
    plt.switch_backend('Agg')
    id = db.Column(db.Integer, primary_key=True)
    csv_data = db.Column(db.String)
    plot_data = db.Column(db.String)

def generate_plot(yoi, plotList):
    fig, ax = plt.subplots()

    ax.plot(range(yoi + 1), plotList)
    ax.ticklabel_format(style='plain')
    ax.set_xlabel("Years")
    ax.set_ylabel("Value of Investment")

    img=io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    
    plt.close(fig)

    return plot_data
    
    
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #initil fields
        try:
            principal = int(request.form["principal"])
            yoi = int(request.form["yoi"])
            interest = 1 + (float(request.form["interest"])/100)
            contribution = int(request.form["contribution"])
            compounding_periods = int(request.form["compound"])
            
            dataList = [principal] #to hold each value after each compounding period
            
            #calculate investments
            returnVal = principal
            for period in range(yoi*compounding_periods):
                returnVal= (returnVal*interest)+contribution
                dataList.append(int(returnVal))
                
            #intialize plot list, to be turned into a csv File and used by matplotlib to create a graph
            plotList = [n for n in dataList if dataList.index(n) % compounding_periods == 0]
            
            
            plotIndex = [i for i in range(len(plotList))] ##list of indexes of plotList
            
            dfDict = {"After Year:": plotIndex, "Balance": plotList}
            
            
            df = pd.DataFrame(dfDict)
            csv_data = df.to_csv(index=False)        
        
            
            plot_data = generate_plot(yoi, plotList)

            new_entry = Calc(csv_data=csv_data, plot_data=plot_data)
            
            db.session.add(new_entry)
            db.session.commit()
        except:
            print("Something went wrong")
        
    entry = Calc.query.order_by(Calc.id.desc()).first()
    print(entry)
    return render_template('index.html', entry=entry)
if __name__ == '__main__':
    app.run(debug=True)