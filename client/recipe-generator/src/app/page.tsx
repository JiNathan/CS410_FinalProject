"use client";

import React, { useState } from "react";
import getResponse from "./api/route";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { text: "Hi! Start searching for recipes below!", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (loading) {
      return;
    }
    if (input.trim()) {
      setLoading(true);
      setMessages((prevMessages) => [...prevMessages, { text: input, sender: "user" }]);
      setMessages((prevMessages) => [...prevMessages, { text: 'Generating recipes...', sender: "bot" }]);
      const query = input;
      setInput("");
      const response = await getResponse(query);
      console.log('Response:', response);
      setMessages((prevMessages) => [...prevMessages.slice(0, -1)]);
      const lines = response.split("\n\n\n")
      lines.map((line: string, index: number) => {
        setMessages((prevMessages) => [...prevMessages, { text: line, sender: "bot" }]);
      });
      setLoading(false);
    }
  };

  const formatText1 = (text: string): JSX.Element[] => {
    const lines = text.split("\n");
    return lines.map((line, index) => (
      <React.Fragment key={index}>
        {line}
        {index < lines.length-1 && <br />}
      </React.Fragment>
    ));
  };
  
  const formatText2 = (text: string): JSX.Element[] => {
    const lines = text.split("\n\n");
    return lines.map((line, index) => (
      <React.Fragment key={index}>
        {formatText1(line)}
        {index < lines.length-1 && <br />}
        {index < lines.length-1 && <br />}
      </React.Fragment>
    ));
  };


  return (
    <div className="bg-gray-200 min-h-screen flex items-end justify-center px-[12vw] pb-10 pt">
      {/* Label at the Top */}
      <div className="absolute top-5 w-full text-center py-4 font-bold text-6xl text-gray-700 font-serif">
        Recipe Recommender System
      </div>

      {/* Chatbox Container */}
      <div className="h-[80vh] flex flex-col-reverse justify-start w-full mx-auto p-10 rounded-lg shadow-lg bg-gray-400 border-4 border-gray-400 text-lg">        
        {/* Input and Send button */}
        <div className="flex items-center border-t border-gray-200 pt-3 mt-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type here..."
            className="flex-grow p-2 rounded-lg border bg-gray border-gray focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          />
          <button
            onClick={handleSend}
            className="inline-flex items-center justify-center rounded-md text-sm font-medium h-10 px-4 py-2 ml-3 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Send
          </button>
        </div>

        {/* Messages container */}
        <div className="flex flex-col space-y-3 overflow-y-auto p-5">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`${
                msg.sender === "user" ? "bg-blue-500 text-white self-end" : "bg-gray-200 text-gray-900 self-start"
              } p-3 rounded-lg max-w-[50vw]`}
            >
              {formatText2(msg.text)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}