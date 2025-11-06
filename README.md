### Update 6/11:

- great day
- first time pushing the project to a github repo
- frontend works well except sidebar is only dummy data
- backend still use dummy agent that doesnt rely on any API call (saves my money??)
- the project is still working with invoke (no streaming yet)

## frontend

- sidebar is still bad. Fetch from database for sidebar content (current is dummy data)
- still think auth is not useful for this project. Might change later?
- Support tool call and HITL rendering

## backend

- not much to do as the backend is not that complex
- consider rate limiting
- auth (if implemented) will be handled here

## agent

- re implement to actual agent architecture (when we are ready to waste money)
- update the MCP for image tooling
- include HITL
- Experiment with streaming

---

# Project as a whole:

- UI is bearable for manual testing
- Agent is still not tested with HITL
- Agent is still not tested with streaming
- Agent is still not tested with image tooling
- MCP is tested but not sure how it will rendered in the UI
- No support for graphing and Image modality yet
- Would love to include binary file as a modality (Parquet?)
