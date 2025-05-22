import { useState } from "react";
import Link from "next/link";
import styles from "./Sidebar.module.css";

export default function Sidebar({
  visible,
  onMouseLeave,
  onMouseEnter,
  onNavItemClick,
}) {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <div
      className={`${styles.sidebar} ${visible ? styles.visible : ""}`}
      onMouseLeave={onMouseLeave}
      onMouseEnter={onMouseEnter}
    >
      <div className={styles.sidebarHeader}>
        <div className={styles.workspaceInfo}>
          <div className={styles.workspaceIcon}>R</div>
          <div className={styles.workspaceName}>
            Rory's Notion
            <span className={styles.dropdownIcon}>▼</span>
          </div>
        </div>
        <div className={styles.searchContainer}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            type="text"
            placeholder="Search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className={styles.searchInput}
          />
        </div>
      </div>

      <nav className={styles.navigation}>
        <Link href="/workspace" className={styles.navItem}>
          <span className={styles.navIcon}>🏠</span>
          <span>Home</span>
        </Link>
        <div
          className={styles.navItem}
          onClick={() => onNavItemClick("notebooks")}
        >
          <span className={styles.navIcon}>📓</span>
          <span>Notebooks</span>
        </div>
      </nav>

      <div className={styles.sectionHeader}>Favorites</div>
      <div className={styles.favoritesList}>
        <Link href="/workspace/board" className={styles.navItem}>
          <span className={styles.navIcon}>📄</span>
          <span>Drive/why Board</span>
        </Link>
        <Link href="/workspace/interview" className={styles.navItem}>
          <span className={styles.navIcon}>📊</span>
          <span>Technical Interview Ques</span>
        </Link>
        <Link href="/workspace/tasks" className={styles.navItem}>
          <span className={styles.navIcon}>📊</span>
          <span>Tasks v2</span>
        </Link>
        <Link href="/workspace/habits" className={styles.navItem}>
          <span className={styles.navIcon}>📊</span>
          <span>Wall of my Best Habits & Minds...</span>
        </Link>
        {/* Add more favorite items as needed */}
      </div>

      <div className={styles.sectionHeader}>Private</div>
      <div className={styles.privateList}>
        <Link href="/workspace/youtube" className={styles.navItem}>
          <span className={styles.navIcon}>📄</span>
          <span>Youtube Master Page</span>
        </Link>
      </div>

      <div className={styles.sidebarFooter}>
        <button className={styles.inviteButton}>
          <span className={styles.inviteIcon}>👥</span>
          <span>Invite members</span>
        </button>
      </div>
    </div>
  );
}
