// import Image from "next/image";

"use client";

import { useState } from "react";
import getResponse from "./api/route";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { text: "Hello user! List ingredients to get recipe suggestions! Remember to put a comma (,) in between each ingredient listed", sender: "bot" }
  ]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: "user" }]);
      const response = await getResponse(input);
      console.log('Response:', response);
      setMessages((prevMessages) => [...prevMessages, { text: response, sender: "bot" }]);
      setInput("");
    }
  };

  return (
    <div className="bg-gray-200 min-h-screen flex items-center justify-center p-5">
      {/* Label at the Top */}
      <div className="absolute top-0 w-full text-center py-4 font-bold text-2xl bg-gray-500 text-gray-100 shadow-sm">
        Recipe Recommender System
      </div>

      {/* Chatbox Container */}
      <div className="flex flex-col max-w-3xl w-full mx-auto p-10 rounded-lg shadow-lg bg-gray-400 mt-20 border-4 border-gray-400">
        {/* Messages container */}
        <div className="flex flex-col space-y-3 overflow-y-auto h-[35rem] p-5">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`${
                msg.sender === "user" ? "bg-blue-500 text-white self-end" : "bg-gray-300 text-gray-900 self-start"
              } p-3 rounded-lg max-w-xs`}
            >
              {msg.text}
            </div>
          ))}
        </div>
        
        {/* Input and Send button */}
        <div className="flex items-center border-t border-gray-300 pt-3 mt-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type ingredients here..."
            className="flex-grow p-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          />
          <button
            onClick={handleSend}
            className="ml-3 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            {'->'}
          </button>
        </div>
      </div>
    </div>
  );
}