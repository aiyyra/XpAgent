from typing import Any, Dict, Optional, Union
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from langchain_community.utilities import SQLDatabase

from sqlalchemy import create_engine

from agent.src.utils import _get_db_schema

_meta_data="""
The column 'title' in the table contains the title of the artwork. Type: TEXT.
The column 'inception' in the table contains the date when the artwork was created. Type: DATETIME.
The column 'movement' in the table contains the art movement that the artwork belongs to. Type: TEXT.
The column 'genre' in the table contains the genre of the artwork. Type: TEXT.
The column 'image_url' in the table contains the URL of the image of the artwork. Type: TEXT.
The column 'img_path' in the table contains the path to the image of the artwork in the local system. Type: TEXT.
"""

_DESCRIPTION = (
    "text2SQL(problem: str, context: Optional[Union[str,list[str]]])-->str\n"
    "The input for this tools should be `problem` as a textual question\n"
    # Context specific rules below
    " - You can optionally provide a list of strings as `context` to help the agent solve the problem. "
    "If there are multiple contexts you need to answer the question, you can provide them as a list of strings.\n"
    "In the 'context' you could add any other information that you think is required to generate te SQL code. It can be the information from previous taks.\n" 
    "This tools is able to translate the question to the SQL code considering the database information.\n"
    "The SQL code can be executed using sqlite3 library.\n"
    "Use the output of running generated SQL code to answer the question.\n"
    
)


_SYSTEM_PROMPT = """  
You are a database expert. Generate a SQL query given the following user question, database information and other context that you receive.
You should analyse the question, context and the database schema and come with the executabel sqlite3 query. 
Provide all the required information in the SQL code to answer the original user question that may required in other tasks utilizing the relevant database schema.
Ensure you include all necessary information, including columns used for filtering, especially when the task involves plotting or data exploration.
This must be taken into account when performing any time-based data queries or analyses.
if the question asks for information that is not found in the database schema, you must retrieve the `ima_path` for image analysis task.
Translate a text question into a SQL query that can be executed on the SQLite database.
List of Businnes Roles to take into account during the translation task:
1- To calculate century from inception field use : (CAST(strftime('%Y', inception) AS INTEGER) - 1) / 100 + 1
....
"""
#If you want to consider "now" or "current_time", then replace them with strftime('2105-12-31 23:59:59').
_ADDITIONAL_CONTEXT_PROMPT = """
"""

# Pydantic Model to force Structured Output
class ExecuteCode(BaseModel):
    reasoning: str = Field(
        ..., # `...` = required fields
        description="The reasoning behind the SQL expression, including how context is included, if applicable.",
    )

    SQL: str = Field(
        ...,
        description="The SQL Code that can be runnable on the corresponding database ",
    )

def _execute_sql_query(query: str, db_path: str, as_dict=True) -> Dict[str, Any]:
    try:
        if as_dict:
            import sqlite3 # we use sqlite for the ArtWork database
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row # to return the results as dictionary
            cursor = conn.cursor()
            print("SQL: ", query) # Checking the query
            cursor.execute(query)
            results = [dict(row) for row in cursor.fetchall()]
            print("Results from sql execution: ", results) # Checking the results from given query
        else:
            engine = create_engine(f'sqlite:///{db_path}')
            database = SQLDatabase(engine, sample_rows_in_table_info=0)
            results = database.run(query)
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_text2sql_tools(llm: ChatOpenAI, db_path: str): # specific to OpenAI as its output pattern correlate well with prompt, may change later
    """
    Provide the SQL code from a given question.

    Args:
        raw_question (str): The raw user question.
        schema (str): The database information such as the Tables and Columns.

    Returns:
        results (SQL QUERY str)
    """

    _db_schema = _get_db_schema(db_path)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", _SYSTEM_PROMPT),
            ("user", "{problem}"),
            ("user", f"{_db_schema}\n{_meta_data}"), # We pass schema with explanation for the tables. **Unique for each database**
            MessagesPlaceholder(variable_name="info", optional=True)
        ]
    )

    extractor = prompt | llm.with_structured_output(ExecuteCode) # prompt and extract sql query

    def text2sql(
            problem: str,
            context: Optional[Union[str,list[str]]] = None,
    ):
        chain_input: Dict[str, Union[str, list[HumanMessage]]] = {"problem": problem}
        if context:
            # Make sure the context is 1 single string
            if isinstance(context, list):
                context_str = "\n".join(context)
            else:
                context_str = context
            # Add context to the chain input if available
            chain_input["info"] = [HumanMessage(content=context_str)]
        code_model = extractor.invoke(chain_input) # get the sql query
        try:
            return _execute_sql_query(code_model.SQL, db_path) # type: ignore
        except Exception as e:
            # self debug
            err = repr(e)
            _error_handling_prompt = f"Something went wrong on executing SQL: `{code_model.SQL}`. This is the error I got: `{err}`. \\ Can you fixed the problem and write the fixed SQL code?" # type: ignore
            chain_input["info"] = [HumanMessage(content=[context_str, _error_handling_prompt])]
            # Another try after one self debug
            code_model = extractor.invoke(chain_input)
            try:
                return _execute_sql_query(code_model.SQL, db_path) # type: ignore
            except Exception as e:
                return repr(e)
            
    return StructuredTool.from_function(
        name="text2SQL", 
        func=text2sql, 
        description=_DESCRIPTION, 
    )
                 




        

