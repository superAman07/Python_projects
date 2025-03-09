import React from "react";
import { useWebSocket } from "../hooks/useWebSocket";

const WebSocketStream: React.FC = () => {
  const { frame, logs } = useWebSocket();

  return (
    <div className="grid grid-cols-3 gap-6 min-h-screen p-6 bg-gray-950 text-white">
      {/* Left: Video Stream */}
      <div className="col-span-2 flex flex-col items-center justify-center p-6 bg-gray-900 rounded-xl shadow-xl">
        <h2 className="text-xl font-bold mb-4 text-blue-400">Live Video Stream</h2>
        {frame ? (
          <img
            src={frame}
            alt="Live Stream"
            className="w-full max-w-4xl rounded-lg shadow-lg border-2 border-blue-500"
          />
        ) : (
          <p className="text-gray-400">Waiting for video stream...</p>
        )}
      </div>

      {/* Right: Logs */}
      <div className="flex flex-col bg-gray-800 p-4 rounded-xl shadow-lg border border-gray-700 overflow-hidden">
        <h3 className="text-lg font-semibold text-green-400 mb-2">Logs</h3>
        <div className="overflow-y-auto h-[75vh] p-2 space-y-2 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-900">
          {logs.map((log, index) => (
            <p
              key={index}
              className="p-2 rounded-md bg-gray-900 text-xs text-green-300 border border-gray-700 shadow-sm"
            >
              {log}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WebSocketStream;




// import React from "react";
// import { useWebSocket } from "../hooks/useWebSocket";

// const WebSocketStream: React.FC = () => {
//   const { frame, logs } = useWebSocket();


//   return (
//     <div className="flex flex-col items-center justify-center">
//       <div>
//         <h2 className="text-lg font-semibold">Live Video Stream</h2>
//         {frame ? (
//           <img
//             src={frame}
//             alt="Live Stream"
//             className="w-full max-w-2xl rounded-lg shadow-lg"
//           />
//         ) : (
//           <p>Waiting for video stream...</p>
//         )}
//       </div>
//       <div className="w-1/4 ml-4 p-2 bg-gray-900 text-white text-xs h-64 overflow-y-auto rounded-lg shadow-lg">
//         <h3 className="font-semibold mb-2">Logs</h3>
//         <div className="space-y-1">
//           {logs.map((log, index) => (
//             <p key={index} className="break-words">
//               {log}
//             </p>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default WebSocketStream;
