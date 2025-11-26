import { IconCheck, IconPlus } from "@tabler/icons-react";
import { ArrowUpIcon } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
  InputGroupText,
  InputGroupTextarea,
} from "@/components/ui/input-group";

export function ChatForm({
  submitHandler,
}: {
  submitHandler: (query: string) => void;
}) {
  return (
    <>
      <form
        onSubmit={(e) => {
          if (!e.currentTarget.query.value.trim()) return;
          e.preventDefault();
          submitHandler(e.currentTarget.query.value.trim());
          e.currentTarget.query.value = "";
        }}
        className="w-full"
      >
        <InputGroup>
          <InputGroupTextarea
            placeholder="Ask, Search or Chat..."
            name="query"
            onKeyDown={(e) => {
              const query = e.currentTarget.value.trim();
              if (!query) return;
              // else if (e.key === "Enter" && e.shiftKey) {
              //   e.preventDefault();
              //   // find a way to go to next line (simply append \n to the value???)
              //   return;
              // }
              else if (e.key === "Enter") {
                e.preventDefault();
                submitHandler(query);
                e.currentTarget.value = "";
              }
            }}
          />
          <InputGroupAddon align="block-end">
            <InputGroupButton
              variant="default"
              className="rounded-full ml-auto"
              size="icon-xs"
              type="submit"
            >
              <ArrowUpIcon />
              <span className="sr-only">Send</span>
            </InputGroupButton>
          </InputGroupAddon>
        </InputGroup>
      </form>
    </>
  );
}
