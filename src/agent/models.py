from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.exceptions import OutputParserException
from langchain.output_parsers import CommaSeparatedListOutputParser


# Define your desired data structure.
class DataFrameDescription(BaseModel):
    description: str = Field(description="Description about the pandas data frame ")

# Define your desired data structure.
class VerticalBarPlotCategorical(BaseModel):
    question: str = Field(description="question to be analysed")
    df: str = Field(description="Name of the pandas dataframe")
    categorical_column: str = Field(description="name of the categorical column from the dataframe")
    numeric_column: str = Field(description="name of the numeric column from the dataframe")
    agg_func: str = Field(description="Aggregation function to be used for the aggregation of dataframe")
    title: str = Field(description="Title of the plotly figure")
    xlabel: str = Field(description="Label to be used for categorical variable in the x-axis")
    ylabel: str = Field(description="Label to be used for the aggregated numeric variable in the y-axis")

# Define your desired data structure.
class ScatterPlotTwoVariables(BaseModel):
    question: str = Field(
        description="question to be analysed using scatter plot"
    )
    x_numeric_column: str = Field(
        description="name of the numeric column from the dataframe for the x-axis"
    )
    y_numeric_column: str = Field(
        description="name of the numeric column from the dataframe for the y-axis"
    )
    title: str = Field(description="Title of the plotly figure")
    xlabel: str = Field(description="Label to be used for categorical variable in the x-axis")
    ylabel: str = Field(description="Label to be used for the aggregated numeric variable in the y-axis")


def ai_viz_call(meta, doc_string, vis_pydantic_object):
    llm = ChatOllama(model="llama3")
    prompt = ChatPromptTemplate.from_template(
        """
        You are an data analytics and visualization expert with business domain knowledge.
        use the meta-data about the pandas data frame to generate a business question which
        can be answered using the plotly visualization function. description of the plotly
        visualization function is provided in the DOC_STRING 

        # meta-data about the data frame is provided in the CONTEXT section
            - meta-data contains row-wise information about the data-frame. meta-data has 
                following information
                - COLUMNS: contains list of columns in the data-frame
                - DTYPE: contains data type of the column in the data-frame
        # plotly visualization function description is provided in the DOC_STRING section

        use the doc string to return the json object which should only consist keys as 
        parameters for the plotly visualization funciton. json object should have all the
        parameters as json keys and values of keys based on question generated using the meta-data
        in context
        
        CONTEXT: {context}

        DOC_STRING: {doc_string}
        
        Do not include any explanation and result should only be a json object

        """
    )

    parser = JsonOutputParser(pydantic_object=vis_pydantic_object)

    chain = prompt | llm | JsonOutputParser()

    response = dict()

    try:
        response = chain.invoke({"context": meta, "doc_string": doc_string})
        print(response)
    except OutputParserException:
        print("Json Parsing error trying again")

    return response

def ai_df_desc_call(sample_data):
    llm = ChatOllama(model="llama3")
    prompt = ChatPromptTemplate.from_template(
        """
        ###
        You are an data analytics with business domain knowledge.
        Based on the sample data provided in CONTEXT section 

        ### Generate the small general description about the dataset

        ###
        CONTEXT: {sample_data}
        """
    )

    parser = JsonOutputParser(pydantic_object=DataFrameDescription)

    chain = prompt | llm

    response = dict()

    try:
        response = chain.invoke({ "sample_data": sample_data})
        print(response)
    except OutputParserException:
        print("Json Parsing error trying again")

    return response

def ai_csv_paraser(context):
    llm = ChatOllama(model="llama3")
    output_parser = CommaSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()
    prompt = PromptTemplate(
        template="""
            List twenty questions which can be used for data exploration 
            based on sample data provided in context\n
            CONTEXT: {context}.\n{format_instructions}
        """,
        input_variables=["context"],
        partial_variables={"format_instructions": format_instructions},
    )



    chain = prompt | llm | output_parser

    response = chain.invoke({"context": context})

    return response



def llm_message():
    llm = ChatOllama(model="llama3")
    prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"topic": "Some Random Topic"})