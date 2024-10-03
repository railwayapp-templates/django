from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
import json
import plotly.graph_objects as go
import numpy as np
from plotly.utils import PlotlyJSONEncoder
import time

from .output import output_data


@login_required(login_url='/login/')
def home_view(request):
    context = {
        'page_title': 'Welcome to the template home page'
    }
    return render(request, 'home.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/api-data') 
        else:
            messages.error(request, "Invalid username or password.")
    
    # Invalid login
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Check if a user with the same email (username) already exists
            email = form.cleaned_data['email']
            if User.objects.filter(username=email).exists():
                messages.error(request, "A user with that email already exists.")
            else:
                user = form.save()
                login(request, user)  # Automatically log in the user after registration
                return redirect('api-data')  # Redirect to home after registration
    else:
        form = UserRegistrationForm()

    context = {
        'form' : form
    }
    return render(request, 'register.html', context)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')


def api_data_view(request):
    if request.method == 'POST':
        # Fetch form data
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Calculation parameters
        return_calculation = request.POST.get('return_calculation')
        price_frequency = request.POST.get('price_frequency')
        risk_free_rate = float(request.POST.get('risk_free_rate', 0))
        invested_amount = float(request.POST.get('invested_amount', 0))
        
        # Optimization parameters
        benchmark_portfolio = request.POST.get('benchmark_portfolio')
        trv_min = float(request.POST.get('target_return_for_min_volatility', 0))
        trv_max = float(request.POST.get('target_volatility_for_max_return', 0))
        default_min_weight = float(request.POST.get('default_min_weight', 0))
        default_max_weight = float(request.POST.get('default_max_weight', 0))
        frontier_runs = int(request.POST.get('frontier_runs', 0))
        monte_carlo_simulations = int(request.POST.get('monte_carlo_simulations', 0))
        solver = request.POST.get('solver')
        dendogram_segment = request.POST.get('dendogram_segment')
        
        # Ticker data - assuming the tickers and their related data are sent as lists
        tickers = request.POST.getlist('tickers[]')  # Ticker symbols
        baw_list = request.POST.getlist('baw[]')     # Benchmark asset weight
        amax_list = request.POST.getlist('amax[]')   # Asset maximum weight
        ba_list = request.POST.getlist('ba[]')       # Benchmark amount

        # Create the ticker data structure
        ticker_data = []
        for i in range(len(tickers)):
            ticker_data.append({
                "symbol": tickers[i],
                "benchmark_asset_weight": float(baw_list[i]),
                "asset_minimum_weight": 0,  # Modify this if you need it from form
                "asset_maximum_weight": float(amax_list[i]),
                "benchmark_amount": float(ba_list[i]),
                "stock_prices": []  # You can handle stock prices data here if needed
            })
        
        # Construct final JSON structure
        form_data = {
            "start_date": start_date,
            "end_date": end_date,
            "calculation_parameters": {
                "return_calculation": return_calculation,
                "price_frequency": price_frequency,
                "risk_free_rate": risk_free_rate,
                "invested_amount": invested_amount
            },
            "optimization_parameters": {
                "benchmark_portfolio": benchmark_portfolio,
                "target_return_for_min_volatility": trv_min,
                "target_volatility_for_max_return": trv_max,
                "default_min_weight": default_min_weight,
                "default_max_weight": default_max_weight,
                "frontier_runs": frontier_runs,
                "monte_carlo_simulations": monte_carlo_simulations,
                "benchmark_ticker": "^GSPC",  # Hardcoded for now, modify if needed
                "solver": solver,
                "dendogram_segment": dendogram_segment
            },
            "ticker_data": ticker_data
        }

        
        # Render the form if it's a GET request
        x_y_data = []
        table_data = []

        strageties = output_data['strategies']
        for strategy in strageties:
            if strategy['data'] is not None:  # Check if 'data' is not None
                x = strategy['data']['portfolio_summary']['annualized_mean']
                y = strategy['data']['portfolio_summary']['standard_deviation']
                x_y_data.append({
                    'annualized_mean': x,
                    'standard_deviation': y
                })
                table_data.append({
                    'exp_return': strategy['data']['expected_return'],
                    'std_dev': strategy['data']['standard_deviation'],
                    'sharpe_ratio': strategy['data']['sharpe_ratio']
                })
        
        # Convert the x_y_data to JSON
        x_y_data_json = json.dumps(x_y_data)
        print(table_data) 

        context = {
            'data': x_y_data_json,
            'table_data': table_data
        }
        # Return JSON response for demonstration
        # return JsonResponse(data)
        return render(request, 'data.html', context)

    # Render the form if it's a GET request
    x_y_data = []
    table_data = []

    strageties = output_data['strategies']
    for strategy in strageties:
        if strategy['data'] is not None:  # Check if 'data' is not None
            x = strategy['data']['portfolio_summary']['annualized_mean']
            y = strategy['data']['portfolio_summary']['standard_deviation']
            x_y_data.append({
                'annualized_mean': x,
                'standard_deviation': y
            })
            table_data.append({
                'exp_return': strategy['data']['expected_return'],
                'std_dev': strategy['data']['standard_deviation'],
                'sharpe_ratio': strategy['data']['sharpe_ratio']
            })
    
    # Convert the x_y_data to JSON
    x_y_data_json = json.dumps(x_y_data)
    print(table_data) 

    context = {
        'data': x_y_data_json,
        'table_data': table_data
    }

    # print("Strategies: ", output_data['strategies'])
    return render(request, 'data2.html', context)


def api_data_view_2(request):
    if request.method == 'POST':
        frontier_runs = output_data['frontier_runs']
        frontier_x = frontier_runs['x']
        frontier_y = frontier_runs['y']
        strageties = output_data['frontier_positions']
        strategy_x = strageties['x']
        strategy_y = strageties['y']
        strategy_labels = strageties['strategy_names']

        fig1 = go.Figure()

        # Add Efficient Frontier (Blue Line)
        fig1.add_trace(go.Scatter(
            x=frontier_x, 
            y=frontier_y, 
            mode='lines+markers', 
            name='Efficient Frontier',
            line=dict(color='blue'),
            marker=dict(color='blue')
        ))

        # Add Portfolio Strategy points (Yellow Dots)
        fig1.add_trace(go.Scatter(
            x=strategy_x, 
            y=strategy_y, 
            mode='markers+text',
            text=strategy_labels, 
            name='Portfolios',
            marker=dict(color='orange', size=10),
             textposition='top center',
             textfont=dict(
                family="Arial",  # Font family
                size=12,         # Font size
                color="black"    # Font color
            ),
             texttemplate="<span style='border: 1px solid black; background-color: red; padding: 2px;'>%{text}</span>"
        ))

        # Set axis titles and layout
        fig1.update_layout(
            xaxis_title="Risk (%)",
            yaxis_title="Return (%)",
            legend=dict(yanchor="top", y=1.1, xanchor="center", x=0.5, orientation='h'),
        )

        # Convert Plotly figure to JSON
        graph_json_1 = json.dumps(fig1, cls=PlotlyJSONEncoder)

        max_cap_weight_data = output_data['strategies'][0]['data']
        max_cap_weight_tbl = {
            'Expected Return': f"{max_cap_weight_data['expected_return'] * 100:.2f}%",
            'Standard Deviation': f"{max_cap_weight_data['standard_deviation'] * 100:.2f}%",
            'Sharpe Ratio': f"{max_cap_weight_data['sharpe_ratio'] * 100:.2f}%",  # If Sharpe Ratio is not a percentage, you can skip formatting
            'CVaR 90%': f"{max_cap_weight_data['cvar_090'] * 100:.2f}%",
            'CVaR 95%': f"{max_cap_weight_data['cvar_095'] * 100:.2f}%",
            'CVaR 99%': f"{max_cap_weight_data['cvar_099'] * 100:.2f}%",
        }

        max_cap_weight_labels = []
        max_cap_weight_allocation = []
        colors = ['#FF5733', '#33FF57']
        
        for label in max_cap_weight_data['symbol_allocations']:
            max_cap_weight_labels.append(label['symbol'])
            max_cap_weight_allocation.append(label['allocation_weight'])

        fig2 = go.Figure(data=[go.Pie(
            labels=max_cap_weight_labels,
            values=max_cap_weight_allocation,
            hole=0.4,
            marker=dict(colors=colors),
            textfont=dict(color='white'),  # Set the label text color
            hoverinfo='label+value',  # Show label and value in tooltip
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>',  # Customize hover content
            hoverlabel=dict(
                font=dict(
                    family='Arial, sans-serif',
                    size=14,
                    color='white'  # Tooltip text color
                ),
                bgcolor='#ffffff',  # Tooltip background color
                bordercolor='#FF0000'  # Tooltip border color
            )
        )])
        fig2.update_layout(
            template='plotly_white',
            legend=dict(yanchor="top", y=1, xanchor="center", x=0.5, orientation='h'),
        )

        graph_json_2 = json.dumps(fig2, cls=PlotlyJSONEncoder)
        max_cap_weight_tracking_error = max_cap_weight_data['tracking_errors']
        max_cap_weight_tracking_error['ratio'] = round(max_cap_weight_tracking_error['ratio'], 2)

        min_variance_data = output_data['strategies'][1]['data']
        min_variance_tbl = {
            'Expected Return': f"{min_variance_data['expected_return'] * 100:.2f}%",
            'Standard Deviation': f"{min_variance_data['standard_deviation'] * 100:.2f}%",
            'Sharpe Ratio': f"{min_variance_data['sharpe_ratio'] * 100:.2f}%",  # If Sharpe Ratio is not a percentage, you can skip formatting
            'CVaR 90%': f"{min_variance_data['cvar_090'] * 100:.2f}%",
            'CVaR 95%': f"{min_variance_data['cvar_095'] * 100:.2f}%",
            'CVaR 99%': f"{min_variance_data['cvar_099'] * 100:.2f}%",
        }

        min_variance_labels = []
        min_variance_allocation = []

        for label in min_variance_data['symbol_allocations']:
            min_variance_labels.append(label['symbol'])
            min_variance_allocation.append(label['allocation_weight'])

        fig3 = go.Figure(data=[go.Pie(
            labels=min_variance_labels,
            values=min_variance_allocation,
            hole=0.4,
            marker=dict(colors=colors),
            textfont=dict(color='white'),  # Set the label text color
            hoverinfo='label+value',  # Show label and value in tooltip
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>',  # Customize hover content
            hoverlabel=dict(
                font=dict(
                    family='Arial, sans-serif',
                    size=14,
                    color='white'  # Tooltip text color
                ),
                bgcolor='#ffffff',  # Tooltip background color
                bordercolor='#FF0000'  # Tooltip border color
            )
        )])
        fig3.update_layout(
            template='plotly_white',
            legend=dict(yanchor="top", y=1, xanchor="center", x=0.5, orientation='h'),
        )

        graph_json_3 = json.dumps(fig3, cls=PlotlyJSONEncoder)
        min_variance_tracking_error = min_variance_data['tracking_errors']
        min_variance_tracking_error['ratio'] = round(min_variance_tracking_error['ratio'], 2)

        summary_tbl_data = output_data['strategies']
        summary_tbl = []
        for strategy in summary_tbl_data:
            if strategy['data'] is not None and strategy['data']['portfolio_summary'] is not None:
                portfolio_summary = strategy['data']['portfolio_summary']

                # Create a new dictionary with the required fields
                summary_item = {
                    'strategy_name': strategy['name'],
                    'expected_return': f"{portfolio_summary.get('annualized_mean', None)* 100:.2f}%",
                    'standard_deviation': f"{portfolio_summary.get('annualized_standard_deviation', None)* 100:.2f}%",
                    'sharpe_ratio': f"{portfolio_summary.get('annualized_sharpe_ratio', None)* 100:.2f}%",
                    'sortino_ratio': f"{portfolio_summary.get('annualized_sortino_ratio', None)* 100:.2f}%",
                    'cvar_090': f"{portfolio_summary.get('cvar_at_95', None)* 100:.2f}%",  # Adjust based on your requirements
                    'cvar_095': f"{portfolio_summary.get('cvar_at_95', None)* 100:.2f}%",  # Adjust based on your requirements
                    'cvar_099': f"{portfolio_summary.get('cvar_at_95', None)* 100:.2f}%"   # Adjust based on your requirements
                }

                # Append the summary_item to summary_tbl
                summary_tbl.append(summary_item)

        print(summary_tbl)

        context = {
            'graph_json_1': graph_json_1,
            'max_cap_weight_tbl': max_cap_weight_tbl,
            'summary_tbl': summary_tbl,
            'graph_json_2': graph_json_2,
            'max_cap_weight_tracking_error': max_cap_weight_tracking_error,
            'min_variance_tbl': min_variance_tbl,
            'graph_json_3': graph_json_3,
            'min_variance_tracking_error': min_variance_tracking_error
        }

        return render(request, 'data3.html', context)

    # Render the form if it's a GET request
    x_y_data = []
    table_data = []

    strageties = output_data['strategies']
    for strategy in strageties:
        if strategy['data'] is not None:  # Check if 'data' is not None
            x = strategy['data']['portfolio_summary']['annualized_mean']
            y = strategy['data']['portfolio_summary']['standard_deviation']
            x_y_data.append({
                'annualized_mean': x,
                'standard_deviation': y
            })
            table_data.append({
                'exp_return': strategy['data']['expected_return'],
                'std_dev': strategy['data']['standard_deviation'],
                'sharpe_ratio': strategy['data']['sharpe_ratio']
            })
    
    # Convert the x_y_data to JSON
    x_y_data_json = json.dumps(x_y_data)
    # print(table_data) 

    context = {
        'data': x_y_data_json,
        'table_data': table_data
    }

    # print("Strategies: ", output_data['strategies'])
    return render(request, 'data3.html', context)


def api_data_view_3(request):
    if request.method == 'POST':
        # Efficient Frontier Data (blue points and line)
        efficient_frontier_data = [
            {'x': 22, 'y': 10},
            {'x': 23, 'y': 12},
            {'x': 24, 'y': 14},
            {'x': 25, 'y': 16},
            {'x': 26, 'y': 18},
            {'x': 27, 'y': 20},
            {'x': 28, 'y': 22},
            {'x': 29, 'y': 24},
            {'x': 30, 'y': 26},
            {'x': 31, 'y': 28},
            {'x': 32, 'y': 30},
        ]

        # Specific Portfolios Data (orange points)
        portfolio_data = [
            {'x': 22, 'y': 10, 'label': 'Min Var'},
            {'x': 24, 'y': 15, 'label': 'HRP'},
            {'x': 26, 'y': 8, 'label': '90% CVaR'},
            {'x': 28, 'y': 28, 'label': 'Max Sharpe'},
        ]

        # Efficient Frontier (Line + Blue Circles)
        efficient_frontier_trace = go.Scatter(
            x=[point['x'] for point in efficient_frontier_data],
            y=[point['y'] for point in efficient_frontier_data],
            mode='lines+markers',
            name='Efficient Frontier',
            line=dict(color='blue'),
            marker=dict(color='blue', size=8),
        )

        # Portfolio Points (Orange Circles with Labels)
        portfolio_trace = go.Scatter(
            x=[point['x'] for point in portfolio_data],
            y=[point['y'] for point in portfolio_data],
            mode='markers+text',
            name='Portfolios',
            marker=dict(color='orange', size=10),
            text=[point['label'] for point in portfolio_data],
            textposition='top right',
            hovertemplate='Label: %{text}<br>Risk: %{x}%<br>Return: %{y}%<extra></extra>',
        )

        # Generate random portfolios (Red Points)
        np.random.seed(42)
        random_risk = np.random.uniform(22, 32, 500)
        random_return = np.random.uniform(5, 30, 500)

        random_portfolios_trace = go.Scatter(
            x=random_risk,
            y=random_return,
            mode='markers',
            name='Random Portfolios',
            marker=dict(color='red', size=5),
            hovertemplate='Risk: %{x}%<br>Return: %{y}%<extra></extra>',
        )

        # Layout (Title, Labels, etc.)
        layout = go.Layout(
            title='Efficient Frontier with Random Portfolios',
            xaxis=dict(title='Risk (%)'),
            yaxis=dict(title='Return (%)'),
            showlegend=True,  # Show the legend
            legend=dict(
                x=0.5,  # Center the legend horizontally
                y=1.02,  # Position it just above the plot area
                xanchor='center',  # Anchor the x-position to the center
                yanchor='bottom',  # Anchor the y-position to the bottom
                orientation='h',  # Horizontal orientation
                bgcolor='rgba(255, 255, 255, 0.5)',  # Background color (optional)
                bordercolor='black',  # Border color (optional)
                borderwidth=1  # Border width (optional)
            )
        )

        # Create the figure with the traces and layout
        fig = go.Figure(data=[random_portfolios_trace, efficient_frontier_trace, portfolio_trace], layout=layout)

        # Convert Plotly figure to JSON
        graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)

        return render(request, 'data3.html', {'graph_json': graph_json})

    # Render the form if it's a GET request
    x_y_data = []
    table_data = []

    strageties = output_data['strategies']
    for strategy in strageties:
        if strategy['data'] is not None:  # Check if 'data' is not None
            x = strategy['data']['portfolio_summary']['annualized_mean']
            y = strategy['data']['portfolio_summary']['standard_deviation']
            x_y_data.append({
                'annualized_mean': x,
                'standard_deviation': y
            })
            table_data.append({
                'exp_return': strategy['data']['expected_return'],
                'std_dev': strategy['data']['standard_deviation'],
                'sharpe_ratio': strategy['data']['sharpe_ratio']
            })
    
    # Convert the x_y_data to JSON
    x_y_data_json = json.dumps(x_y_data)
    print(table_data) 

    context = {
        'data': x_y_data_json,
        'table_data': table_data
    }

    # print("Strategies: ", output_data['strategies'])
    return render(request, 'data3.html', context)


def process_form(rq):
    # Fetch form data
    start_date = rq.POST.get('start_date')
    end_date = rq.POST.get('end_date')
    
    # Calculation parameters
    return_calculation = rq.POST.get('return_calculation')
    price_frequency = rq.POST.get('price_frequency')
    risk_free_rate = float(rq.POST.get('risk_free_rate', 0))
    invested_amount = float(rq.POST.get('invested_amount', 0))
    
    # Optimization parameters
    benchmark_portfolio = rq.POST.get('benchmark_portfolio')
    trv_min = float(rq.POST.get('target_return_for_min_volatility', 0))
    trv_max = float(rq.POST.get('target_volatility_for_max_return', 0))
    default_min_weight = float(rq.POST.get('default_min_weight', 0))
    default_max_weight = float(rq.POST.get('default_max_weight', 0))
    frontier_runs = int(rq.POST.get('frontier_runs', 0))
    monte_carlo_simulations = int(rq.POST.get('monte_carlo_simulations', 0))
    solver = rq.POST.get('solver')
    dendogram_segment = rq.POST.get('dendogram_segment')
    
    # Ticker data - assuming the tickers and their related data are sent as lists
    tickers = rq.POST.getlist('tickers[]')  # Ticker symbols
    baw_list = rq.POST.getlist('baw[]')     # Benchmark asset weight
    amax_list = rq.POST.getlist('amax[]')   # Asset maximum weight
    ba_list = rq.POST.getlist('ba[]')       # Benchmark amount

    # Create the ticker data structure
    ticker_data = []
    for i in range(len(tickers)):
        ticker_data.append({
            "symbol": tickers[i],
            "benchmark_asset_weight": float(baw_list[i]),
            "asset_minimum_weight": 0,  # Modify this if you need it from form
            "asset_maximum_weight": float(amax_list[i]),
            "benchmark_amount": float(ba_list[i]),
            "stock_prices": []  # You can handle stock prices data here if needed
        })
    
    # Construct final JSON structure
    form_data = {
        "start_date": start_date,
        "end_date": end_date,
        "calculation_parameters": {
            "return_calculation": return_calculation,
            "price_frequency": price_frequency,
            "risk_free_rate": risk_free_rate,
            "invested_amount": invested_amount
        },
        "optimization_parameters": {
            "benchmark_portfolio": benchmark_portfolio,
            "target_return_for_min_volatility": trv_min,
            "target_volatility_for_max_return": trv_max,
            "default_min_weight": default_min_weight,
            "default_max_weight": default_max_weight,
            "frontier_runs": frontier_runs,
            "monte_carlo_simulations": monte_carlo_simulations,
            "benchmark_ticker": "^GSPC",  # Hardcoded for now, modify if needed
            "solver": solver,
            "dendogram_segment": dendogram_segment
        },
        "ticker_data": ticker_data
    }

    return form_data
    

def create_table(data):
    return {
            'Expected Return': f"{data['expected_return'] * 100:.2f}%",
            'Standard Deviation': f"{data['standard_deviation'] * 100:.2f}%",
            'Sharpe Ratio': f"{data['sharpe_ratio'] * 100:.2f}%",  
            'CVaR 90%': f"{data['cvar_090'] * 100:.2f}%",
            'CVaR 95%': f"{data['cvar_095'] * 100:.2f}%",
            'CVaR 99%': f"{data['cvar_099'] * 100:.2f}%",
            'Tracking Error': data['tracking_errors']
        }


def create_pie_chart(labels, values):
    colors = ['#FF5733', '#33FF57'] 
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textfont=dict(color='white'),
        hoverinfo='label+value',
        hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>',
        hoverlabel=dict(
            font=dict(family='Arial, sans-serif', size=14, color='white'),
            bgcolor='#ffffff',
            bordercolor='#FF0000'
        )
    )])
    fig.update_layout(
        template='plotly_white',
        legend=dict(yanchor="top", y=1.2, xanchor="center", x=0.5, orientation='h'),
    )
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def create_consolidate_table(all_symbols, consolidated_table):
    table_html = '<table class="table table-striped"><thead class="bg-dark text-light"><tr>'
    table_html += '<th>Strategy Name</th>'
    table_html += '<th>Expected Return (%)</th>'
    table_html += '<th>Standard Deviation (%)</th>'
    table_html += '<th>Sharpe Ratio</th>'
    
    # Add symbols as headers
    for symbol in all_symbols:
        table_html += f'<th>{symbol}</th>'
    
    table_html += '</tr></thead><tbody>'
    
    # Populate table rows
    for row in consolidated_table:
        table_html += '<tr>'
        table_html += f'<td>{row["strategy_name"]}</td>'
        table_html += f'<td>{row["expected_return"]}</td>'
        table_html += f'<td>{row["standard_deviation"]}</td>'
        table_html += f'<td>{row["sharpe_ratio"]}</td>'
        
        # Populate symbol values
        for symbol in all_symbols:
            table_html += f'<td>{row.get(symbol, "0.00%")}</td>'  # Default to "0.00%" if the symbol doesn't exist
            
        table_html += '</tr>'
    
    table_html += '</tbody></table>'

    return table_html


def create_return_risk_chart(frontier_runs, strategy_x, strategy_y, scatter_do_color, strategy_labels):
    frontier_x = frontier_runs['x']
    frontier_y = frontier_runs['y']

    fig = go.Figure()

    # Add Efficient Frontier (Blue Line)
    fig.add_trace(go.Scatter(
        x=frontier_x, 
        y=frontier_y, 
        mode='lines+markers', 
        name='Efficient Frontier',
        line=dict(color='blue'),
        marker=dict(color='blue')
    ))

    # Add Portfolio Strategy points (Yellow Dots)
    scatter_trace = go.Scatter(
        x=strategy_x, 
        y=strategy_y, 
        mode='markers+text',
        text=strategy_labels, 
        name='Strategies',
        marker=dict(color=scatter_do_color, size=10),
        textposition='top center',
        textfont=dict(
            family="Arial",  # Font family
            size=12,         # Font size
            color="black"    # Font color
        )
    )

    # Conditionally add the texttemplate if strategy_labels is not empty
    if strategy_labels and any(strategy_labels):
        scatter_trace['texttemplate'] = "<span style='border: 1px solid black; background-color: red; padding: 2px;'>%{text}</span>"

    # Add the trace to the figure
    fig.add_trace(scatter_trace)

    # Set axis titles and layout
    fig.update_layout(
        xaxis_title="Risk (%)",
        yaxis_title="Return (%)",
        legend=dict(yanchor="top", y=1.1, xanchor="center", x=0.5, orientation='h'),
    )

    # Convert Plotly figure to JSON
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)

    return graph_json


def api_data_view_4(request):
    if request.method == 'POST':
        form_data = process_form(request)
        print("=========================================================")
        print("Form Data: ", form_data)
        print("=========================================================")

        start_time = time.time()
        # Return-Risk Chart data
        frontier_runs = output_data['frontier_runs']
        strageties = output_data['frontier_positions']
        strategy_x = strageties['x']
        strategy_y = strageties['y']
        strategy_labels = strageties['strategy_names']
        scatter_do_color = 'orange'

        graph_json_1 = create_return_risk_chart(frontier_runs, strategy_x, strategy_y, scatter_do_color, strategy_labels)


        summary_tbl_data = output_data['strategies']
        summary_tbl = []
        for strategy in summary_tbl_data:
            if strategy['data'] is not None and strategy['data']['portfolio_summary'] is not None:
                portfolio_summary = strategy['data']['portfolio_summary']

                # Create a new dictionary with the required fields
                summary_item = {
                    'strategy_name': strategy['name'],
                    'expected_return': f"{portfolio_summary.get('annualized_mean', None)* 100:.2f}%",
                    'standard_deviation': f"{portfolio_summary.get('annualized_standard_deviation', None)* 100:.2f}%",
                    'sharpe_ratio': f"{portfolio_summary.get('annualized_sharpe_ratio', None)* 100:.2f}%",
                    'sortino_ratio': f"{portfolio_summary.get('annualized_sortino_ratio', None)* 100:.2f}%",
                    'cvar_090': f"{portfolio_summary.get('cvar_at_95', None)* 100:.2f}%",  # Adjust based on your requirements
                    'cvar_095': f"{portfolio_summary.get('cvar_at_95', None)* 100:.2f}%",  # Adjust based on your requirements
                    'cvar_099': f"{portfolio_summary.get('cvar_at_95', None)* 100:.2f}%"   # Adjust based on your requirements
                }

                # Append the summary_item to summary_tbl
                summary_tbl.append(summary_item)

        results = []
        consolidated_table = []
        all_symbols = set()
        strategy_expected_return = []
        strategy_standard_deviation = []

        for strategy in output_data['strategies']:
            strategy_data = strategy['data']
            if strategy_data is not None:
                allocation_data = strategy_data['symbol_allocations']
                strategy_expected_return.append(strategy_data['expected_return'])
                strategy_standard_deviation.append(strategy_data['standard_deviation'])
                labels = []
                allocations = []

                # Extract labels and allocations
                if isinstance(allocation_data, list) and len(allocation_data) > 0:
                    for label in allocation_data:
                        labels.append(label['symbol'])
                        allocations.append(label['allocation_weight'])
                        all_symbols.add(label['symbol'])  # Collect all symbols for the consolidated table

                elif isinstance(allocation_data, dict) and allocation_data:
                    labels.append(allocation_data['symbol'])
                    allocations.append(allocation_data['allocation_weight'])
                    all_symbols.add(allocation_data['symbol'])  # Collect all symbols for the consolidated table

                # Create the chart and table for the current strategy
                chart = create_pie_chart(labels, allocations)
                table = create_table(strategy_data)

                # Prepare the row for the consolidated table
                row = {
                    'strategy_name': strategy['name'],
                    'expected_return': f"{strategy_data['expected_return'] * 100:.2f}%",
                    'standard_deviation': f"{strategy_data['standard_deviation'] * 100:.2f}%",
                    'sharpe_ratio': f"{strategy_data['sharpe_ratio']:.2f}",
                }

                # Initialize allocation data for all symbols (default to 0.00%)
                for symbol in all_symbols:
                    row[symbol] = "0.00%"  # Start with 0.00% for every symbol

                # Populate allocation data for the current strategy
                if isinstance(allocation_data, list):
                    for allocation in allocation_data:
                        row[allocation['symbol']] = f"{allocation['allocation_weight'] * 100:.2f}%"
                elif isinstance(allocation_data, dict):
                    row[allocation_data['symbol']] = f"{allocation_data['allocation_weight'] * 100:.2f}%"

                # Append the row to the consolidated table
                consolidated_table.append(row)


                # Append the chart and table data to results
                results.append({
                    'strategy_name': strategy['name'],
                    'table_data': table,
                    'chart_data': chart
                })

        table_html = create_consolidate_table(all_symbols, consolidated_table)
        scatter_do_color = 'red'
        graph_json_2 = create_return_risk_chart(frontier_runs, strategy_expected_return, strategy_standard_deviation, scatter_do_color, [])
        end_time = time.time()
        # Calculate the processing time
        processing_time = end_time - start_time
    
        context = {
            'graph_json_1': graph_json_1,
            'graph_json_2': graph_json_2,
            'summary_tbl': summary_tbl,
            'strategies': results,
            'consolidated_table': consolidated_table,
            'all_symbols': all_symbols,
            'table_html': table_html,
            'processing_time': processing_time
        }

        # Pass the results to your template
        return render(request, 'data4.html', context)