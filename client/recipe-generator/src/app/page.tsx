// import Image from "next/image";

"use client";

import { useState } from "react";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { text: "Welcome to the Recipe Recommender System! List ingredients to get recipe suggestions Remember to put a comma (,) in between each ingredient listed", sender: "bot" }
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: "user" }]);
      // Add code to call your recipe recommendation API here
      setInput("");
    }
  };

  return (
    <div className="flex flex-col max-w-2xl mx-auto p-8 rounded-lg shadow-lg bg-white dark:bg-gray-800 mt-10">
      <div> Recipe Recommender System </div>
      <div className="flex flex-col space-y-3 overflow-y-auto h-96 p-3">
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
          Send
        </button>
      </div>
    </div>
  );
}