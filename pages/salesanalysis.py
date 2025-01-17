import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc ,callback,Input,Output,dash_table
import dash_bootstrap_components as dbc
from dash.dash_table import FormatTemplate
import dash_ag_grid as dag

dash.register_page(__name__,path = "/salesanalysis", title = "Sales Analysis")
superstore=pd.read_csv("data/Sample - Superstore.csv",encoding="latin1")
superstore["Order Date"] = pd.to_datetime(superstore["Order Date"],format="%m/%d/%Y")




categorysales = superstore.groupby('Category')['Sales'].sum()
categorysalesdistribution = px.pie(names = categorysales.index, 
                                      values = categorysales.values,
                                      hole = 0.7,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

categorysalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white', title = dict(font = dict(color = 'white')))

totalsales = '${:,}'.format(round(categorysales.sum(), 2))
categorysalesdistribution.add_annotation(text = "Total Sales by Category", showarrow = False,
                                            font_size = 14, font_color = 'White',
                                            y = 0.55)
categorysalesdistribution.add_annotation(text = totalsales, showarrow = False,
                                            font_size = 14, font_color = 'White', y = 0.45)


segmentsales = superstore.groupby('Segment')['Sales'].sum()
segmentsalesdistribution = px.pie(names = segmentsales.index, 
                                      values = categorysales.values,
                                      hole = 0.7,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

segmentsalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white', title = dict(font = dict(color = 'white')))

totalsales = '${:,}'.format(round(segmentsales.sum(), 2))
segmentsalesdistribution.add_annotation(text = "Total Sales by Segment", showarrow = False,
                                            font_size = 14, font_color = 'White',
                                            y = 0.55)
segmentsalesdistribution.add_annotation(text = totalsales, showarrow = False,
                                            font_size = 14, font_color = 'White', y = 0.45)




categoryprofit = superstore.groupby('Category')['Profit'].sum()
categoryprofitdistribution = px.pie(names = categoryprofit.index, 
                                      values = categoryprofit.values,
                                      hole = 0.7,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

categoryprofitdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white')

totalprofit = '${:,}'.format(round(categoryprofit.sum(), 2))
categoryprofitdistribution.add_annotation(text = "Total Profit by Category", showarrow = False,
                                            font_size = 14, font_color = 'White',
                                            y = 0.55)
categoryprofitdistribution.add_annotation(text = totalprofit, showarrow = False,
                                            font_size = 14, font_color = 'White', y = 0.45)

categorysalesprofit = superstore.groupby('Category').agg(
                      {"Sales" : 'sum', 'Profit' : 'sum', 'Quantity' : 'sum'}  
                    ).reset_index()

categorysalesprofitdistribution = px.scatter(categorysalesprofit, x = 'Profit', y = 'Sales', color = 'Category',
                                             size = "Quantity" , title = "Category Quantity for Sales Vs Returns")

categorysalesprofitdistribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = 'rgba(0,0,0,0)',
                                              xaxis = dict(title = "Total Profit", color = 'white'),
                                              yaxis = dict(title = "Total Sales", color = 'white'),
                                              title = dict(font  = dict(color = 'white')),
                                              legend_font_color = 'white'
                                              )

categorysalesprofitdistribution.update_xaxes(showgrid = False)
categorysalesprofitdistribution.update_yaxes(showgrid = False)



categorysalesprofitdiscount = superstore.groupby('Category').agg(
                      {"Sales" : 'sum', 'Profit' : 'sum', 'Discount' : 'sum'}  
                    ).reset_index()

categorysalesprofitdiscountdistribution = px.scatter(categorysalesprofitdiscount, x = 'Profit', y = 'Sales', color = 'Category',
                                             size = "Discount" , title = "Category Profit for Sales Vs Returns")

categorysalesprofitdiscountdistribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = 'rgba(0,0,0,0)',
                                              xaxis = dict(title = "Total Profit", color = 'white'),
                                              yaxis = dict(title = "Total Sales", color = 'white'),
                                              title = dict(font  = dict(color = 'white')),
                                              legend_font_color = 'white'
                                              )

categorysalesprofitdiscountdistribution.update_xaxes(showgrid = False)
categorysalesprofitdiscountdistribution.update_yaxes(showgrid = False)


categorysubcategorysales = superstore.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysubcategorysalesdistribution = px.sunburst(categorysubcategorysales, path = ['Category', 'Sub-Category'], values = 'Sales')

categorysubcategorysalesdistribution.update_layout(paper_bgcolor = 'rgba(0,0,0,0)')

categorysubcategorysalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24))


categorysegmentsales = superstore.groupby(['Segment', 'Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysegmentsalesdistribution = px.sunburst(categorysegmentsales, path = ['Segment', 'Category', 'Sub-Category'], values = 'Sales', color_discrete_sequence=px.colors.qualitative.Dark24_r)

categorysegmentsalesdistribution.update_layout(title = "Categories and Sub-Categories Sales by Segment",
                                              title_font = dict(color = 'White'),
                                              paper_bgcolor = 'rgba(0,0,0,0)')

categorysegmentsalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24_r))



totalsalesbycustomer = superstore.groupby(['Customer Name', 'Order Date'])['Sales'].sum().reset_index()

totalsalesbycustomer = totalsalesbycustomer.groupby('Customer Name')['Sales'].sum().reset_index()

top5customersbysales = totalsalesbycustomer.nlargest(5, 'Sales')['Customer Name']

filteredtop5 = superstore[superstore['Customer Name'].isin(top5customersbysales)]

totalsalesovertimetop5 = filteredtop5.groupby(['Customer Name', filteredtop5['Order Date'].dt.year])['Sales'].sum().reset_index()
totalsalesovertimetop5['Order Date'] = pd.to_datetime(totalsalesovertimetop5['Order Date'], format = "%Y")

totalsalesovertimetop5distribution = px.area(totalsalesovertimetop5, x = 'Order Date', y = "Sales", color = "Customer Name", title = "Customer Sales Over Years")

totalsalesovertimetop5distribution.update_layout(plot_bgcolor = 'rgba(0,0,0,0)', paper_bgcolor = "rgba(0,0,0,0)",
                                                  legend_font_color = 'white', title_font = dict(color = "white"),
                                                  xaxis = dict(title = "Order Date", color = "white"),
                                                  yaxis = dict(title = "Total Sales", color = "white"),
                                                  )

totalsalesovertimetop5distribution.update_xaxes(showgrid = False)
totalsalesovertimetop5distribution.update_yaxes(showgrid = False)



salesquantity = superstore.groupby(['Segment']).agg(
                      {"Sales" : 'sum', 'Quantity' : 'sum'}  
                    ).reset_index()

salesquantitydist = px.bar(salesquantity, x="Segment", y="Sales", title='Sales by Segment', text_auto='', color_discrete_sequence=px.colors.qualitative.Dark24_r)

salesquantitydist.update_layout(title=dict(font=dict(color='white')), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                       xaxis=dict(title=dict(font=dict(color='white')), tickfont=dict(color='white')),
                       yaxis=dict(showticklabels=False), yaxis_title='', xaxis_title = '')

salesquantitydist.update_yaxes(showgrid=False, gridcolor='rgba(255, 255, 255, 0.2)', zeroline=True, zerolinecolor='rgba(0, 0, 0, 0)')

salesquantitydist.update_traces(marker_line_width=0, textfont_size=12, textfont_color='white', textangle=0, texttemplate='%{y:,}', textposition="outside", cliponaxis=False)




categorysegmentsalesdistributicategorysegmentsales = superstore.groupby(['Segment', 'Category', 'Sub-Category'])['Sales'].sum().reset_index()

categorysegmentsalesdistribution = px.sunburst(categorysegmentsales, path = ['Segment', 'Category', 'Sub-Category'], values = 'Sales', color_discrete_sequence=px.colors.qualitative.Dark24_r)

categorysegmentsalesdistribution.update_layout(title = "Categories and Sub-Categories Sales by Segment",
                                              title_font = dict(color = 'White'),
                                              paper_bgcolor = 'rgba(0,0,0,0)')

categorysegmentsalesdistribution.update_traces(marker = dict(colors = px.colors.qualitative.Dark24_r))


####table 
products_table=dag.AgGrid(
    rowData=superstore.to_dict("records"),
    id="products_table",
    columnDefs=[
       {"field": 'Product ID'  },
       {"field": 'Category' ,'filter': True},
       {"field": 'Sub-Category' ,'filter': True},
       {"field": 'Product Name',"headerName":"Product",'filter': True},
       {"field":"Profit",'filter': True}
    ] , 
    className="ag-theme-alpine-dark",
    dashGridOptions={'pagination':True},       
)




layout=html.Div (
    children= [
        dbc.Row(
            children = [
               dbc.Col(
                   dcc.Dropdown(
                    superstore['City'].unique(),
                    className= 'text-danger',
                    style= {'background':'black'},
                    value= 'Concord',
                    id ="city_dropdown",)
                  ),
                dbc.Col(
                      dcc.RadioItems(
                          superstore['Region'].unique(),
                     id='region_radio_items')
                  )  
            ]
        ),
        dbc.Row(
            children= [
               dbc.Col(
                    children=dcc.Graph(id='category_sales_distribution')
                ),
               dbc.Col(
                  
                     children=dcc.Graph(figure=segmentsalesdistribution)
               ),
            ]   
        ),
        dbc.Row(
            children= [
                dbc.Col(
                    children=dcc.Graph(figure=categorysalesprofitdistribution) 
               ),  
               dbc.Col(
                    children=dcc.Graph(figure=categorysalesprofitdiscountdistribution)
                ),
            ]
        ),
        dbc.Row(
            children=[
               dbc.Col(
                  
                     children=dcc.Graph(figure=categorysubcategorysalesdistribution)
               ),
               dbc.Col(
                    children=dcc.Graph(figure=categorysegmentsalesdistribution) 
               ),  
            ]   
        ),
        dbc.Row(
            children= [
               dbc.Col(
                    children=dcc.Graph(figure=salesquantitydist)
                ),
            ]   
        ),
        dbc.Row(
            children= [
               dbc.Col(
                    children=dcc.Graph(figure=totalsalesovertimetop5distribution)
               )
               
            ]   
        ),
        dbc.Row(
            products_table
        )
        
    ]
)

@callback(
    Output('category_sales_distribution','figure'),
    Input ('city_dropdown', 'value'),
    Input('region_radio_items','value')
)


def update_category_sales_distribution(city_value,region_value):
    city_filter_superstore=superstore[superstore['City']== city_value | superstore['Region']== region_value]
    categorysales = city_filter_superstore.groupby('Category')['Sales'].sum()
    categorysalesdistribution = px.pie(names = categorysales.index, 
                                      values = categorysales.values,
                                      hole = 0.7,
                                      color_discrete_sequence = px.colors.qualitative.Dark24_r)

    categorysalesdistribution.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)",
                                           legend_font_color = 'white', title = dict(font = dict(color = 'white')))

    totalsales = '${:,}'.format(round(categorysales.sum(), 2))
    categorysalesdistribution.add_annotation(text = "Total Sales by Category", showarrow = False,
                                            font_size = 14, font_color = 'White',
                                            y = 0.55)
    categorysalesdistribution.add_annotation(text = totalsales, showarrow = False,
                                            font_size = 14, font_color = 'White', y = 0.45)

    return categorysalesdistribution