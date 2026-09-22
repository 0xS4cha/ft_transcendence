import { useEffect, useState, useCallback, useRef } from 'react';
import { useAppDispatch } from "@/store/hooks"
import { addChatContent } from "@/store/reducers/userSlice";

export function useWSConnection(url: string = 'ws://127.0.0.1:8080') {
  const [isConnected, setIsConnected] = useState(false);
  const [isActive, setIsActive] = useState(false);
  const dispatch = useAppDispatch();
  const reconnectAttempt = useRef(0);
  const reconnectTimeoutId = useRef<ReturnType<typeof setTimeout> | null>(null);

  const startConnection = useCallback(() => {
    setIsActive(true);
    reconnectAttempt.current = 0;
  }, []);

  const stopConnection = useCallback(() => {
    setIsActive(false);
    setIsConnected(false);
    if (reconnectTimeoutId.current) {
      clearTimeout(reconnectTimeoutId.current);
    }
  }, []);

  useEffect(() => {
    if (!isActive) return;

    let ws: WebSocket;

    const connect = () => {
      ws = new WebSocket(url);

      ws.onopen = () => {
        setIsConnected(true);
        reconnectAttempt.current = 0;
      };

    ws.onmessage = (event) => {
    try {
        const parsed = JSON.parse(event.data);
        dispatch(addChatContent(parsed.data));
    } catch (err) {
        console.error("WS message parsing failed:", err);
    }
    };

      ws.onerror = () => {
        ws.close();
      };

      ws.onclose = () => {
        setIsConnected(false);
        if (isActive) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempt.current), 30000);
          reconnectAttempt.current += 1;
          reconnectTimeoutId.current = setTimeout(connect, delay);
        }
      };
    };

    connect();



    return () => {
      if (reconnectTimeoutId.current) clearTimeout(reconnectTimeoutId.current);
      if (ws) {
        ws.onclose = null;
        ws.close();
      }
    };
  }, [isActive, url, dispatch]);

  return { isConnected, isActive, startConnection, stopConnection };
}