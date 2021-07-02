from flask_sqlalchemy import SQLAlchemy
from authorization import *
import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import psycopg2
import psycopg2.extras

from data import suka
import time

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Анализ ГСМ')

server = app.server

from datetime import datetime

a = time.time()

#
# list_my = {
#     '4826 СМ': ['Снегоход'],
#     '4827 СМ': ['Снегоболотоход'],
#     'А 868 РУ': ['ЗИЛ(131)'],
#     'К 136 ТК': ['АЦ-7,5-40(4320)'],
#     'К 441 РТ': ['АЦ-2,5-40(5313)'],
#     'М 063 НХ': ['АЦ-5,5-40(5557)'],
#     'М 355 НЕ': ['АЦ-5,5-40(5557)'],
#     'М 367 НЕ': ['АРС(15)'],
#     'М 368 ТК': ['АЦЛ-3,0-40-17(43118)'],
#     'М 736 ВМ': ['УАЗ(390995)'],
#     'М 910 МЕ': ['АМУР(531382)'],
#
# }
#
#
# df = pd.DataFrame.from_dict(list_my, orient='index', columns=['auto'])

# dbc.Col(dcc.Dropdown(id='dropdown_osp',
#                      options=[{'label': a, "value": a} for a in
#                               list.keys()],
#                      value='Анива'), style={'text-align': 'left', 'font-size': 'large'},
#         width={'size': 3, "offset": 0, 'order': 0}),
#
# dbc.Col(dcc.Dropdown(id='dropdown_psch',
#                      options=[{'label': b, "value": b} for b in
#                               df['Пожарная часть'].unique()],
#                      value=''), style={'text-align': 'left', 'font-size': 'large'},
#         width={'size': 3, "offset": 0, 'order': 0}),


# with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
#     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cur.execute("SELECT count(*) FROM total_consumption_join_main4;")
#     data = cur.fetchall()
#     print(data)


# app.server.config["SQLALCHEMY_DATABASE_URI"] = \
#     'postgresql://tinwqzwytvlios:4914678fe9df3d09af79ff8471077cdde4616e7400a3ab8f0312e41817566821@ec2-63-34-97-163.eu' \
#     '-west-1.compute.amazonaws.com:5432/dahabnlnvjhvm7'
# #
# db = SQLAlchemy(app.server)
#
# df = pd.read_sql_table('productlist', con=db.engine)
# with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
#     cur = conn.cursor()
#     count_str = cur.execute('SELECT * FROM productlist;')

reason = ['Взаимодействие со службами', 'ДТП', 'ЕТО', 'Заправка ГСМ', 'Иные выезда', 'Ложный', 'Обкатка после ТО',
          'Оказание помощи населению', 'Отработка нормативов ГДЗС', 'Отработка нормативов ПС/ТСП',
          'Отработка ПТП и КТП', 'Пожар', 'Проверка подразделения', 'ПТЗ', 'ПТУ']

app.layout = html.Div([
    dbc.Modal(
        [
            html.Form([

                # Пожарный отряд
                # html.Pre('Пожарный отряд:'),
                html.Pre('Введите данные:', className='login_name'),
                dcc.Dropdown(id='brigate', options=[{'label': a, "value": a} for a in suka.keys()],
                             placeholder="Выберите название отряда", searchable=True),
                # html.Span('Это поле должно содержать E-Mail в формате example@site.com', className='form__error'),
                # Пожарная часть
                # html.Pre('Пожарная часть:'),
                dcc.Dropdown(id='department', options=[], placeholder="Выберете название ПЧ"),
                # html.Span('Это поле должно содержать текстовое значение', className='form__error'),

                # Календарь
                # html.Pre('Дата выезда (м/д/г):'),
                html.Div(
                    dcc.DatePickerSingle(id='date_out', month_format='MMMM Y', placeholder='MMMM Y',
                                         date=date(
                                             datetime.now().year, datetime.now().month,
                                             datetime.now().day), first_day_of_week=1,
                                         display_format='DD.MM.YYYY'),
                    className='first_date'),

                # Время выезда
                # html.Pre('Время выезда:'),
                dbc.Input(id='time_out', type="text", placeholder="Время выезда", value='08:00',
                          required=True,
                          autoComplete='off'),

                # Пожарная техника
                # html.Pre('Пожарная техника:'),
                dcc.Dropdown(id='fire_auto', placeholder="Вид техники", options=[],
                             style={'background-color': '#e6e3df'}),

                # Государственный номер
                # html.Pre('Государственный номер:'),
                dcc.Dropdown(id='gov_number', placeholder="Государственный номер", value="",
                             style={'background-color': '#e6e3df'}, options=[]),

                # Показание спидометра при выезде
                # html.Pre('Показание спидометра при выезде:'),
                dbc.Input(id='speedo_out', type="number", placeholder="Показание спидометра при выезде",
                          required=True, autoComplete='off'),

                # Показание спидометра при возвращении
                # html.Pre('Показание спидометра при возвращении:'),
                dbc.Input(id='speedo_in', type='number',
                          placeholder="Показание спидометра на момент прибытия",
                          required=True, autoComplete='off'),

                # Работа с насосом, мин
                # html.Pre('Работа с насосом, мин:'),
                dbc.Input(id='work_pump', type="number", placeholder="Работа с насосом", required=True,
                          autoComplete='off'),

                # Работа без насоса, мин
                # html.Pre('Работа без насоса, мин:'),
                dbc.Input(id='without_pump', type="number", placeholder="Работа без насоса",
                          required=True,
                          autoComplete='off'),

                # Фактический расход топлива, л
                # html.Pre('Фактический расход топлива, л:'),
                dbc.Input(id='actual_con', type="number", placeholder="Фактический расход",
                          required=True,
                          autoComplete='off'),

                # Дата возвращения (м/д/г)
                # html.Pre('Дата возвращения (месяц/день/год):'),
                html.Div(
                    dcc.DatePickerSingle(id='date_in', month_format='MMMM Y', placeholder='MMMM Y',
                                         date=date(
                                             datetime.now(
                                             ).year, datetime.now().month, datetime.now().day),
                                         first_day_of_week=1, display_format='DD.MM.YYYY',
                                         className="date_return")),

                # Время возвращения
                # html.Pre('Время возвращения:'),

                dbc.Input(id='time_in', type="text", placeholder="Время возвращения", value='08:00',
                          required=True,
                          autoComplete='off'),

                # Основание выезда
                # html.Pre('Основание выезда:'),
                dcc.Dropdown(id='reason_out', placeholder="Основание для выезда", value="",
                             style={'background-color': '#e6e3df'},
                             options=[{'label': a, "value": a} for a in
                                      reason]),
                html.Button('Отправить', id='save_to_postgres', n_clicks=0),
            ], className='form'),

            dbc.ModalFooter(
                dbc.Button(
                    "Закрыть", id="close", className="ml-auto", n_clicks=0,
                )
            ),
        ],
        id="modal",
        centered=True,
        is_open=False,
    ),

    html.Div([
        html.Div([
            html.Button("ПЕРЕДАТЬ СВЕДЕНИЯ", id="open", n_clicks=0, className='send'),
            html.Div([html.H3('Оперативная обстановка за '),
                      dcc.DatePickerRange(
                          id='my-date-picker-range',
                          first_day_of_week=1,
                          # clearable=True,
                          start_date=datetime.now().date() - timedelta(days=3),
                          end_date=datetime.now().date(),
                          display_format='DD.MM.YYYY',
                          className='datepickerrange'
                      )], className='title_data'),
        ], className='title'),

        html.Div([
            dcc.Dropdown(id='brigate2', options=[{'label': a, "value": a} for a in suka.keys()], value='Анива',
                         placeholder="Выберите название отряда", searchable=True,
                         className='department_dropdown'),
            html.Br(),
            dash_table.DataTable(id='the_table',
                                 columns=[{"name": c, "id": c} for c in
                                          ['часть', 'дата выезда', 'время выезда', 'пожарная техника',
                                           'номер', 'спидометр при выезде', 'спидометр при возвращении',
                                           'работа с насосом', 'работа без насоса', 'фактический расход',
                                           'дата возвращения', 'время возвращения', 'основание выезда', 'отправлено']],
                                 page_size=15,
                                 data=[],
                                 style_cell={
                                     'whiteSpace': 'normal',
                                     'height': 'auto',
                                     'font-size': '10px',
                                 },
                                 style_header={
                                     'fontWeight': 'bold',
                                     'font-size': '10px',
                                 },
                                 style_table={'overflowX': 'auto'},

                                 style_cell_conditional=[

                                     {'if': {'column_id': 'дата выезда'},
                                      'width': '80px'},
                                     {'if': {'column_id': 'номер'},
                                      'width': '60px'},
                                     {'if': {'column_id': 'Пожарная техника'},
                                      'width': '70px'},
                                     {'if': {'column_id': 'Спидометр при возвращении'},
                                      'width': '70px'},
                                     {'textAlign': 'center'},

                                 ],
                                 sort_action='native',
                                 style_data_conditional=[
                                     {
                                         'if': {
                                             'filter_query': '{общий пробег от нормы, %} > 32',
                                             'column_id': 'общий пробег от нормы, %'
                                         },
                                         'color': 'tomato',
                                         'fontWeight': 'bold'
                                     }],

                                 )], className='second_columns'),
        html.Div([
            html.Div([html.Pre('Количество\nвыездов'),
                      html.Div(id='day_out')], className='i_graph'),
            html.Div([html.Pre('Фактический\nрасход топлива'),
                      html.Div(id='current_expence')], className='i_graph'),
            html.Div([html.Pre('Работа\nс насосом'),
                      html.Div(id='day_pump')], className='i_graph'),
            html.Div([html.Pre('Работа\nбез насоса'),
                      html.Div(id='day_without_pump')], className='i_graph'),
            html.Div([html.Pre('Пробег'),
                      html.Div(id='day_miles')], className='i_graph'),
            html.Div([html.Pre('Пожары'),
                      html.Div(id='day_fire')], className='i_graph')
        ], className='third_columns')], className='two_third_columns'),

    html.Div([
        html.Div(id='con_postgresql', children=[]),
        dcc.Interval(id='interval', interval=2000),

    ]),
], className='body')


@app.callback(
    dash.dependencies.Output("modal", "is_open"),
    [dash.dependencies.Input("open", "n_clicks"),
     dash.dependencies.Input("close", "n_clicks")],
    [dash.dependencies.State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [dash.dependencies.Output('department', 'options'),
     dash.dependencies.Output('fire_auto', 'options')
     ],
    [
        dash.dependencies.Input('brigate', 'value'),
    ],
)
def update_output(brigate):
    list_department = [{'label': a, 'value': a} for a in suka[brigate]['brigate']]
    list_fire_auto = [{'label': a, 'value': a} for a in suka[brigate]['auto']]
    return list_department, list_fire_auto


@app.callback(
    dash.dependencies.Output('gov_number', 'options'),
    [dash.dependencies.Input('fire_auto', 'value'),
     dash.dependencies.Input('brigate', 'value')],
)
def update_output(fire_auto, brigate):
    list_gov_number = [{'label': a, 'value': a} for a in suka[brigate][fire_auto]]
    return list_gov_number


@app.callback(
    dash.dependencies.Output('con_postgresql', 'children'),
    [dash.dependencies.Input('save_to_postgres', 'n_clicks'),
     dash.dependencies.Input("interval", "n_intervals")
     ],
    [dash.dependencies.State('brigate', 'value'),
     dash.dependencies.State('department', 'value'),
     dash.dependencies.State('date_out', 'date'),
     dash.dependencies.State('time_out', 'value'),
     dash.dependencies.State('fire_auto', 'value'),
     dash.dependencies.State('gov_number', 'value'),
     dash.dependencies.State('speedo_out', 'value'),
     dash.dependencies.State('speedo_in', 'value'),
     dash.dependencies.State('work_pump', 'value'),
     dash.dependencies.State('without_pump', 'value'),
     dash.dependencies.State('actual_con', 'value'),
     dash.dependencies.State('date_in', 'date'),
     dash.dependencies.State('time_in', 'value'),
     dash.dependencies.State('reason_out', 'value'),
     ], prevent_initial_call=True)
def update_output(n_clicks, n_intervals, brigate, department, date_out, time_out, fire_auto, gov_number,
                  speedo_out, speedo_in, work_pump, without_pump, actual_con, date_in, time_in,
                  reason_out):
    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if input_triggered == 'save_to_postgres':
        with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO dataset VALUES ('{brigate}', '{department}', '{date_out}' , '{time_out}', "
                f"'{fire_auto}', '{gov_number}', '{speedo_out}', '{speedo_in}', '{work_pump}', "
                f"'{without_pump}', '{actual_con}', '{date_in}', '{time_in}', '{reason_out}')")


@app.callback(
    dash.dependencies.Output('the_table', 'data'),
    dash.dependencies.Output("current_expence", "children"),
    dash.dependencies.Output("day_out", "children"),
    dash.dependencies.Output("day_without_pump", "children"),
    dash.dependencies.Output("day_pump", "children"),
    dash.dependencies.Output("day_miles", "children"),
    dash.dependencies.Output("day_fire", "children"),

    [
        dash.dependencies.Input('brigate2', 'value'),
        dash.dependencies.Input('my-date-picker-range', 'start_date'),
        dash.dependencies.Input('my-date-picker-range', 'end_date'),

    ]
)
def display_graph(brigate2, start_date, end_date):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SET timezone = 'Asia/Sakhalin';")
            cur.execute("SELECT * FROM dataset ORDER BY data_sent DESC;")
            data = cur.fetchall()

            postgreTable = pd.DataFrame(data,
                                        columns=['отряд', 'часть', 'дата выезда', 'время выезда',
                                                 'пожарная техника',
                                                 'номер', 'спидометр при выезде', 'спидометр при возвращении',
                                                 'работа с насосом', 'работа без насоса', 'фактический расход',
                                                 'дата возвращения', 'время возвращения', 'основание выезда',
                                                 'отправлено'])

            start_datetime_object = datetime.strptime(f'{start_date}', '%Y-%m-%d').date()
            end_datetime_object = datetime.strptime(f'{end_date}', '%Y-%m-%d').date()

            postgreTable_filterDate = postgreTable.loc[
                (postgreTable['дата выезда'] >= start_datetime_object) & (postgreTable['дата выезда']
                                                                          <= end_datetime_object)]

            postgreTable_filterDate_filterDepartment = \
                postgreTable_filterDate[(postgreTable_filterDate['отряд'] == brigate2)][
                    ['часть', 'дата выезда', 'время выезда', 'пожарная техника',
                     'номер', 'спидометр при выезде', 'спидометр при возвращении',
                     'работа с насосом', 'работа без насоса', 'фактический расход',
                     'дата возвращения', 'время возвращения', 'основание выезда', 'отправлено']]

            cur.execute("SELECT * FROM pivot_table")
            data1 = cur.fetchall()
            data_pivot_table = pd.DataFrame(data1,
                                            columns=['отряд', 'дата', 'пробег', 'расход ГСМ', 'работа без насоса',
                                                     'работа с насосом', 'фактический расход', 'кол-во выездов',
                                                     'пожары'])

            data_pivot_table = data_pivot_table.loc[(data_pivot_table['дата'] >= start_datetime_object) & (
                    data_pivot_table['дата'] <= end_datetime_object)]

            def day_out():
                if brigate2 == None:
                    w_day_out = data_pivot_table['кол-во выездов'].sum()
                    return w_day_out
                else:
                    current_day_out = data_pivot_table[(data_pivot_table['отряд'] == brigate2)]['кол-во выездов'].sum()
                    return current_day_out

            def current_expence():
                if brigate2 == None:
                    w_current_expence = data_pivot_table['фактический расход'].sum()
                    return w_current_expence
                else:
                    current_expence = data_pivot_table[(data_pivot_table['отряд'] == brigate2)][
                        'фактический расход'].sum()
                    return current_expence

            def without_pump():
                if brigate2 == None:
                    w_without_pump = data_pivot_table['работа без насоса'].sum()
                    return w_without_pump
                else:
                    current_without_pump = data_pivot_table[(data_pivot_table['отряд'] == brigate2)][
                        'работа без насоса'].sum()
                    return current_without_pump

            def witn_pump():
                if brigate2 == None:
                    w_pump = data_pivot_table['работа с насосом'].sum()
                    return w_pump
                else:
                    current_pump = data_pivot_table[(data_pivot_table['отряд'] == brigate2)]['работа с насосом'].sum()
                    return current_pump

            def the_mileage():
                if brigate2 == None:
                    w_mileage = data_pivot_table['пробег'].sum()
                    return w_mileage
                else:
                    current_mileage = data_pivot_table[(data_pivot_table['отряд'] == brigate2)][
                        'пробег'].sum()
                    return current_mileage

            def the_fire():
                if brigate2 == None:
                    w_fire = data_pivot_table['пожары'].sum()
                    return w_fire
                else:
                    current_fire = data_pivot_table[(data_pivot_table['отряд'] == brigate2)][
                        'пожары'].sum()
                    return current_fire

            def the_table():
                if brigate2 == None:
                    without_filter = postgreTable_filterDate.copy()
                    return without_filter
                else:
                    return postgreTable_filterDate_filterDepartment

            return the_table().to_dict('records'), current_expence(), day_out(), without_pump(), witn_pump(), \
                   the_mileage(), the_fire()


if __name__ == '__main__':
    app.run_server(debug=False)
