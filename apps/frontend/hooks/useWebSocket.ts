import { useState, useEffect } from "react";
import { io } from "socket.io-client";

const SERVER_URL = "ws://127.0.0.1:5000"; // Ya phir "ws://192.168.1.34:5000"

export const useWebSocket = () => {
  const [frame, setFrame] = useState<string | null>(null);

  useEffect(() => {
    const socket = io(SERVER_URL);

    socket.on("connect", () => {
      console.log("Connected to WebSocket Server ✅");
    });

    socket.on("video_frame", (data) => {
      setFrame(`data:image/jpeg;base64,${data.frame}`);
    });

    socket.on("disconnect", () => {
      console.log("Disconnected ❌");
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return frame;
};
