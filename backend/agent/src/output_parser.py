import ast
import re 

from langchain.tools import BaseTool
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseTransformOutputParser

import logging
from typing import Any, Dict, Iterator, List, Literal, Optional, Sequence, Tuple, TypedDict, Union

logger = logging.getLogger(__name__)

# Regex patterns to parse
THOUGHT_PATTERN = r"Thought: ([^\n]*)"
ACTION_PATTERN = r"\n*(\d+)\. (\w+)\((.*)\)(\s*#\w+\n)?"
# $1 or ${1} -> 1
ID_PATTERN = r"\$\{?(\d+)\}?"
END_OF_PLAN = "<END_OF_PLAN>"

# Helper function
def _ast_parse(arg: str) -> Any:
    try:
        return ast.literal_eval(arg)
    except :
        return arg
    
def _parse_xmode_action_args(args: str, tool: Union[str, BaseTool]) -> Dict[str, Any]:
    """Parse arguments from a string.""" # use llm list of tasks, parse the args to create a task object
    if args == "":
        return {}
    if isinstance(tool, str):
        return {} # joins 
    extracted_args = {}
    tool_key = None
    prev_idx = None
    for key in tool.args.keys():
        # Split if present
        if f"{key}=" in args:
            idx = args.index(f"{key}=")
            if prev_idx is not None:
                extracted_args[tool_key] = _ast_parse(
                    args[prev_idx:idx].strip().rstrip(",")
                )
            args = args.split(f"{key}=")[1]
            tool_key = key
            prev_idx = 0
    if prev_idx is not None:
        extracted_args[tool_key] = _ast_parse(
            args[prev_idx:].strip().rstrip(",").rstrip(")")
            )
    return extracted_args

def default_dependancy_rule(idx, args: str):
    matches = re.findall(ID_PATTERN, args)
    numbers = [int(match) for match in matches]
    return idx in numbers

def _get_dependencies_from_graph(
    idx: int,
    tool_name: str,
    args: Dict[str, Any],
) -> List[int]:
    """Get dependencies from the graph."""
    if tool_name == "join":
        return list(range(1, idx))
    return [i for i in range(1, idx) if default_dependancy_rule(i, str(args))]

class Task(TypedDict):
    idx: int
    tool: Union[str, BaseTool]
    args: Dict[str, Any]
    dependencies: List[int]
    thought: Optional[str]

def instantiate_task(
    tools: Sequence[BaseTool],
    idx: int,
    tool_name : str,
    args: Union[str, Any],
    thought : Optional[str] = None,
) -> Task:
    if tool_name == "join":
        tool = "join"
    else:
        try:
            tool = tools[[tool.name for tool in tools].index(tool_name)]
        except ValueError as err:
            raise OutputParserException(f"Tool {tool_name} not found.") from err
        
    tool_args = _parse_xmode_action_args(args, tool)
    dependencies = _get_dependencies_from_graph(idx, tool_name, tool_args)

    return Task(
        idx=idx,
        tool=tool,
        args=tool_args,
        dependencies=dependencies,
        thought=thought,
    )

class M3LXPlanParser(BaseTransformOutputParser[dict], extra="allow"):
    """Planning output parser."""

    tools : Sequence[BaseTool] 

    # Override _transform to return a list of tasks?
    def _transform(self, input: Iterator[Union[str, BaseMessage]]) -> Iterator[Task]:
        texts = []
        # TODO: cleanup tuple state tracking here
        thought = None
        for chunk in input:
            # Assume chunk is str. TODO: support vision/other format
            text = chunk if isinstance(chunk, str) else str(chunk.content)
            for task, thought in self.ingest_token(text, texts, thought):
                yield task
        # Final possible task
        if texts:
            task, _ = self._parse_task("".join(texts), thought)
            if task:
                yield task 


    def parse(
            self, 
            text: str,
    ) -> List[Task]:
        out = list(self._transform([text]))  # type: ignore
        print("Output plan: ", out)
        return out

    def stream(
        self,
        input: str | BaseMessage,
        config: RunnableConfig | None = None,
        **kwargs: Any | None, 
    ) -> Iterator[Task]:
        yield from self.transform([input], config, **kwargs) # type: ignore

    def ingest_token(
        self, 
        token: str,
        buffer: List[str],
        thought: Optional[str] = None,    
    ) -> Iterator[Tuple[Task, str | None]]: #change Optional[Task] cause it seems unnecessary?
        buffer.append(token)
        if "\n" in token:
            buffer_ = "".join(buffer).split("\n")
            suffix = buffer_[-1]
            for line in buffer_[:-1]:
                task, thought = self._parse_task(line, thought)
                if task:
                    yield task, thought
            buffer.clear()
            buffer.append(suffix)

    def _parse_task(
         self, 
         line: str,
         thought: Optional[str] = None,   
    ):
        task = None
        if match := re.match(THOUGHT_PATTERN, line):
            thought = match.group(1)
        elif match := re.match(ACTION_PATTERN, line):
            # if action is parsed, return task and clear buffer
            idx, tool_name, args, _ = match.groups()
            idx = int(idx)
            task = instantiate_task(
                # not sure why it error here
                tools=self.tools, # type: ignore
                idx=idx,
                tool_name=tool_name,
                args=args,
                thought=thought,
            )
            thought = None
        # Else it is just drop
        return task, thought
        
    