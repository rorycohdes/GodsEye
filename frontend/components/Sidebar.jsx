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
  const [favoriteItems, setFavoriteItems] = useState([
    { id: 1, name: "Untitled", icon: "📄", isEditing: false },
  ]);

  // Function to add a new untitled item
  const addNewFavoriteItem = () => {
    const newId =
      favoriteItems.length > 0
        ? Math.max(...favoriteItems.map((item) => item.id)) + 1
        : 1;

    setFavoriteItems([
      ...favoriteItems,
      { id: newId, name: "Untitled", icon: "📄", isEditing: false },
    ]);
  };

  // Function to handle renaming items
  const startEditing = (id) => {
    setFavoriteItems(
      favoriteItems.map((item) =>
        item.id === id ? { ...item, isEditing: true } : item
      )
    );
  };

  const handleNameChange = (id, newName) => {
    setFavoriteItems(
      favoriteItems.map((item) =>
        item.id === id ? { ...item, name: newName } : item
      )
    );
  };

  const finishEditing = (id) => {
    setFavoriteItems(
      favoriteItems.map((item) =>
        item.id === id ? { ...item, isEditing: false } : item
      )
    );
  };

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

      <div className={styles.sectionHeader}>
        <span>Favorites</span>
        <button
          className={styles.addButton}
          onClick={addNewFavoriteItem}
          title="Add new item"
        >
          +
        </button>
      </div>

      <div className={styles.favoritesList}>
        {favoriteItems.map((item) => (
          <div key={item.id} className={styles.navItem}>
            <span className={styles.navIcon}>{item.icon}</span>
            {item.isEditing ? (
              <input
                type="text"
                value={item.name}
                onChange={(e) => handleNameChange(item.id, e.target.value)}
                onBlur={() => finishEditing(item.id)}
                onKeyDown={(e) => e.key === "Enter" && finishEditing(item.id)}
                className={styles.editInput}
                autoFocus
              />
            ) : (
              <span onClick={() => startEditing(item.id)}>{item.name}</span>
            )}
            <div className={styles.itemActions}>
              <button
                className={styles.renameButton}
                onClick={() => startEditing(item.id)}
              >
                ✏️
              </button>
            </div>
          </div>
        ))}
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
