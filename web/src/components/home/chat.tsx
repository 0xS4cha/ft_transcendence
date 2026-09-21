import { Card, CardHeader, CardContent } from "@/components/ui/card";
import {
  Bubble,
  BubbleContent,
  BubbleGroup,
  BubbleReactions,
} from "@/components/ui/bubble";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupText,
  InputGroupTextarea,
} from "@/components/ui/input-group";
import { useEffect, useState } from "react";
import { toast } from "@/components/ui/toast";
import { type ChatDataProps } from "@/types/chat";
import { getChatHistory } from "@/services/chatService";

export function BubbleGroupDemo() {
  return (
    <div className="flex w-full  flex-col gap-8 py-12 ml-auto">
      <Bubble variant="muted">
        <BubbleContent>Can you tell me what&apos;s the issue?</BubbleContent>
      </Bubble>
      <BubbleGroup>
        <Bubble align="end">
          <BubbleContent>You tell me!</BubbleContent>
        </Bubble>
        <Bubble align="end">
          <BubbleContent>It worked yesterday. You broke it!</BubbleContent>
        </Bubble>
        <Bubble align="end">
          <BubbleContent>Find the bug and fix it.</BubbleContent>
          <BubbleReactions aria-label="Reactions: eyes" align="start">
            <span>👀</span>
          </BubbleReactions>
        </Bubble>
      </BubbleGroup>
      <Bubble variant="muted">
        <BubbleContent>
          Want me to diff yesterday&apos;s you against today&apos;s you?
          It&apos;s a bit embarrassing.
        </BubbleContent>
      </Bubble>
    </div>
  )
}


export function Chat() {
    const [chatHistory, setChatHistory] = useState<ChatDataProps[]>([]);
    const [message, setMessage] = useState<String>("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await getChatHistory();
                setChatHistory(result);
            } catch (error) {
                toast.add({
                type: "error",
                title: `Fetch failed: ${error}`,
                });
            }
        };

        fetchData();
    }, []);

    function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
        const value = event.target.value;
        setMessage(value);
    }

    return (
        <Card>
            <CardHeader>
                Global chat
            </CardHeader>
            <CardContent>
                <BubbleGroupDemo />
                <InputGroup>
                    <InputGroupTextarea
                        id="block-end-textarea"
                        placeholder="Write a message..."
                        onChange={handleChange}
                    />
                    <InputGroupAddon align="block-end">
                        <InputGroupButton variant="default" size="sm" className="ml-auto">
                        Post
                        </InputGroupButton>
                    </InputGroupAddon>
                </InputGroup>
            </CardContent>
        </Card>
    )
}