"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Upload,
  Search,
  Plus,
  Share,
  Settings,
  Bot,
  PenBox,
  Info,
  MoreVertical,
  Send,
  FileText,
  MessageSquare,
  Clock,
  ArrowLeft,
} from "lucide-react";
import { FileUploadModal } from "@/components/file-upload-modal";
import { SourceItem } from "@/components/source-item";
import Link from "next/link";

export default function NotebookDetailPage() {
  const params = useParams();
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [sources, setSources] = useState([]);
  const [notebook, setNotebook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditingTitle, setIsEditingTitle] = useState(false);

  // Sample notebook data - in a real app, this would come from an API
  const notebooks = [
    {
      id: "1",
      title: "Untitled notebook",
      date: "May 18, 2025",
      sources: 0,
      icon: "📔",
      content:
        "This is your untitled notebook. Start writing your thoughts and ideas here.",
    },
    {
      id: "2",
      title: "Apples and Oranges",
      date: "May 2, 2025",
      sources: 1,
      icon: "🍎",
      content:
        "A comprehensive comparison between apples and oranges, exploring their nutritional values, origins, and cultural significance.",
    },
    {
      id: "3",
      title: "Einstein and Relativity: Abridged",
      date: "Mar 20, 2025",
      sources: 1,
      icon: "💡",
      content:
        "An exploration of Einstein's theory of relativity, breaking down complex concepts into digestible explanations.",
    },
    {
      id: "4",
      title: "Clausius, Entropy, and the Second Law of Thermodynamics",
      date: "Mar 10, 2025",
      sources: 2,
      icon: "🔥",
      content:
        "Diving deep into thermodynamics, exploring Clausius's contributions and the fundamental concept of entropy.",
    },
    {
      id: "5",
      title: "Five Equations That Changed the World",
      date: "Feb 19, 2025",
      sources: 1,
      icon: "💡",
      content:
        "An analysis of the most influential mathematical equations in human history and their impact on science.",
    },
    {
      id: "6",
      title: "Between a Rock and a Hard Life: Daniel's Story",
      date: "Feb 6, 2025",
      sources: 1,
      icon: "✈️",
      content:
        "A personal narrative exploring challenges, resilience, and personal growth through difficult circumstances.",
    },
    {
      id: "7",
      title: "Five Equations That Changed the World",
      date: "Feb 19, 2025",
      sources: 2,
      icon: "💡",
      content:
        "A deeper dive into mathematical equations that revolutionized our understanding of the universe.",
    },
    {
      id: "8",
      title: "inGenius: A Crash Course on Creativity",
      date: "Feb 20, 2025",
      sources: 1,
      icon: "💡",
      content:
        "Exploring the science and art of creativity, with practical techniques for enhancing innovative thinking.",
    },
  ];

  useEffect(() => {
    const foundNotebook = notebooks.find((nb) => nb.id === params.id);
    setNotebook(foundNotebook);
    setLoading(false);
  }, [params.id]);

  const handleFileUpload = (file) => {
    setSources((prev) => [...prev, file]);
  };

  const handleDeleteSource = (id) => {
    setSources((prev) => prev.filter((source) => source.id !== id));
  };

  const handleTitleEdit = () => {
    setIsEditingTitle(true);
  };

  const handleTitleSave = (newTitle) => {
    if (notebook) {
      const updatedTitle = newTitle.trim() || notebook.title;
      setNotebook({ ...notebook, title: updatedTitle });
    }
    setIsEditingTitle(false);
  };

  const handleTitleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleTitleSave(e.currentTarget.value);
    } else if (e.key === "Escape") {
      setIsEditingTitle(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#1e1e1e] text-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p>Loading notebook...</p>
        </div>
      </div>
    );
  }

  if (!notebook) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-[#1e1e1e] text-white gap-4">
        <h1 className="text-2xl font-bold">Notebook Not Found</h1>
        <p className="text-gray-400">
          The notebook you're looking for doesn't exist.
        </p>
        <Link
          href="/notebooks"
          className="flex items-center gap-2 text-blue-400 hover:text-blue-300"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Notebooks
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-[#1e1e1e] text-white">
      {/* Header */}
      <header className="flex items-center justify-between p-4 border-b border-gray-800">
        <div className="flex items-center gap-3">
          <Link
            href="/notebooks"
            className="flex items-center gap-2 text-gray-400 hover:text-white"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
            <span className="text-lg">{notebook.icon}</span>
          </div>
          <h1 className="text-lg font-medium">
            {isEditingTitle ? (
              <Input
                value={notebook.title}
                onChange={(e) =>
                  setNotebook({ ...notebook, title: e.target.value })
                }
                onKeyDown={handleTitleKeyDown}
                onBlur={() => handleTitleSave(notebook.title)}
                className="border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 text-lg font-medium p-0 h-auto"
                autoFocus
              />
            ) : (
              <span
                onClick={handleTitleEdit}
                className="cursor-pointer hover:text-gray-300"
              >
                {notebook.title}
              </span>
            )}
          </h1>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" className="text-gray-300 gap-2">
            <Share className="w-4 h-4" />
            Share
          </Button>
          <Button variant="ghost" size="sm" className="text-gray-300">
            <Settings className="w-4 h-4" />
            Settings
          </Button>
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-pink-500"></div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sources Panel */}
        <div className="w-[350px] border-r border-gray-800 flex flex-col">
          <div className="flex items-center justify-between p-4">
            <h2 className="font-medium">Sources</h2>
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <PenBox className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex gap-2 p-2 box-border w-full">
            <Button
              variant="outline"
              className="flex-1 flex items-center justify-center gap-2 bg-[#2a2a2a] border-gray-700 hover:bg-[#333333]"
              onClick={() => setUploadModalOpen(true)}
            >
              <Plus className="h-4 w-4" />
              Add
            </Button>
            <Button
              variant="outline"
              className="flex-1 flex items-center justify-center gap-2 bg-[#2a2a2a] border-gray-700 hover:bg-[#333333]"
            >
              <Search className="h-4 w-4" />
              Discover
            </Button>
          </div>
          {sources.length > 0 ? (
            <div className="flex-1 overflow-y-auto p-2">
              {sources.map((source) => (
                <SourceItem
                  key={source.id}
                  file={source}
                  onDelete={handleDeleteSource}
                />
              ))}
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
              <div className="w-16 h-16 mb-4 text-gray-500">
                <FileText className="w-full h-full" />
              </div>
              <p className="text-sm font-medium text-gray-300 mb-1">
                Saved sources will appear here
              </p>
              <p className="text-xs text-gray-500 max-w-[250px]">
                Click Add source above to add PDFs, websites, text, videos, or
                audio files. Or import a file directly from Google Drive.
              </p>
            </div>
          )}
        </div>

        {/* Chat Panel */}
        <div className="flex-1 flex flex-col border-r border-gray-800">
          <div className="flex items-center justify-between p-4">
            <h2 className="font-medium">Chat</h2>
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <PenBox className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
            {sources.length > 0 ? (
              <div className="text-center">
                <div className="w-10 h-10 rounded-full bg-[#2a2a2a] flex items-center justify-center mb-4 mx-auto">
                  <Bot className="w-5 h-5 text-blue-400" />
                </div>
                <h3 className="text-xl font-medium mb-2">Ready to chat</h3>
                <p className="text-sm text-gray-400 max-w-md">
                  You&apos;ve added {sources.length} source
                  {sources.length !== 1 ? "s" : ""}. Ask questions about your
                  content or start a conversation.
                </p>
              </div>
            ) : (
              <>
                <div className="w-10 h-10 rounded-full bg-[#2a2a2a] flex items-center justify-center mb-4">
                  <Upload className="w-5 h-5 text-blue-400" />
                </div>
                <h3 className="text-xl font-medium mb-4">
                  Add a source to get started
                </h3>
                <Button
                  className="bg-[#2a2a2a] hover:bg-[#333333] text-white border border-gray-700 rounded-full"
                  onClick={() => setUploadModalOpen(true)}
                >
                  Upload a source
                </Button>
              </>
            )}
          </div>
          <div className="p-2 border-t border-gray-800">
            <div className="flex items-center gap-2 bg-[#2a2a2a] rounded-lg p-2 pr-1">
              <Input
                placeholder={
                  sources.length > 0
                    ? "Ask a question..."
                    : "Upload a source to get started"
                }
                className="border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 text-sm"
                disabled={sources.length === 0}
              />
              <div className="text-xs text-gray-500">
                {sources.length} sources
              </div>
              <Button
                size="icon"
                className="h-8 w-8 rounded-full bg-blue-600 hover:bg-blue-700"
                disabled={sources.length === 0}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Studio Panel */}
        <div className="w-[350px] flex flex-col">
          <div className="flex items-center justify-between p-4">
            <h2 className="font-medium">Studio</h2>
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <PenBox className="h-4 w-4" />
            </Button>
          </div>

          <div className="p-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-medium">Audio Overview</h3>
              <Button variant="ghost" size="icon" className="h-6 w-6">
                <Info className="h-4 w-4" />
              </Button>
            </div>

            <div className="bg-[#2a2a2a] rounded-lg p-3 mb-6">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-5 h-5 rounded-full bg-blue-600 flex items-center justify-center">
                  <Bot className="w-3 h-3 text-white" />
                </div>
                <p className="text-xs text-blue-400">
                  Create an Audio Overview in more languages!{" "}
                  <span className="underline">Learn more</span>
                </p>
              </div>

              <div className="flex items-center gap-3 mt-4">
                <div className="w-12 h-12 rounded-full bg-[#3a3a3a] flex items-center justify-center">
                  <Bot className="w-6 h-6 text-gray-300" />
                </div>
                <div>
                  <p className="text-sm font-medium">Deep Dive conversation</p>
                  <p className="text-xs text-gray-400">Two hosts</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 mt-4">
                <Button
                  variant="outline"
                  className="bg-[#2a2a2a] border-gray-700 hover:bg-[#333333] text-sm"
                >
                  Customize
                </Button>
                <Button
                  className="bg-gray-200 text-black hover:bg-gray-300 text-sm"
                  disabled={sources.length === 0}
                >
                  Generate
                </Button>
              </div>
            </div>

            <div className="flex items-center justify-between mb-2">
              <h3 className="font-medium">Notes</h3>
              <Button variant="ghost" size="icon" className="h-6 w-6">
                <MoreVertical className="h-4 w-4" />
              </Button>
            </div>

            <Button
              variant="outline"
              className="w-full justify-center gap-2 bg-[#2a2a2a] border-gray-700 hover:bg-[#333333] mb-3"
            >
              <Plus className="h-4 w-4" />
              Add note
            </Button>

            <div className="grid grid-cols-2 gap-2 mb-3">
              <Button
                variant="ghost"
                className="justify-start gap-2 text-gray-400 hover:text-white text-xs"
              >
                <MessageSquare className="h-3 w-3" />
                Study guide
              </Button>
              <Button
                variant="ghost"
                className="justify-start gap-2 text-gray-400 hover:text-white text-xs"
              >
                <FileText className="h-3 w-3" />
                Briefing doc
              </Button>
              <Button
                variant="ghost"
                className="justify-start gap-2 text-gray-400 hover:text-white text-xs"
              >
                <MessageSquare className="h-3 w-3" />
                FAQ
              </Button>
              <Button
                variant="ghost"
                className="justify-start gap-2 text-gray-400 hover:text-white text-xs"
              >
                <Clock className="h-3 w-3" />
                Timeline
              </Button>
            </div>

            <div className="flex-1 flex flex-col items-center justify-center p-6 text-center mt-8">
              <div className="w-16 h-16 mb-4 text-gray-500">
                <FileText className="w-full h-full" />
              </div>
              <p className="text-sm font-medium text-gray-300 mb-1">
                Saved notes will appear here
              </p>
              <p className="text-xs text-gray-500 max-w-[250px]">
                Save a chat message to create a new note, or click Add note
                above.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="p-2 text-center border-t border-gray-800">
        <p className="text-xs text-gray-500">
          NotebookLM can be inaccurate; please double check its responses.
        </p>
      </footer>

      {/* File Upload Modal */}
      <FileUploadModal
        open={uploadModalOpen}
        onOpenChange={setUploadModalOpen}
        onFileUpload={handleFileUpload}
      />
    </div>
  );
}
