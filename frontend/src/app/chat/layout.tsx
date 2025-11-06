import { SidebarInset } from "@/components/ui/sidebar";

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <SidebarInset>{children}</SidebarInset>;
}
