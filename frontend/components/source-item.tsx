"use client";

import { useState } from "react";
import { formatFileSize } from "@/lib/utils";
import { formatDate } from "@/lib/utils";
import { MoreHorizontal } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { FilePreview } from "./file-preview";
import type { UploadedFile } from "@/components/file-upload-modal";

interface SourceItemProps {
  file: UploadedFile;
  onDelete?: (id: string) => void;
}

export function SourceItem({ file, onDelete }: SourceItemProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const getFileIcon = () => {
    switch (file.type) {
      case "image":
        return <span className="text-2xl">🖼️</span>;
      case "video":
        return <span className="text-2xl">🎬</span>;
      case "audio":
        return <span className="text-2xl">🎵</span>;
      case "pdf":
        return <span className="text-2xl">📄</span>;
      case "text":
        return <span className="text-2xl">📝</span>;
      case "website":
        return <span className="text-2xl">🌐</span>;
      default:
        return <span className="text-2xl">📄</span>;
    }
  };

  const handleDownload = () => {
    // Create a temporary anchor element to trigger download
    const link = document.createElement("a");
    link.href = file.url;
    link.download = file.name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setDropdownOpen(false);
  };

  const handleDelete = () => {
    if (onDelete) {
      onDelete(file.id);
    }
    setDropdownOpen(false);
  };

  return (
    <div
      className="relative group rounded-lg border border-gray-700 bg-[#2a2a2a] p-4 hover:bg-[#333333]"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div
        className="flex items-center gap-3 cursor-pointer"
        onClick={() => setPreviewOpen(true)}
      >
        <div className="w-10 h-10 rounded-lg bg-[#3a3a3a] flex items-center justify-center">
          {getFileIcon()}
        </div>
        <div className="overflow-hidden">
          <p className="text-sm font-medium truncate max-w-[180px]">
            {file.name}
          </p>
          <div className="flex items-center gap-2 text-xs text-gray-400">
            <span>{formatFileSize(file.size)}</span>
            <span>•</span>
            <span>{formatDate(file.uploadedAt)}</span>
          </div>
        </div>
      </div>

      {(isHovered || dropdownOpen) && (
        <DropdownMenu open={dropdownOpen} onOpenChange={setDropdownOpen}>
          <DropdownMenuTrigger className="absolute top-2 right-2 rounded-full p-1.5 hover:bg-secondary">
            <MoreHorizontal className="h-4 w-4 text-muted-foreground" />
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={handleDownload}>
              Download
            </DropdownMenuItem>
            <DropdownMenuItem onClick={handleDelete} variant="destructive">
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )}
      <FilePreview
        file={file}
        open={previewOpen}
        onOpenChange={setPreviewOpen}
      />
    </div>
  );
}
