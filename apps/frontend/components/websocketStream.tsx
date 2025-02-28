import React from "react";
import { useWebSocket } from "../hooks/useWebSocket";

const WebSocketStream: React.FC = () => {
  const frame = useWebSocket();

  return (
    <div className="flex flex-col items-center justify-center">
      <h2 className="text-lg font-semibold">Live Video Stream</h2>
      {frame ? (
        <img
          src={frame}
          alt="Live Stream"
          className="w-full max-w-2xl rounded-lg shadow-lg"
        />
      ) : (
        <p>Waiting for video stream...</p>
      )}
    </div>
  );
};

export default WebSocketStream;
