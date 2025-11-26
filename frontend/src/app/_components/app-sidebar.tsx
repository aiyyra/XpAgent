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

import { get_thread_list } from "../chat/route";

interface SideBarProps {
  // threads:
  // activeThreadId: string | null;
  // onThreadSelect: (threadId: string) => void;
  // onNewChat: () => void;
}

interface Thread {
  topic: string;
  id: string;
  created_at: string;
  expires_at: string;
}

// Currently we make a very static approach that load the sidebar and require reload
const threads: Thread[] = await get_thread_list();

export function AppSidebar({}: // threads: Thread[],
// activeThreadId,
// onThreadSelect,
SideBarProps) {
  const router = useRouter();

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="border-b border-border p-4 ">
        <SidebarTrigger />
        {/* add other part of sidebar header later */}
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>General</SidebarGroupLabel>
          <SidebarGroupContent>
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
                          {thread.topic == "" ? thread.id : thread.topic}
                        </span>
                      </div>
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
