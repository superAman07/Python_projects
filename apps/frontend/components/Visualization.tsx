import { useState, useEffect } from "react";
import Image from "next/image";
import useWebSocket from "../hooks/useWebSocket";

interface WebSocketData {
  movement_speed: number;
  stampede_probability: number;
  people_count: number;
}

export default function Visualization() {
  const data: WebSocketData | null = useWebSocket("ws://localhost:8000/ws"); // WebSocket API URL
  const [alert, setAlert] = useState<string | null>(null);

  useEffect(() => {
    if (data?.stampede_probability > 70) {
      setAlert("🚨 High Risk Detected!");
    } else {
      setAlert(null);
    }
  }, [data]);

  return (
    <div>
      <div className="p-4">
        <h1 className="text-2xl font-bold">Crowd Monitoring</h1>
        <Image src="http://localhost:8000/video_feed" alt="Live Feed" layout="responsive" width={700} height={475} className="w-full rounded-lg" />
        {alert && (
          <div className="absolute top-4 left-4 bg-red-500 text-white px-4 py-2 rounded">
            {alert}
          </div>
        )}
      </div>
      <div className="mt-4">
        <p>People Count: {data?.people_count}</p>
        <p>Movement Speed: {data?.movement_speed}</p>
        <p>Risk: {data?.stampede_probability}%</p>
      </div>
    </div>
  );
}