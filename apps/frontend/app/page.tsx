'use client'
import Image from "next/image";
import { useEffect, useRef } from "react";

export default function Home() {
  const videoRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/video");
    ws.binaryType = "arraybuffer";

    ws.onmessage = (event) => {
      const blob = new Blob([event.data], { type: "image/jpeg" });
      const url = URL.createObjectURL(blob);
      if (videoRef.current) {
        videoRef.current.src = url;
      }
    };

    return () => ws.close();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white"> 
      <h1 className="text-2xl mb-4">Live Video Feed</h1>
      <Image ref={videoRef} alt="Live feed" className="w-1/2 border rounded-lg" />
    </div>
  );
}