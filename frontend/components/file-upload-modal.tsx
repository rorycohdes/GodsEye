"use client";

import type React from "react";

import { useState, useRef } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  FileText,
  Upload,
  File,
  ImageIcon,
  FileVideo,
  FileAudio,
  Globe,
} from "lucide-react";
import { cn } from "@/lib/utils";

export type FileType =
  | "pdf"
  | "image"
  | "video"
  | "audio"
  | "text"
  | "website"
  | "other";

export interface UploadedFile {
  id: string;
  name: string;
  type: FileType;
  size: number;
  url: string;
  uploadedAt: Date;
}

interface FileUploadModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onFileUpload: (file: UploadedFile) => void;
}

export function FileUploadModal({
  open,
  onOpenChange,
  onFileUpload,
}: FileUploadModalProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const getFileType = (file: File): FileType => {
    if (file.type.includes("pdf")) return "pdf";
    if (file.type.includes("image")) return "image";
    if (file.type.includes("video")) return "video";
    if (file.type.includes("audio")) return "audio";
    if (file.type.includes("text")) return "text";
    return "other";
  };

  const getFileIcon = (type: FileType) => {
    switch (type) {
      case "pdf":
        return <FileText className="h-6 w-6 text-red-500" />;
      case "image":
        return <ImageIcon className="h-6 w-6 text-blue-500" />;
      case "video":
        return <FileVideo className="h-6 w-6 text-purple-500" />;
      case "audio":
        return <FileAudio className="h-6 w-6 text-green-500" />;
      case "text":
        return <File className="h-6 w-6 text-yellow-500" />;
      case "website":
        return <Globe className="h-6 w-6 text-cyan-500" />;
      default:
        return <File className="h-6 w-6 text-gray-500" />;
    }
  };

  const processFile = (file: File) => {
    setIsUploading(true);

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 200);

    // Simulate file upload completion
    setTimeout(() => {
      clearInterval(interval);
      setUploadProgress(100);

      const fileType = getFileType(file);

      // Create a URL for the file (in a real app, this would be a server URL)
      const fileUrl = URL.createObjectURL(file);

      const uploadedFile: UploadedFile = {
        id: Math.random().toString(36).substring(2, 9),
        name: file.name,
        type: fileType,
        size: file.size,
        url: fileUrl,
        uploadedAt: new Date(),
      };

      onFileUpload(uploadedFile);

      // Reset state
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
        onOpenChange(false);
      }, 500);
    }, 2000);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      processFile(file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      processFile(file);
    }
  };

  const triggerFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md bg-[#2a2a2a] border-gray-700 text-white">
        <DialogHeader>
          <DialogTitle>Upload Source</DialogTitle>
          <DialogDescription className="text-gray-400">
            Upload PDFs, documents, images, videos, or audio files
          </DialogDescription>
        </DialogHeader>

        <div
          className={cn(
            "mt-4 border-2 border-dashed rounded-lg p-8 text-center flex flex-col items-center justify-center transition-colors",
            isDragging
              ? "border-blue-500 bg-blue-500/10"
              : "border-gray-700 hover:border-gray-500"
          )}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {isUploading ? (
            <div className="w-full space-y-4">
              <Progress
                value={uploadProgress}
                className="h-2 w-full bg-gray-700"
              />
              <p className="text-sm text-gray-300">
                Uploading... {uploadProgress}%
              </p>
            </div>
          ) : (
            <>
              <div className="w-12 h-12 rounded-full bg-[#3a3a3a] flex items-center justify-center mb-4">
                <Upload className="w-6 h-6 text-blue-400" />
              </div>
              <h3 className="text-lg font-medium mb-2">Drag & Drop</h3>
              <p className="text-sm text-gray-400 mb-4">
                or click to browse files
              </p>

              <div className="flex flex-wrap justify-center gap-3 mb-4">
                <div className="flex items-center gap-1 text-xs text-gray-400">
                  <FileText className="h-4 w-4 text-red-500" />
                  <span>PDF</span>
                </div>
                <div className="flex items-center gap-1 text-xs text-gray-400">
                  <ImageIcon className="h-4 w-4 text-blue-500" />
                  <span>Images</span>
                </div>
                <div className="flex items-center gap-1 text-xs text-gray-400">
                  <FileVideo className="h-4 w-4 text-purple-500" />
                  <span>Videos</span>
                </div>
                <div className="flex items-center gap-1 text-xs text-gray-400">
                  <FileAudio className="h-4 w-4 text-green-500" />
                  <span>Audio</span>
                </div>
                <div className="flex items-center gap-1 text-xs text-gray-400">
                  <File className="h-4 w-4 text-yellow-500" />
                  <span>Text</span>
                </div>
              </div>

              <Button
                variant="outline"
                onClick={triggerFileInput}
                className="bg-[#3a3a3a] border-gray-700 hover:bg-[#444444]"
              >
                Select File
              </Button>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden"
                accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.mp4,.mp3,.wav"
              />
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
