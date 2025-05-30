"use client";

import { useState } from "react";
import Link from "next/link";
import { Plus, Grid3X3, List, ChevronDown, MoreVertical } from "lucide-react";

export default function NotebooksView() {
  const [viewMode, setViewMode] = useState("grid");
  const minCards = 12; // Minimum number of cards to display

  // Sample notebook data
  const notebooks = [
    {
      id: 1,
      title: "Untitled notebook",
      date: "May 18, 2025",
      sources: 0,
      icon: "📔",
    },
    {
      id: 2,
      title: "Apples and Oranges",
      date: "May 2, 2025",
      sources: 1,
      icon: "🍎",
    },
    {
      id: 3,
      title: "Einstein and Relativity: Abridged",
      date: "Mar 20, 2025",
      sources: 1,
      icon: "💡",
    },
    {
      id: 4,
      title: "Clausius, Entropy, and the Second Law of Thermodynamics",
      date: "Mar 10, 2025",
      sources: 2,
      icon: "🔥",
    },
    {
      id: 5,
      title: "Five Equations That Changed the World",
      date: "Feb 19, 2025",
      sources: 1,
      icon: "💡",
    },
    {
      id: 6,
      title: "Between a Rock and a Hard Life: Daniel's Story",
      date: "Feb 6, 2025",
      sources: 1,
      icon: "✈️",
    },
    {
      id: 7,
      title: "Five Equations That Changed the World",
      date: "Feb 19, 2025",
      sources: 2,
      icon: "💡",
    },
    {
      id: 8,
      title: "inGenius: A Crash Course on Creativity",
      date: "Feb 20, 2025",
      sources: 1,
      icon: "💡",
    },
  ];

  // Calculate skeleton cards needed
  const skeletonCount = Math.max(0, minCards - notebooks.length);

  const SkeletonCard = () => (
    <div className="h-32 bg-[#2a2a2a] rounded-lg p-4 animate-pulse">
      <div className="flex items-start gap-3 h-full">
        <div className="w-8 h-8 bg-[#3a3a3a] rounded-md flex-shrink-0"></div>
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-[#3a3a3a] rounded w-3/4"></div>
          <div className="h-3 bg-[#3a3a3a] rounded w-1/2"></div>
        </div>
        <div className="w-6 h-6 bg-[#3a3a3a] rounded flex-shrink-0"></div>
      </div>
    </div>
  );

  const NotebookCard = ({ notebook }: { notebook: (typeof notebooks)[0] }) => (
    <Link href={`/notebooks/${notebook.id}`} className="block">
      <div className="h-32 bg-[#2a2a2a] rounded-lg p-4 hover:bg-[#333333] transition-colors cursor-pointer">
        <div className="flex items-start gap-3 h-full">
          <div className="text-2xl flex-shrink-0">{notebook.icon}</div>
          <div className="flex-1 min-w-0">
            <h3
              className="font-medium text-sm leading-tight mb-2 truncate text-white"
              title={notebook.title}
            >
              {notebook.title}
            </h3>
            <p className="text-xs text-[#b9bbbe] truncate">
              {notebook.date} • {notebook.sources}{" "}
              {notebook.sources === 1 ? "source" : "sources"}
            </p>
          </div>
          <button
            className="h-6 w-6 p-0 flex-shrink-0 bg-transparent border-none text-[#b9bbbe] hover:text-white hover:bg-[#3a3a3a] rounded cursor-pointer flex items-center justify-center"
            onClick={(e) => e.preventDefault()}
          >
            <MoreVertical className="h-4 w-4" />
          </button>
        </div>
      </div>
    </Link>
  );

  return (
    <div className="min-h-screen bg-[#1e1e1e] text-[#e0e0e0] p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">
            Welcome to NotebookLM
          </h1>
        </div>

        <div className="flex items-center justify-between mb-6">
          <button className="flex items-center gap-2 bg-white text-[#1e1e1e] px-4 py-2 rounded-full font-medium hover:bg-gray-100 transition-colors">
            <Plus className="h-4 w-4" />
            Create new
          </button>

          <div className="flex items-center gap-2">
            <div className="flex border border-[#3a3a3a] rounded-md">
              <button
                className={`px-3 py-2 rounded-l-md transition-colors ${
                  viewMode === "list"
                    ? "bg-[#3a3a3a] text-white"
                    : "bg-transparent text-[#b9bbbe] hover:text-white hover:bg-[#2a2a2a]"
                }`}
                onClick={() => setViewMode("list")}
              >
                <List className="h-4 w-4" />
              </button>
              <button
                className={`px-3 py-2 rounded-r-md transition-colors ${
                  viewMode === "grid"
                    ? "bg-[#3a3a3a] text-white"
                    : "bg-transparent text-[#b9bbbe] hover:text-white hover:bg-[#2a2a2a]"
                }`}
                onClick={() => setViewMode("grid")}
              >
                <Grid3X3 className="h-4 w-4" />
              </button>
            </div>

            <div className="relative">
              <button className="flex items-center gap-2 bg-[#2a2a2a] text-[#e0e0e0] px-4 py-2 rounded-md border border-[#3a3a3a] hover:bg-[#333333] transition-colors">
                Most recent
                <ChevronDown className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        <div
          className={
            viewMode === "grid"
              ? "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
              : "space-y-2"
          }
        >
          {notebooks.map((notebook) => (
            <NotebookCard key={notebook.id} notebook={notebook} />
          ))}

          {viewMode === "grid" &&
            Array.from({ length: skeletonCount }, (_, index) => (
              <SkeletonCard key={`skeleton-${index}`} />
            ))}
        </div>
      </div>
    </div>
  );
}
