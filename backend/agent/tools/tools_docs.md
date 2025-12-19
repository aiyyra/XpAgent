# Agent Tools Documentation

This document provides comprehensive documentation for all tools available in the agent system.

## SQL Tools

### text2sql Tool

**Module**: `SQL.py`  
**Function**: `get_text2sql_tools(llm: ChatOpenAI, db_path: str)`  
**Tool Name**: `text2sql`

#### Overview

The `text2sql` tool converts natural language questions into executable SQL queries for artwork database analysis. It leverages LangChain with OpenAI's structured output capabilities to generate accurate SQL queries based on user questions and optional contextual information.

#### Function Signature

```python
text2sql(problem: str, context: Optional[Union[str, list[str]]] = None) -> Dict[str, Any]
```

#### Parameters

| Parameter | Type                              | Required | Description                                                              |
| --------- | --------------------------------- | -------- | ------------------------------------------------------------------------ |
| `problem` | `str`                             | Yes      | The natural language question to convert to SQL                          |
| `context` | `Optional[Union[str, list[str]]]` | No       | Additional contextual information to help generate more accurate queries |

#### Context Parameter Details

The `context` parameter accepts three possible value types:

1. **None** (default): No additional context provided

   ```python
   text2sql("Show me all Renaissance artworks")
   ```

2. **String**: Single contextual information

   ```python
   text2sql(
       problem="Show me similar artworks",
       context="Previous query returned 'The Starry Night' by Van Gogh from Post-Impressionism"
   )
   ```

3. **List of Strings**: Multiple pieces of contextual information
   ```python
   text2sql(
       problem="Compare artworks by style",
       context=[
           "User prefers Impressionist paintings",
           "Focus on 19th century works",
           "Include image paths for visualization"
       ]
   )
   ```

#### Database Schema

The tool works with an artwork database containing the following columns:

| Column      | Type     | Description                            |
| ----------- | -------- | -------------------------------------- |
| `title`     | TEXT     | Title of the artwork                   |
| `inception` | DATETIME | Date when the artwork was created      |
| `movement`  | TEXT     | Art movement the artwork belongs to    |
| `genre`     | TEXT     | Genre of the artwork                   |
| `image_url` | TEXT     | URL of the artwork image               |
| `img_path`  | TEXT     | Local system path to the artwork image |

#### Return Value

Returns a dictionary with the following structure:

**Success Response:**

```python
{
    "status": "success",
    "data": [
        {
            "title": "The Starry Night",
            "inception": "1889-06-01",
            "movement": "Post-Impressionism",
            # ... other columns
        }
    ]
}
```

**Error Response:**

```python
{
    "status": "error",
    "message": "Error description"
}
```

#### Key Features

1. **Structured Output**: Uses Pydantic model `ExecuteCode` to ensure consistent SQL generation with reasoning
2. **Context Integration**: Incorporates contextual information from previous tasks or user preferences
3. **Self-Debugging**: Automatically attempts to fix SQL errors with a second generation pass
4. **SQLite Optimization**: Specifically designed for SQLite databases with artwork data
5. **Image Path Retrieval**: Automatically includes `img_path` when image analysis is needed

#### Business Rules

The tool implements specific business logic:

1. **Century Calculation**:

   ```sql
   (CAST(strftime('%Y', inception) AS INTEGER) - 1) / 100 + 1
   ```

2. **Current Time Reference**: Uses `strftime('2105-12-31 23:59:59')` for "now" or "current_time"

#### Error Handling

The tool includes a sophisticated error handling mechanism:

1. **First Attempt**: Executes generated SQL query
2. **Error Detection**: Catches execution exceptions
3. **Self-Debug**: Generates error handling prompt with the error message
4. **Second Attempt**: Re-generates SQL query with error context
5. **Fallback**: Returns error message if second attempt also fails

#### Internal Components

##### ExecuteCode Pydantic Model

```python
class ExecuteCode(BaseModel):
    reasoning: str = Field(..., description="Reasoning behind the SQL expression")
    SQL: str = Field(..., description="Executable SQL code")
```

##### \_execute_sql_query Function

```python
def _execute_sql_query(query: str, db_path: str, as_dict=True) -> Dict[str, Any]
```

- Executes SQL queries against SQLite database
- Returns results as dictionaries when `as_dict=True`
- Includes debug printing for query and results

#### Usage Examples

##### Basic Query

```python
result = text2sql("Show me all Impressionist paintings")
```

##### Query with Context

```python
result = text2sql(
    problem="Find artworks for comparison",
    context="User analyzed Renaissance period in previous step"
)
```

##### Multi-Context Query

```python
result = text2sql(
    problem="Create a visualization dataset",
    context=[
        "Need data for plotting tool",
        "Focus on 19th century",
        "Include image paths for visual analysis"
    ]
)
```

#### Integration Notes

- **LangChain Integration**: Uses `ChatPromptTemplate` and `MessagesPlaceholder` for context handling
- **OpenAI Compatibility**: Optimized for OpenAI's structured output patterns
- **Tool Registration**: Registered as `StructuredTool` for agent framework integration

#### Dependencies

- `langchain_openai.ChatOpenAI`
- `langchain_core.messages.HumanMessage`
- `langchain_core.prompts.ChatPromptTemplate`
- `langchain_core.tools.StructuredTool`
- `sqlite3` (for database operations)
- `agent.src.utils._get_db_schema`

---

## Data Plotting Tools

### data_plotting Tool

**Module**: `plot.py`  
**Function**: `get_plotting_tools(llm: ChatOpenAI, log_path: str)`  
**Tool Name**: `data_plotting`

#### Overview

The `data_plotting` tool analyzes data and creates appropriate visualizations to answer user queries. It generates Python code using matplotlib to create charts and plots, automatically saving them as PNG files to a specified directory. The tool uses LangChain with structured output to ensure reliable plot generation.

#### Function Signature

```python
data_plotting(question: str, context: Union[str, List[str], dict] = None, config: Optional[RunnableConfig] = None) -> str
```

#### Parameters

| Parameter  | Type                          | Required | Description                                      |
| ---------- | ----------------------------- | -------- | ------------------------------------------------ |
| `question` | `str`                         | Yes      | The user's question or request for visualization |
| `context`  | `Union[str, List[str], dict]` | No       | Data from previous steps to be plotted           |
| `config`   | `Optional[RunnableConfig]`    | No       | LangChain runnable configuration                 |

#### Context Parameter Details

The `context` parameter can accept multiple formats:

1. **String**: Serialized data or simple context

   ```python
   data_plotting(
       question="Plot the distribution of artworks by century",
       context="[{'century': 19, 'count': 45}, {'century': 20, 'count': 78}]"
   )
   ```

2. **List**: Multiple data points or context strings

   ```python
   data_plotting(
       question="Create a comparison chart",
       context=["Data from SQL query", "Include legend", "Use bar chart"]
   )
   ```

3. **Dictionary**: Structured data with keys
   ```python
   data_plotting(
       question="Show trends over time",
       context={'data': [{'year': 1880, 'paintings': 12}, ...]}
   )
   ```

#### Key Features

1. **Automatic Visualization Selection**: Analyzes data and question to determine the most suitable chart type
2. **Headless Execution**: Uses matplotlib's 'Agg' backend to prevent GUI issues in async environments
3. **Error Handling**: Automatically attempts to fix code errors with a second generation pass
4. **PNG Export**: Saves all plots as PNG files to the specified log path
5. **Code Extraction**: Handles both plain code and markdown code blocks

#### System Behavior

The tool follows these guidelines:

- Minimizes plotting actions for efficiency
- Does not create sample data - only uses provided data
- Saves plots with proper filenames and `.png` extension
- Uses non-blocking matplotlib configuration for async compatibility
- Returns the generated Python code on success

#### Matplotlib Configuration

The tool enforces proper matplotlib usage for server environments:

```python
import matplotlib
matplotlib.use("Agg")   # Set backend before pyplot import
import matplotlib.pyplot as plt

plt.figure()
# ... plotting code ...
plt.savefig("out.png")
plt.close()
```

#### Return Values

**Success Response:**

````python
"Plot created successfully!:\n```python\n{generated_code}\n```\nStdout: {execution_result}"
````

**Error Response:**

```python
"Failed to execute. Error: {error_message}"
```

#### Internal Components

##### ExecuteCode Pydantic Model

```python
class ExecuteCode(BaseModel):
    reasoning: str = Field(..., description="Reasoning behind the visualization")
    code: str = Field(..., description="Python code to execute")
```

##### PythonREPL Class

- Executes Python code using `PythonAstREPLTool`
- Extracts code from markdown blocks
- Provides error handling for execution failures

#### Usage Examples

##### Basic Plotting

```python
result = data_plotting(
    question="Create a bar chart showing artwork distribution",
    context="[{'movement': 'Impressionism', 'count': 45}, {'movement': 'Cubism', 'count': 32}]"
)
```

##### Time Series Visualization

```python
result = data_plotting(
    question="Show artwork creation trends over centuries",
    context={'data': [{'century': 18, 'artworks': 120}, {'century': 19, 'artworks': 340}]}
)
```

##### Multi-Context Plotting

```python
result = data_plotting(
    question="Compare genres with custom styling",
    context=["Data: [{'genre': 'Portrait', 'count': 56}]", "Use warm colors", "Add grid"]
)
```

#### Integration Notes

- **LangChain Integration**: Uses `ChatPromptTemplate` for prompt management
- **PythonAstREPLTool**: Safely executes generated Python code
- **Log Path**: Automatically appends save location to context
- **Tool Registration**: Registered as `StructuredTool` for agent framework

#### Dependencies

- `langchain_openai.ChatOpenAI`
- `langchain_core.tools.StructuredTool`
- `langchain_experimental.tools.PythonAstREPLTool`
- `matplotlib` (with Agg backend)
- `PIL` (Pillow)

---

## Data Preparation Tools

### data_preparation Tool

**Module**: `data.py`  
**Function**: `get_data_preparation_tools(llm: ChatOpenAI, log_path: str)`  
**Tool Name**: `data_preparation`

#### Overview

The `data_preparation` tool processes and transforms raw data into properly structured formats suitable for downstream tasks like plotting or analysis. It generates Python code to clean, transform, and organize data according to user requirements, ensuring all data points are preserved and properly labeled.

#### Function Signature

```python
data_preparation(question: str, context: Union[str, List[str], dict] = None, config: Optional[RunnableConfig] = None) -> str
```

#### Parameters

| Parameter  | Type                          | Required | Description                             |
| ---------- | ----------------------------- | -------- | --------------------------------------- |
| `question` | `str`                         | Yes      | The data preparation task or question   |
| `context`  | `Union[str, List[str], dict]` | No       | Raw data from previous steps to process |
| `config`   | `Optional[RunnableConfig]`    | No       | LangChain runnable configuration        |

#### Context Parameter Details

Similar to the plotting tool, context can be:

1. **String**: Raw data as serialized string

   ```python
   data_preparation(
       question="Prepare data for plotting",
       context="[{'title': 'Mona Lisa', 'year': 1503}, ...]"
   )
   ```

2. **List**: Multiple data sources or instructions

   ```python
   data_preparation(
       question="Merge and clean datasets",
       context=["Dataset 1: {...}", "Dataset 2: {...}", "Remove nulls"]
   )
   ```

3. **Dictionary**: Structured input data
   ```python
   data_preparation(
       question="Format for visualization",
       context={'raw_data': [...], 'columns': ['x', 'y']}
   )
   ```

#### Key Features

1. **Data Preservation**: Ensures all input data is included without truncation
2. **Automatic Labeling**: Provides meaningful names/captions for each value
3. **No Sample Data**: Only processes provided data, never creates synthetic data
4. **File Output**: Saves processed data to specified directory
5. **Structured Output**: Returns final data structure in standardized format
6. **Error Recovery**: Automatically retries with error correction on failure

#### System Guidelines

The tool adheres to these principles:

- Minimizes data preparation actions for efficiency
- Prevents data truncation (no `# ... (rest of the data)` comments)
- Provides descriptive labels considering context and question
- Prints and returns the final data structure
- Saves processed data to log path

#### Return Values

**Success Response:**
Returns the final data structure as a string (from the `data` field of the model)

**Error Response:**

```python
"Failed to execute. Error: {error_message}"
```

Or the reasoning if no code was generated

#### Internal Components

##### ExecuteCode Pydantic Model

```python
class ExecuteCode(BaseModel):
    reasoning: str = Field(..., description="Reasoning behind the data processing")
    code: str = Field(..., description="Python code to execute")
    data: str = Field(..., description="Final data structure output")
```

Note: This model includes an additional `data` field to capture the processed output.

##### PythonREPL Class

- Executes data processing code using `PythonAstREPLTool`
- Handles code block extraction
- Returns execution results or error messages

#### Usage Examples

##### Basic Data Structuring

```python
result = data_preparation(
    question="Organize artwork data for bar chart",
    context="[{'title': 'Starry Night', 'movement': 'Post-Impressionism', 'year': 1889}, ...]"
)
```

##### Data Aggregation

```python
result = data_preparation(
    question="Count artworks by century and add labels",
    context={'artworks': [{'inception': '1889-01-01'}, {'inception': '1920-05-15'}, ...]}
)
```

##### Multi-Step Processing

```python
result = data_preparation(
    question="Clean, filter, and format data",
    context=[
        "Raw data: [{'title': 'Art1', 'year': None}, ...]",
        "Remove entries with missing years",
        "Sort by year ascending"
    ]
)
```

#### Error Handling

The tool implements robust error handling:

1. **First Attempt**: Executes generated code
2. **Error Detection**: Catches execution exceptions
3. **Self-Correction**: Generates fix prompt with error details
4. **Second Attempt**: Re-generates and executes corrected code
5. **Fallback**: Returns error representation if second attempt fails

#### Integration Notes

- **LangChain Integration**: Uses `ChatPromptTemplate` and structured output
- **Code Execution**: Leverages `PythonAstREPLTool` for safe execution
- **Output Handling**: Returns data from the `data` field of the model
- **Tool Registration**: Registered as `StructuredTool` for agent framework

#### Dependencies

- `langchain_openai.ChatOpenAI`
- `langchain_core.tools.StructuredTool`
- `langchain_experimental.tools.PythonAstREPLTool`
- `pydantic` (for data models)
- `json` (for data serialization)

---

## Visual QA Tools

### visual_qa Tool

**Module**: `visual_qa.py`  
**Status**: ⚠️ Not Implemented

The `visual_qa.py` file exists but is currently empty. This tool is planned for future implementation and will likely handle visual question-answering tasks for artwork images.

---

_Last Updated: December 7, 2025_
