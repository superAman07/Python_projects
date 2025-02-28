'use client'
import WebSocketStream from "@/components/websocketStream";

export default function LivePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
      <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300 mb-6">
        Live Video Stream
      </h1>

      <div className="relative w-full max-w-4xl p-6 rounded-xl bg-gray-800/50 backdrop-blur-md shadow-lg border border-gray-700">
        <WebSocketStream /> 
      </div>

      <p className="mt-6 text-gray-400 text-sm">
        Powered by WebSockets & OpenCV | <span className="text-blue-400">Next.js</span>
      </p>
    </div>
  );
}
