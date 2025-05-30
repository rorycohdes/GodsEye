"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import type { UploadedFile } from "@/components/file-upload-modal";
import {
  FileText,
  ImageIcon,
  FileVideo,
  FileAudio,
  File,
  Download,
} from "lucide-react";

interface FilePreviewProps {
  file: UploadedFile | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function FilePreview({ file, open, onOpenChange }: FilePreviewProps) {
  const [content, setContent] = useState<string | null>(null);

  useEffect(() => {
    if (!file) return;

    // For text files, try to load the content
    if (file.type === "text" || file.type === "pdf") {
      fetch(file.url)
        .then((response) => {
          if (file.type === "text") {
            return response.text();
          }
          return "PDF preview not available in this demo. In a real application, a PDF viewer component would be integrated here.";
        })
        .then((text) => setContent(text))
        .catch((error) => setContent("Error loading file content."));
    } else {
      setContent(null);
    }
  }, [file]);

  if (!file) return null;

  const renderPreview = () => {
    switch (file.type) {
      case "image":
        return (
          <div className="flex items-center justify-center p-4 bg-[#1a1a1a] rounded-lg">
            <ImageIcon
              src={file.url || "/placeholder.svg"}
              alt={file.name}
              className="max-w-full max-h-[60vh] object-contain"
            />
          </div>
        );
      case "video":
        return (
          <div className="p-4 bg-[#1a1a1a] rounded-lg">
            <video src={file.url} controls className="max-w-full max-h-[60vh]">
              Your browser does not support the video tag.
            </video>
          </div>
        );
      case "audio":
        return (
          <div className="p-4 bg-[#1a1a1a] rounded-lg">
            <audio src={file.url} controls className="w-full">
              Your browser does not support the audio tag.
            </audio>
          </div>
        );
      case "text":
        return (
          <div className="p-4 bg-[#1a1a1a] rounded-lg overflow-auto max-h-[60vh]">
            <pre className="text-sm whitespace-pre-wrap font-mono text-gray-300">
              {content || "Loading content..."}
            </pre>
          </div>
        );
      case "pdf":
        return (
          <div className="p-4 bg-[#1a1a1a] rounded-lg text-center">
            <div className="w-16 h-16 mx-auto mb-4">
              <FileText className="w-full h-full text-red-500" />
            </div>
            <p className="text-gray-300 mb-4">
              {content || "PDF preview not available in this demo."}
            </p>
            <Button
              variant="outline"
              className="bg-[#2a2a2a] border-gray-700 hover:bg-[#333333] gap-2"
              onClick={() => window.open(file.url, "_blank")}
            >
              <Download className="h-4 w-4" />
              Download PDF
            </Button>
          </div>
        );
      default:
        return (
          <div className="p-4 bg-[#1a1a1a] rounded-lg text-center">
            <div className="w-16 h-16 mx-auto mb-4">
              <File className="w-full h-full text-gray-500" />
            </div>
            <p className="text-gray-300">
              Preview not available for this file type.
            </p>
          </div>
        );
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-3xl bg-[#2a2a2a] border-gray-700 text-white">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            {file.type === "pdf" && (
              <FileText className="h-5 w-5 text-red-500" />
            )}
            {file.type === "image" && (
              <ImageIcon className="h-5 w-5 text-blue-500" />
            )}
            {file.type === "video" && (
              <FileVideo className="h-5 w-5 text-purple-500" />
            )}
            {file.type === "audio" && (
              <FileAudio className="h-5 w-5 text-green-500" />
            )}
            {(file.type === "text" || file.type === "other") && (
              <File className="h-5 w-5 text-gray-500" />
            )}
            {file.name}
          </DialogTitle>
        </DialogHeader>

        {renderPreview()}
      </DialogContent>
    </Dialog>
  );
}
