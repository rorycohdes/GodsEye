"use client";

import { useState } from "react";
import Sidebar from "../../components/Sidebar";
import styles from "./workspace.module.css";

export default function WorkspacePage() {
  const [sidebarVisible, setSidebarVisible] = useState(false);

  const handleMouseMove = (e) => {
    // Show sidebar when mouse is near the left edge (within 20px)
    if (e.clientX <= 20) {
      setSidebarVisible(true);
    }
  };

  return (
    <div className={styles.workspaceContainer} onMouseMove={handleMouseMove}>
      <Sidebar
        visible={sidebarVisible}
        onMouseLeave={() => setSidebarVisible(false)}
        onMouseEnter={() => setSidebarVisible(true)}
      />
      <main className={styles.workspaceContent}>
        {/* Your workspace content goes here */}
      </main>
    </div>
  );
}
