from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/', methods=['GET'])
def plot():
    from pandas_datareader import data
    import datetime, datedelta
    from bokeh.plotting import figure, show, output_file
    from bokeh.models.annotations import Title
    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.models import ColumnDataSource, HoverTool
    from flask import Flask, flash, request, redirect, url_for

    def inc_dec(c, o):

        if c > o:
            return 'Increase'
        elif c < o:
            return 'Decrease'
        else:
            return 'Equal'

    if request.method == 'GET':
        if 'symbol' in request.args:
            stock_symbol = request.args.get('symbol')
            now = datetime.datetime.now()
            start = now - datedelta.datedelta(months=3)
            end = now

            try:
                df = data.DataReader(name=stock_symbol, data_source='yahoo', start=start, end=end)

                df['Status'] = [inc_dec(c1, o1) for c1, o1 in zip(df.Close, df.Open)]
                df.index[df.Status == 'Decrease']
                df['Height'] = abs(df.Open - df.Close)
                df['Middle'] = (df.Open + df.Close)/2
                df["Date_string"] = df.index.strftime("%Y-%m-%d")

                p = figure(x_axis_type='datetime', width=1000, height=300)
                t = Title()
                t.text = 'Candlestick chart for ' + stock_symbol + ': ' + start.strftime('%d/%m/%y') + ' - ' + end.strftime('%d/%m/%y')
                p.title = t
                p.grid.grid_line_alpha = 0.3

                hours_12 = 12*60*60*1000

                hover = HoverTool(tooltips=[("Date", "@Date_string"), ("Open", "@Open"), ("Close", "@Close"), ("High", "@High"), ("Low", "@Low")])
                p.add_tools(hover)

                cds_all = ColumnDataSource(df)
                cds_increase = ColumnDataSource(df[df['Status']=='Increase'])
                cds_decrease = ColumnDataSource(df[df['Status']=='Decrease'])

                p.segment('Date', 'High', 'Date', 'Low', source=cds_all)
                p.rect('Date', 'Middle', hours_12, 'Height', fill_color='green', line_color='black', source=cds_increase)
                p.rect('Date', 'Middle', hours_12, 'Height', fill_color='red', line_color='black', source=cds_decrease)

                script, div = components(p)
                cdn_js = CDN.js_files[0]
                cdn_css = CDN.css_files[0]

                return render_template("plot.html", charts=script, containers=div, cdn_css=cdn_css, cdn_js=cdn_js )

            except:
                return render_template("plot.html", message="Unable to fetch data for symbol \"%s\"" % (stock_symbol))

        return render_template("plot.html")

@app.route('/file_upload/', methods=['GET', 'POST'])
def file_upload():
    import hashlib
    import os
    from flask import Flask, flash, request, redirect, url_for
    from werkzeug.utils import secure_filename

    def sha256_checksum(file, block_size=65536):
        sha256 = hashlib.sha256()
        with open(file, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()

    if request.method == 'POST':

        if 'Upload' in request.form['action']:
            print('Upload clicked')

        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            tmpfile_dir = app.config['TMP_DIR'] + filename

            file.save(os.path.join(tmpfile_dir))
            file_length = os.stat(tmpfile_dir).st_size
            computed_checksum = sha256_checksum(tmpfile_dir)
            os.remove(tmpfile_dir)

            print('Request file: ', file)
            print('File size (bytes): ', file_length)
            print('SHA256 checksum: ', computed_checksum)

            input_checksum = request.form['text']
            checksum_result = None
            if len(input_checksum) > 0:
                flash('Input checksum: ' + input_checksum)
                if computed_checksum == input_checksum:
                    flash('Checksum is the same')
                    checksum_result = 'Equal'
                else:
                    flash('Checksum is not the same')
                    checksum_result = 'Not equal'

            flash('Filename: ' + filename)
            flash('SHA256: ' + computed_checksum)

            return redirect(url_for('file_upload')) #using flask to post response to same page
            #return redirect(url_for('file_upload', checksum=computed_checksum, filename=filename, result=checksum_result)) # using page paramter to post response to same page
            #return redirect(url_for('result', checksum=computed_checksum, filename=filename, result=checksum_result)) # using a new page to show the post response
        except:
            return redirect(url_for("file_upload"))

    return render_template("file_upload.html", checksum=request.args.get('checksum'), filename=request.args.get('filename'), result=request.args.get('result'))

@app.route('/file_upload_result/<checksum>/<filename>/<result>')
def result(checksum, filename, result):
    print('result')
    return checksum + '<br>' + filename + '<br>' + result

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

import tempfile
app.config['TMP_DIR'] = tempfile.gettempdir()
if __name__=="__main__":
    app.secret_key = b'_5#y2L"F12$2!8z\n\xec]/'
    app.run(debug=True, host='0.0.0.0')
