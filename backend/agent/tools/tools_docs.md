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

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `problem` | `str` | Yes | The natural language question to convert to SQL |
| `context` | `Optional[Union[str, list[str]]]` | No | Additional contextual information to help generate more accurate queries |

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

| Column | Type | Description |
|--------|------|-------------|
| `title` | TEXT | Title of the artwork |
| `inception` | DATETIME | Date when the artwork was created |
| `movement` | TEXT | Art movement the artwork belongs to |
| `genre` | TEXT | Genre of the artwork |
| `image_url` | TEXT | URL of the artwork image |
| `img_path` | TEXT | Local system path to the artwork image |

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

##### _execute_sql_query Function
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

*Last Updated: December 1, 2025*