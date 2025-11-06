"use client";

import { useEffect, useRef, useState } from "react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { User, Bot } from "lucide-react";
import { cn } from "@/lib/utils";
import { BaseMessage, HumanMessage } from "@langchain/core/messages";
import { StickToBottom, useStickToBottomContext } from "use-stick-to-bottom";
import { get_message_history, query_agent } from "@/app/chat/route";
import { ChatForm } from "@/app/_components/chat-form";

function MessageComponent({ message }: { message: BaseMessage }) {
  // Simple styling based on the message type, replace with ui/avatar later
  const isHuman = message.type === "human";
  const isAI = message.type === "ai";

  return (
    <div
      className={cn(
        "mb-8 flex gap-4",
        isHuman ? "justify-end" : "justify-start"
      )}
    >
      {/* Ensure the side of chat bubble on previous parent div */}
      {/* Bot profile */}
      {isAI && (
        <Avatar className="h-8 w-8 shrink-0 bg-primary">
          <AvatarFallback className="bg-primary text-primary-foreground">
            <Bot className="h-5 w-5" />
          </AvatarFallback>
        </Avatar>
      )}

      {/* Use same chat bubble in centre but differ bg color based on type, this is a simple implementation useful for current usecase (focus on rendering ai and human message) */}
      <div
        className={cn(
          "max-w-[85%] rounded-2xl px-5 py-3.5",
          isHuman
            ? "bg-primary text-primary-foreground"
            : "bg-muted text-foreground"
        )}
      >
        <p className="text-[15px] leading-relaxed">
          {message.content as string}
        </p>
      </div>

      {/* User profile */}
      {isHuman && (
        <Avatar className="h-8 w-8 shrink-0 bg-secondary">
          <AvatarFallback className="bg-secondary text-secondary-foreground">
            <User className="h-5 w-5" />
          </AvatarFallback>
        </Avatar>
      )}
    </div>
  );
}

function ScrollToBottomButton() {
  // This utility component uses the context to manage manual scrolling
  const { isAtBottom, scrollToBottom } = useStickToBottomContext();

  return (
    !isAtBottom && (
      <button
        className="absolute right-4 bottom-4 p-2 bg-blue-500 text-white rounded-full shadow-lg z-10 hover:bg-blue-600 transition-colors"
        onClick={() => scrollToBottom()}
        aria-label="Scroll to bottom"
      >
        ⬇️
      </button>
    )
  );
}

export function ChatInterface({ thread_id }: { thread_id: string }) {
  const [messages, setMessages] = useState<BaseMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // use history in
  useEffect(() => {
    async function fetchHistory() {
      try {
        const history = await get_message_history(thread_id);
        setMessages(history);
      } catch (error) {
        console.error("Failed to fetch history: ", error);
      }
    }
    fetchHistory();
  }, [thread_id]);

  const handleQuery = async (query: string) => {
    if (isLoading) return;

    // Consider add auto scroll to bottom on query handle

    const newMessage: HumanMessage = new HumanMessage(query);
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    setIsLoading(true);

    try {
      const response = await query_agent(thread_id, query);
      setMessages((prev) => [...prev, response.messages.at(-1)]);
    } catch (error) {
      console.error("Agent query failed: ", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[85vh] w-1/2 bg-transparent ">
      <StickToBottom
        className="flex-1 overflow-hidden relative" // flex-1 allows it to fill the available space
        resize="smooth" // Recommended for chat apps
        // initial={{ mass: 10 }} // You can pass animation props here if needed
      >
        <StickToBottom.Content className="flex flex-col gap-3 p-4 overflow-y-auto">
          {/* 🚀 Rendering the BaseMessage array here */}
          {messages.length === 0 && (
            <p className="text-center text-gray-500 mt-10">
              .message.content Start the conversation...
            </p>
          )}
          {messages.map((message, index) => (
            <MessageComponent key={index} message={message} />
          ))}
        </StickToBottom.Content>

        {/* The 'Scroll to Bottom' button shows up when the user scrolls up */}
        <ScrollToBottomButton />
      </StickToBottom>

      {/* Input Area (Outside the scrolling container) */}
      <div className="p-4 border-t border-gray-200 flex gap-2 w-full ">
        <ChatForm submitHandler={handleQuery} />
        {/* <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleQuery(input)}
          placeholder="Send a message..."
          className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={() => handleQuery(input)}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-400"
          disabled={!input.trim()}
        >
          Send
        </button> */}
      </div>
    </div>
  );
}
