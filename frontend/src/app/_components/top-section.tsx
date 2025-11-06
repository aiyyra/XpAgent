"use client";

import { motion } from "motion/react";
import LogoButton from "./logo-button";
import { ModeToggle } from "./theme-toggle-button";
import { SidebarTrigger } from "@/components/ui/sidebar";

export default function TopSection() {
  return (
    <div className=" relative w-full z-10 flex items-center justify-between gap-3 p-5 bg-background">
      <div className="relative flex items-center justify-start gap-2">
        <div className="absolute left-0 z-10">
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
        <motion.button
          className="flex cursor-pointer items-center gap-2 pl-3"
          //   onClick={() => setThreadId(null)}
          onClick={undefined} // set later
          animate={
            {
              // marginLeft: !chatHistoryOpen ? 48 : 0,
            }
          }
          transition={{
            type: "spring",
            stiffness: 300,
            damping: 30,
          }}
        >
          {/* <SidebarTrigger /> */}
          <LogoButton />
        </motion.button>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center">
          {/* <OpenGitHubRepo /> */} <ModeToggle />
        </div>
        {/* Add button here to create new thread and start new chat */}
        {/* <TooltipIconButton
                  size="lg"
                  className="p-4"
                  tooltip="New thread"
                  variant="ghost"
                  onClick={() => setThreadId(null)}
                >
                  <SquarePen className="size-5" />
                </TooltipIconButton> */}
      </div>

      <div className="from-background to-background/0 absolute inset-x-0 top-full h-2 bg-linear-to-b" />
    </div>
  );
}
