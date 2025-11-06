import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { AppSidebar } from "./_components/app-sidebar";

import { create_new_thread_id } from "./chat/route";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "XpAgent Chat",
  description: "Exploration Agent by Afiq",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // this implementation is temporary only
  const onNewChat = () => {
    // use api to create new thread
    const threadID = create_new_thread_id();
    // log the new thread
    console.log(threadID);
  };

  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`h-full overflow-hidden ${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          <SidebarProvider>
            <AppSidebar />
            <SidebarInset>{children}</SidebarInset>
            {/* {children} */}
            {/* <div className="h-screen w-screen">
              <AppSidebar />
              <main className="border border-red-500">{children}</main>
            </div> */}
          </SidebarProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
