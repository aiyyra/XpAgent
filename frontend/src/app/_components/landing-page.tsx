"use client";
import TopSection from "./top-section";
import { ChatForm } from "./chat-form";
import { HumanMessage } from "@langchain/core/messages";
import { create_new_thread_id, query_agent } from "../chat/route";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LandingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleQueryFromLanding = async (query: string) => {
    if (!query.trim()) return;
    setLoading(true);

    try {
      const thread_id = await create_new_thread_id();
      if (!thread_id) throw new Error("Failed to create thread");

      // query agent
      await query_agent(thread_id, query);

      // redirect to chat page
      router.push(`/chat/${thread_id}`);
    } catch (error) {
      console.error("Agent query failed: ", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <>
      <header className="top-0 sticky">
        <TopSection />
      </header>
      <div className=" flex flex-1 flex-col overflow-hidden  justify-center items-center mb-35">
        <div className="p-5">
          <h1 className="text-4xl font-bold">XpAgent</h1>
          <p className="text-xl">Exploration Agent by Afiq</p>
        </div>
        <div className="w-1/2">
          <ChatForm submitHandler={handleQueryFromLanding} />
        </div>
      </div>
    </>
  );
}
