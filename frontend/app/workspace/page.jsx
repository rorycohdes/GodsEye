"use client";

import { useState } from "react";
import Sidebar from "../../components/Sidebar";
import NotebooksView from "../../components/NotebooksView";
import JobBoardView from "../../components/JobBoardView";
import ForceDirectedGraph from "../../components/ForceDirectedGraph";
import styles from "./workspace.module.css";

export default function WorkspacePage() {
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [currentView, setCurrentView] = useState("home");

  const handleMouseMove = (e) => {
    // Show sidebar when mouse is near the left edge (within 20px)
    if (e.clientX <= 20) {
      setSidebarVisible(true);
    }
  };

  const handleNavItemClick = (view) => {
    setCurrentView(view);
  };

  const handleFavoriteItemClick = (itemName) => {
    if (itemName === "Untitled") {
      setCurrentView("jobboard");
    } else if (itemName === "Network Graph") {
      setCurrentView("graph");
    }
  };

  return (
    <div className={styles.workspaceContainer} onMouseMove={handleMouseMove}>
      <Sidebar
        visible={sidebarVisible}
        onMouseLeave={() => setSidebarVisible(false)}
        onMouseEnter={() => setSidebarVisible(true)}
        onNavItemClick={handleNavItemClick}
        onFavoriteItemClick={handleFavoriteItemClick}
      />
      <main className={styles.workspaceContent}>
        {currentView === "notebooks" ? (
          <NotebooksView />
        ) : currentView === "jobboard" ? (
          <JobBoardView />
        ) : currentView === "graph" ? (
          <ForceDirectedGraph />
        ) : (
          <div className={styles.homeView}>
            {/* Default home view content */}
            <h1>Home</h1>
            <p>Select an option from the sidebar to get started.</p>
          </div>
        )}
      </main>
    </div>
  );
}
