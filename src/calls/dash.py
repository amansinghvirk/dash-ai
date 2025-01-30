import pandas as pd
import plotly.graph_objs as go
from src.dataframe.df_meta import get_dataframe_info
from src.agent.models import (
    ai_viz_call,
    VerticalBarPlotCategorical,
    ScatterPlotTwoVariables
)
from src.plots.plots import (
    bar_plot_for_categorical_variable_v,
    scatter_plot_two_variables
)

class ColumnNotInDataFrame(Exception):
    pass

def validate_columns(col, df):
    if col in df.columns:
        return True
    return False

def ai_call_bar_plot_for_categorical_variables_v(
    df: pd.DataFrame,
    max_retries=10
) -> go.Figure:
    meta = get_dataframe_info(df).to_markdown()

    fig = go.Figure()

    for i_try in range(max_retries):
        try:
            llm_response = ai_viz_call(
                meta,
                bar_plot_for_categorical_variable_v.__doc__,
                VerticalBarPlotCategorical
            )

            if (('categorical_variable' not in llm_response.keys())
                | (validate_columns(llm_response['categorical_variable'], df) == False)):
                raise ColumnNotInDataFrame

            if (('numeric_variable' not in llm_response.keys())
                | (validate_columns(llm_response['numeric_variable'], df) == False)):
                raise ColumnNotInDataFrame

            fig = bar_plot_for_categorical_variable_v(
                llm_response['question'],
                df.copy(), 
                llm_response['categorical_variable'],
                llm_response['numeric_variable'],
                llm_response['agg_func'],
                llm_response['title'],
                llm_response['xlabel'],
                llm_response['ylabel']  
            )

            break
        except Exception as e:
            print(e)
            print("Trying again.")

    return llm_response['question'], fig

def ai_call_scatter_plot_for_two_variables(
    df: pd.DataFrame,
    max_retries=10
) -> go.Figure:
    meta = get_dataframe_info(df).to_markdown()

    fig = go.Figure()

    for i_try in range(max_retries):
        try:
            llm_response = ai_viz_call(
                meta,
                scatter_plot_two_variables.__doc__,
                ScatterPlotTwoVariables
            )
            print(llm_response)

            if (('x_numeric_variable' not in llm_response.keys())
                | (validate_columns(llm_response['x_numeric_variable'], df) == False)):
                raise ColumnNotInDataFrame
            if (('x_numeric_variable' not in llm_response.keys())
                | (validate_columns(llm_response['x_numeric_variable'], df) == False)):
                raise ColumnNotInDataFrame


            fig = scatter_plot_two_variables(
                llm_response['question'],
                df.copy(), 
                llm_response['x_numeric_variable'],
                llm_response['y_numeric_variable'],
                llm_response['title'],
                llm_response['xlabel'],
                llm_response['ylabel']  
            )

            break
        except Exception as e:
            print(e)
            print("Trying again.")

    return llm_response['question'], fig

