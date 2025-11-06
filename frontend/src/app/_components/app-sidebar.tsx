"use client";

import { Button } from "@/components/ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { MessageSquare, MessageSquarePlus } from "lucide-react";
// import { NewChatButton } from "./new-chat-button";
import { useRouter } from "next/navigation";

interface SideBarProps {
  // threads: Thread[];
  // activeThreadId: string | null;
  // onThreadSelect: (threadId: string) => void;
  // onNewChat: () => void;
}

// mock Thread
const threads = [
  {
    id: "bfa242be-aa77-49a5-88fa-ddb9228318fc",
    title: "Chat on memancing",
    lastMessage: "Hello, how are you?",
    timestamp: "10:00 AM",
  },
  {
    id: "2",
    title: "Random 2",
    lastMessage: "Hello, how are you?",
    timestamp: "10:00 AM",
  },
  {
    id: "3",
    title: "Random 3",
    lastMessage: "Hello, how are you?",
    timestamp: "10:00 AM",
  },
  {
    id: "4",
    title: "Random 4",
    lastMessage: "Hello, how are you?",
    timestamp: "10:00 AM",
  },
];

export function AppSidebar({}: // threads,
// activeThreadId,
// onThreadSelect,
SideBarProps) {
  const router = useRouter();

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="border-b border-border p-4 ">
        <SidebarTrigger />
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            {/* <NewChatButton onClick={onNewChat} /> */}
            <Button
              onClick={() => router.push("/")}
              className="w-full justify-start gap-2 bg-transparent text-primary hover:bg-sidebar-accent"
            >
              <MessageSquarePlus className="h-4 w-4" />
              New Chat
            </Button>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Threads</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {threads.map((thread) => (
                <SidebarMenuItem key={thread.id}>
                  <SidebarMenuButton
                    asChild
                    onClick={() => router.push(`/chat/${thread.id}`)}
                    // isActive
                    className="flex flex-col items-start gap-1 py-3"
                  >
                    {/* redirect to a new url with thread id as params, use the thread id to render the chat accordingly */}
                    <div className="pb-8">
                      <div className="flex w-full items-center gap-2">
                        <MessageSquare className="h-4 w-4 shrink-0" />
                        <span className="flex-1 truncate font-medium">
                          {thread.title}
                        </span>
                      </div>
                      {/* <div className="flex w-full items-center justify-between gap-2 pl-6">
                        <span className="text-muted-foreground truncate text-xs">
                          {thread.lastMessage}
                        </span>
                        <span className="text-muted-foreground shrink-0 text-xs">
                          {formatTimestamp(thread.timestamp)}
                          {thread.timestamp}
                        </span>
                      </div> */}
                    </div>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
