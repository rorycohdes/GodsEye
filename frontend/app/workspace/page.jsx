"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
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
  const [currentView, setCurrentView] = useState("feed");
  const searchParams = useSearchParams();

  useEffect(() => {
    const view = searchParams.get("view");
    if (view) {
      setCurrentView(view);
    }
  }, [searchParams]);

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
    <div className={styles.workspaceContainer}>
      <main className={styles.workspaceContent}>{renderCurrentView()}</main>
    </div>
  );
}
