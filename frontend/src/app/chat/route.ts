// consider create a [slug] folder to get user id and append it with the url

export async function GET() {
  const data = await fetch('http://localhost:8000/api/v1/health');
  const result = await data.json();
  return Response.json(result);
  // return Response.json({ message: 'Hello World' })
}

// Get thread list
export async function get_thread_list() {
  const data = await fetch('http://localhost:8000/api/v1/allThread');
  const result = await data.json();
  return result;
}

// Create a new thread with post to thread
export async function create_new_thread_id() {
  const res = await fetch('http://localhost:8000/api/v1/thread', {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
    }
  });
  if (!res.ok) throw new Error(`Backend returned ${res.status}`);
  const data = await res.json();
  return data.session_id;
}

export async function query_agent(thread_id: string, query: string) {
  const data = await fetch(`http://localhost:8000/api/v1/thread/${thread_id}/query`, {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ "query": query }),
  });

  if (!data.ok) {
    // Optional: throw an error or handle the bad response gracefully
    const errorBody = await data.text();
    console.error(`Fetch failed with status ${data.status}: ${errorBody}`);
    throw new Error(`Failed to query agent for thread ${thread_id}. Status: ${data.status}`);
  }

  const result = await data.json();
  return result;
}

// Get message history
export async function get_message_history(thread_id: string) {
  // const data = await fetch(`http://localhost:8000/api/v1/thread/${slug}`);
  // const thread_data = await data.json();
  const data = await fetch(`http://localhost:8000/api/v1/thread/${thread_id}/`, {
    method: 'GET', 
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const result =  data.json();
  return result;
}
