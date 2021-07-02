from datetime import datetime
from authorization import *

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import psycopg2
import psycopg2.extras
from  data import brigate_name, month, i, x

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

def dict_data():
    sd = tuple({'label': key, 'value': value} for key, value in zip(x, i))
    return sd


app.layout = html.Div([

    html.Div(id='title', className='title'),

    html.Div([

        html.Form([

            dcc.Dropdown(id='dropdown_month',
                         options=dict_data(),
                         value=6, placeholder="Выберите номер месяцв", searchable=True,
                         className='department_dropdown'),
            html.Br(),

            dcc.Dropdown(id='dropdown_department',
                         options=[{'label': a, "value": a} for a in
                                  ['А-Сахалинский', 'Анива', 'Долинск', 'Курильск', 'Макаров', 'Невельск', 'Новиково',
                                   'Поронайск', 'С-Курильск', 'Томари', 'Тымовское', 'Углегорск', 'Чехов', 'Ю-Курильск',
                                   'Смирных']],
                         value='Макаров', placeholder="Выберите название отряда", searchable=True,
                         className='department_dropdown'),
            html.Br(),

            dcc.RadioItems(
                id='dropdown_fuel_type',
                options=[{'label': a, "value": a} for a in ['Дизельное топливо', 'Бензин А-92', 'Бензин А-80']],
                value='Дизельное топливо',
                labelStyle={'display': 'inline-block'}
            ),
            html.Br(),
            html.Div([
                html.Div([html.Pre('Бензин-80'),
                          html.Div(id='gasoline76', className='block_1')], className='block_1_1'),
                html.Div([html.Pre('Бензин-92'),
                          html.Div(id='gasoline92', className='block_2')], className='block_2_1'),
                html.Div([html.Pre('Дизельное топливо'),
                          html.Div(id='diesel_fuel', className='block_3')], className='block_3_1'),

            ], className='block'),

            html.Br(),
            dash_table.DataTable(
                id='raport_month_table',
                columns=[{"name": c, "id": c} for c in
                         ['Пожарная часть', 'Пожарная техника', 'Номер',
                          'Показание спидометра на начало месяца',
                          'Показание спидометра на конец месяца', 'Пробег', 'Работа с насосом', 'Работа без насоса',
                          'Фактический расход', 'Нормативный расход']],
                page_size=25,
                data=[],
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'padding': '1px',
                    # 'border': '0.1px solid black',
                    'font-size': '10px',
                    'line-height': '10px',
                    'background-color': '#f3f3f3',
                    'margin': '0px',

                },
                style_as_list_view=True,
                style_header={
                    'fontWeight': 'bold',
                    'font-size': '10px',
                },

                style_cell_conditional=[

                    {'textAlign': 'center'},
                    {'if': {'column_id': 'Пожарная техника'},
                     'width': '80px'},
                    {'if': {'column_id': 'Номер'},
                     'width': '60px'},
                    {'if': {'column_id': 'Пробег'},
                     'width': '70px'},

                ],

                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Лимит общего пробега} < {Общий пробег год}',
                            'column_id': 'Общий пробег год'

                        },
                        'backgroundColor': '#85144b',
                        'color': 'white',
                        'fontWeight': 'bold'
                    }]),
            html.Br(),

            dash_table.DataTable(
                id='raport_month_table2',
                columns=[{"name": c, "id": c} for c in
                         ['Пожарная часть', 'Пожарная техника',
                          'Номер', 'Общий пробег с начала эксплуатации', 'Лимит общего пробега',
                          'Общий пробег месяц',
                          'Общий пробег год', 'Заправлено ГСМ',
                          'Заправлено ГСМ год', 'Топливо в баке']],
                page_size=25,
                data=[],
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'padding': '1px',
                    # 'border': '0.1px solid black',
                    'font-size': '10px',
                    'line-height': '10px',
                    'background-color': '#f3f3f3',
                    'margin': '0px',

                },
                style_as_list_view=True,
                style_header={
                    'fontWeight': 'bold',
                    'font-size': '10px',
                },
                style_cell_conditional=[

                    {'textAlign': 'center'},
                    {'if': {'column_id': 'Пожарная техника'},
                     'width': '80px'},
                    {'if': {'column_id': 'Номер'},
                     'width': '60px'},
                    {'if': {'column_id': 'Общий пробег с начала эксплуатации'},
                     'width': '90px'},
                    {'if': {'column_id': 'Лимит общего пробега'},
                     'width': '60px'},
                    {'if': {'column_id': 'Общий пробег месяц'},
                     'width': '60px'},
                    {'if': {'column_id': 'Общий пробег год'},
                     'width': '60px'},
                    {'if': {'column_id': 'Заправлено ГСМ год'},
                     'width': '50px'},
                    {'if': {'column_id': 'Заправлено ГСМ'},
                     'width': '50px'},
                    {'if': {'column_id': 'Топливо в баке'},
                     'width': '50px'},
                    {'if': {'column_id': 'Пожарная часть'},
                     'width': '60px'},

                ],

                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Лимит общего пробега} < {Общий пробег год}',
                            'column_id': 'Общий пробег год'

                        },
                        'backgroundColor': '#85144b',
                        'color': 'white',
                        'fontWeight': 'bold'
                    }]),
            dcc.Store(id="store1", data=0),

        ], className='second_columns2'),

    ], className='first_line'),

], className='body2')


@app.callback(
    dash.dependencies.Output('raport_month_table', 'data'),
    dash.dependencies.Output('raport_month_table2', 'data'),
    dash.dependencies.Output('gasoline76', 'children'),
    dash.dependencies.Output('gasoline92', 'children'),
    dash.dependencies.Output('diesel_fuel', 'children'),
    dash.dependencies.Output('title', 'children'),

    [
        dash.dependencies.Input('dropdown_month', 'value'),
        dash.dependencies.Input('dropdown_department', 'value'),
        dash.dependencies.Input('dropdown_fuel_type', 'value'),
    ],
)
def raport_month_table(dropdown_month, dropdown_department, dropdown_fuel_type):
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT fire_brigate, fire_department, auto, auto_number, min_speedo_out, max_speedo_out, miles, "
                    "sum_pump, sum_without_pump, actual_expense, total_con, month_departure, d_fuel_type FROM dataset_python;")

        data_table = cur.fetchall()

        cur.execute("SELECT fire_brigate, fire_department, auto, auto_number, current_total_mileage, "
                    "d_total_mileage_max_value, total_mileage, cumulative_total_mileage, sum_r_refueling, "
                    "cumulative_sum_refueling, current_fuel_tank, month_departure, d_fuel_type FROM dataset_python;")
        data_table2 = cur.fetchall()

        cur.execute("SET timezone = 'Asia/Sakhalin';")

        # запрос на формирование данных для заполнения карточек расхода ГСМ по отряду и виду ГСМ
        cur.execute("SELECT fire_brigate, d_fuel_type, month_departure, SUM(actual_expense) AS actual_expense FROM "
                    "dataset_python GROUP BY fire_brigate, d_fuel_type, month_departure;")
        data_table3 = cur.fetchall()

        fuel_con_months_brigate = pd.DataFrame(data_table3,
                                               columns=['Отряд', 'Вид топлива', 'Месяц', 'Фактический расход'])

        fuel_con_months_brigate_gasoline92 = fuel_con_months_brigate[
            (fuel_con_months_brigate['Отряд'] == dropdown_department) & (
                    fuel_con_months_brigate['Месяц'] == dropdown_month) & (
                    fuel_con_months_brigate['Вид топлива'] == 'Бензин А-92')]['Фактический расход'].sum()

        fuel_con_months_brigate_diesel = fuel_con_months_brigate[
            (fuel_con_months_brigate['Отряд'] == dropdown_department) & (
                    fuel_con_months_brigate['Месяц'] == dropdown_month) & (
                    fuel_con_months_brigate['Вид топлива'] == 'Дизельное топливо')]['Фактический расход'].sum()

        fuel_con_months_brigate_gasoline76 = fuel_con_months_brigate[
            (fuel_con_months_brigate['Отряд'] == dropdown_department) & (
                    fuel_con_months_brigate['Месяц'] == dropdown_month) & (
                    fuel_con_months_brigate['Вид топлива'] == 'Бензин А-80')]['Фактический расход'].sum()

        # запрос таблицы
        data_table_base = pd.DataFrame(data_table,
                                       columns=['Отряд', 'Пожарная часть', 'Пожарная техника', 'Номер',
                                                'Показание спидометра на начало месяца',
                                                'Показание спидометра на конец месяца',
                                                'Пробег', 'Работа с насосом', 'Работа без насоса', 'Фактический расход',
                                                'Нормативный расход', 'Номер месяца', 'Вид топлива'])

        raport_month_table = \
            data_table_base[
                (data_table_base['Номер месяца'] == dropdown_month) & (
                        data_table_base['Отряд'] == dropdown_department) & (
                        data_table_base['Вид топлива'] == dropdown_fuel_type)][
                ['Пожарная часть', 'Пожарная техника', 'Номер', 'Отряд', 'Номер месяца', 'Пробег',
                 'Работа с насосом', 'Работа без насоса', 'Фактический расход', 'Нормативный расход',
                 'Показание спидометра на начало месяца', 'Показание спидометра на конец месяца']]

        # запрос таблицы
        data_table_base2 = pd.DataFrame(data_table2,
                                        columns=['Отряд', 'Пожарная часть', 'Пожарная техника',
                                                 'Номер', 'Общий пробег с начала эксплуатации', 'Лимит общего пробега',
                                                 'Общий пробег месяц',
                                                 'Общий пробег год', 'Заправлено ГСМ',
                                                 'Заправлено ГСМ год', 'Топливо в баке',
                                                 'Месяц', 'Вид топлива'])

        print(dropdown_month)
        # def table_2():
        #     if dropdown_department == None:
        #         filtered_df =  data_table_base2[
        #         (data_table_base2['Месяц'] == dropdown_month) & (
        #                 data_table_base2['Отряд'] == dropdown_department)][
        #             ['Пожарная часть', 'Техника',
        #              'Номер', 'Общий пробег с начала эксплуатации', 'Лимит общего пробега',
        #              'Общий пробег месяц',
        #              'Общий пробег год', 'Заправлено ГСМ',
        #              'Заправлено ГСМ год', 'Топливо в баке']]
        #         return filtered_df
        #     else:
        #         return data_table_base2

        raport_month_table2 = \
            data_table_base2[
                (data_table_base2['Месяц'] == dropdown_month) & (
                        data_table_base2['Отряд'] == dropdown_department) & (
                        data_table_base['Вид топлива'] == dropdown_fuel_type)][
                ['Пожарная часть', 'Пожарная техника',
                 'Номер', 'Общий пробег с начала эксплуатации', 'Лимит общего пробега',
                 'Общий пробег месяц',
                 'Общий пробег год', 'Заправлено ГСМ',
                 'Заправлено ГСМ год', 'Топливо в баке']]

    def name_month(params, dropdown):
        for i in params:
            if i[1] == dropdown:
                pass
                return i[0]

    title = html.Div(html.Pre(f'Отчет ГСМ за {name_month(month, dropdown_month)} месяц\nOСП: '
                              f'{name_month(brigate_name, dropdown_department)}'),
                     className='title'),

    return raport_month_table.to_dict('records'), raport_month_table2.to_dict(
        'records'), fuel_con_months_brigate_gasoline76, fuel_con_months_brigate_gasoline92, \
           fuel_con_months_brigate_diesel, title


if __name__ == '__main__':
    app.run_server(debug=True)
