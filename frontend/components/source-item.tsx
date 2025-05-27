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

interface SourceItemProps {
  file: {
    id: string;
    name: string;
    size: number;
    type: string;
    uploadedAt: Date;
    url: string;
  };
}

export function SourceItem({ file }: SourceItemProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [previewOpen, setPreviewOpen] = useState(false);

  const getFileIcon = () => {
    if (file.type.includes("image")) {
      return <span className="text-2xl">🖼️</span>;
    }

    if (file.type.includes("video")) {
      return <span className="text-2xl">🎬</span>;
    }

    if (file.type.includes("audio")) {
      return <span className="text-2xl">🎵</span>;
    }

    return <span className="text-2xl">📄</span>;
  };

  return (
    <div
      className="relative group rounded-lg border border-border bg-card p-4 hover:bg-muted"
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

      {isHovered && (
        <DropdownMenu>
          <DropdownMenuTrigger className="absolute top-2 right-2 rounded-full p-1.5 hover:bg-secondary">
            <MoreHorizontal className="h-4 w-4 text-muted-foreground" />
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" forceMount>
            <DropdownMenuItem>Download</DropdownMenuItem>
            <DropdownMenuItem>Delete</DropdownMenuItem>
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
