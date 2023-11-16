from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap4(app)






class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    locations = StringField("Locations (URL)", validators=[DataRequired(), URL()])
    open = StringField("Open", validators=[DataRequired()])
    close = StringField("Close", validators=[DataRequired()])
    coffee = SelectField("Coffee Rating", choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
    wifi = SelectField("WiFi", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')





# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.locations.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.coffee.data},"
                           f"{form.wifi.data},"
                           f"{form.power.data}")
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        cafe_to_delete = request.form['cafe']
        rows = []

        # Чтение CSV-файла и удаление строки с заданным именем
        with open('cafe-data.csv', 'r', newline='', encoding='utf-8') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            for row in csv_data:
                if row[0] != cafe_to_delete:
                    rows.append(row)

        # Запись обновленных данных в CSV-файл
        with open('cafe-data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerows(rows)

    # После удаления перенаправление на страницу с оставшимися кафе
    with open('cafe-data.csv', 'r', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = list(csv_data)

    return render_template('delete.html', cafes=list_of_rows)



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
