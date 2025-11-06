"use client"; // use client temporarily for testing

import LogoButton from "@/app/_components/logo-button";
import { ModeToggle } from "@/app/_components/theme-toggle-button";
import { Button } from "../ui/button";
import { useMediaQuery } from "@/hooks/use-media-query";
import * as motion from "motion/react-client";
import { cn } from "@/lib/utils";
import { StickToBottom, useStickToBottomContext } from "use-stick-to-bottom";
import TopSection from "@/app/_components/top-section";
import { ChatForm } from "@/app/_components/chat-form";

// const isLargeScreen = useMediaQuery("(min-width: 1024px)");
// const chatStarted = !!threadId || !!messages.length;
const chatStarted = true; // hard code for testing, target implementation is as above

export function Thread() {
  return (
    <div className="flex h-screen w-full overflow-hidden">
      <div className="relative hidden lg:flex">
        <motion.div
          className="absolute z-20 h-full overflow-hidden border-r bg-white"
          style={{ width: 300 }}
          animate={
            undefined // change the condition later
            // isLargeScreen
            //   ? { x: chatHistoryOpen ? 0 : -300 }
            //   : { x: chatHistoryOpen ? 0 : -300 }
          }
          initial={{ x: -300 }}
          transition={
            undefined // will implement later
            // isLargeScreen
            //   ? { type: "spring", stiffness: 300, damping: 30 }
            //   : { duration: 0 }
          }
        >
          {/* Show Thread history list here, Thread list will act like a sidebar*/}
          <div className="relative h-full" style={{ width: 300 }}>
            {/* <ThreadList/> */}
          </div>
        </motion.div>
      </div>
      <div
        className={cn(
          "grid w-full grid-cols-[1fr_0fr] transition-all duration-500"
          //   artifactOpen && "grid-cols-[3fr_2fr]"   -- update with artifact later
        )}
      >
        <motion.div
          className={cn(
            "relative flex min-w-0 flex-1 flex-col overflow-hidden"
            // !chatStarted && "grid-rows-[1fr]" -- update with chatStarted later,
          )}
          //    layout={isLargeScreen}
          animate={
            {
              // marginLeft: chatHistoryOpen ? (isLargeScreen ? 300 : 0) : 0,
              // width: chatHistoryOpen
              //   ? isLargeScreen
              //     ? "calc(100% - 300px)"
              //     : "100%"
              //   : "100%",
            }
          }
          transition={
            undefined // will implement later
            // isLargeScreen
            //   ? { type: "spring", stiffness: 300, damping: 30 }
            //   : { duration: 0 }
          }
        >
          {!chatStarted && (
            <div className="absolute top-0 left-0 z-10 flex w-full items-center justify-between gap-3 p-2 pl-4">
              <div>
                {/* implement the button to show and hide the sidebar(ChatHistory) */}
                {/* {(!chatHistoryOpen || !isLargeScreen) && (
                  <Button
                    className="hover:bg-gray-100"
                    variant="ghost"
                    onClick={() => setChatHistoryOpen((p) => !p)}
                  >
                    {chatHistoryOpen ? (
                      <PanelRightOpen className="size-5" />
                    ) : (
                      <PanelRightClose className="size-5" />
                    )}
                  </Button>
                )} */}
              </div>
              <div className="absolute top-2 right-4 flex items-center">
                {/* <OpenGitHubRepo /> */}
                <ModeToggle />
              </div>
            </div>
          )}

          {chatStarted && <TopSection />}

          {/* Sticky to bottom is chat rendering library specialise for ai chat realtime render */}
          <StickToBottom className="relative flex-1 overflow-hidden">
            <div>Chat</div>
            {/* Here we will use useStickToBottomContext to render the chat */}
            {/* <StickyToBottomContent/> -- create this class to pass the useStickToBottomContext and render the chat, create on this file is okay */}
            {/* We will pass everything about the chat UI including form to send chat here */}
          </StickToBottom>
        </motion.div>
      </div>
      <div className="relative flex items-center justify-start gap-2">
        <div className="absolute left-0 z-10">
          <Button>New Chat</Button>
          <LogoButton />
          <ModeToggle />
        </div>
        <ChatForm />
      </div>
    </div>
  );
}
