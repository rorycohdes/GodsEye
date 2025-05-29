"use client";

import type React from "react";
import "./globals.css";
import { Inter } from "next/font/google";
import { useState } from "react";
import Sidebar from "../components/Sidebar";
import { useRouter } from "next/navigation";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const router = useRouter();

  const handleMouseMove = (e: React.MouseEvent) => {
    // Show sidebar when mouse is near the left edge (within 20px)
    if (e.clientX <= 20) {
      setSidebarVisible(true);
    }
  };

  const handleNavItemClick = (view: string) => {
    // Route to workspace with the specific view as a query parameter
    router.push(`/workspace?view=${view}`);
  };

  const handleFavoriteItemClick = (itemName: string) => {
    if (itemName === "Untitled") {
      router.push("/workspace?view=jobboard");
    } else if (itemName === "Network Graph") {
      router.push("/workspace?view=graph");
    }
  };

  return (
    <html lang="en">
      <head>
        <title>Notebook Interface</title>
        <meta
          name="description"
          content="A research and note-taking interface"
        />
      </head>
      <body className={inter.className}>
        <div
          style={{
            display: "flex",
            minHeight: "100vh",
            position: "relative",
          }}
          onMouseMove={handleMouseMove}
        >
          <Sidebar
            visible={sidebarVisible}
            onMouseLeave={() => setSidebarVisible(false)}
            onMouseEnter={() => setSidebarVisible(true)}
            onNavItemClick={handleNavItemClick}
            onFavoriteItemClick={handleFavoriteItemClick}
          />
          <main
            style={{
              flex: 1,
              position: "relative",
              minHeight: "100vh",
            }}
          >
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
