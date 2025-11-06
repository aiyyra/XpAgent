import TopSection from "@/app/_components/top-section";
import { ChatInterface } from "@/components/message-component";

export default async function ChatPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  return (
    <>
      <header className="top-0 sticky">
        <TopSection />
      </header>
      <div className=" flex flex-1 flex-col overflow-hidden justify-center items-center p-4  w-full">
        <ChatInterface thread_id={slug as string} />
      </div>
    </>
  );
}
