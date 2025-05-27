"use client";

import { useState } from "react";
import Sidebar from "../../components/Sidebar";
import NotebooksView from "../../components/NotebooksView";
import JobBoardView from "../../components/JobBoardView";
import ForceDirectedGraph from "../../components/ForceDirectedGraph";
import ClippedView from "../../components/ClippedView";
import SavedView from "../../components/SavedView";
import ConnectionsView from "../../components/ConnectionsView";
import ScrapedView from "../../components/ScrapedView";
import KnowledgeBaseView from "../../components/KnowledgeBaseView";
import styles from "./workspace.module.css";

export default function WorkspacePage() {
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [currentView, setCurrentView] = useState("feed");

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

  const renderCurrentView = () => {
    switch (currentView) {
      case "notebooks":
        return <NotebooksView />;
      case "clipped":
        return <ClippedView />;
      case "saved":
        return <SavedView />;
      case "connections":
        return <ConnectionsView />;
      case "scraped":
        return <ScrapedView />;
      case "knowledge-base":
        return <KnowledgeBaseView />;
      case "jobboard":
        return <JobBoardView />;
      case "graph":
        return <ForceDirectedGraph />;
      default:
        return (
          <div className={styles.homeView}>
            <h1>Feed</h1>
            <p>
              Your personalized content feed. Select an option from the sidebar
              to explore different sections.
            </p>
          </div>
        );
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
      <main className={styles.workspaceContent}>{renderCurrentView()}</main>
    </div>
  );
}
