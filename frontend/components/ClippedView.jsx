import { useState } from "react";
import styles from "./ClippedView.module.css";

export default function ClippedView() {
  const [clippedItems, setClippedItems] = useState([
    {
      id: 1,
      title: "AI Research Paper - Attention Mechanisms",
      source: "arxiv.org",
      date: "2 hours ago",
      preview:
        "This paper introduces a novel attention mechanism that improves transformer performance...",
      tags: ["AI", "Research", "Transformers"],
    },
    {
      id: 2,
      title: "Web Development Best Practices",
      source: "developer.mozilla.org",
      date: "1 day ago",
      preview:
        "A comprehensive guide to modern web development practices including performance optimization...",
      tags: ["Web Dev", "Performance", "Best Practices"],
    },
    {
      id: 3,
      title: "Climate Change Data Analysis",
      source: "nature.com",
      date: "3 days ago",
      preview:
        "Recent findings on global temperature trends and their implications for future climate models...",
      tags: ["Climate", "Data", "Science"],
    },
  ]);

  return (
    <div className={styles.clippedContainer}>
      <div className={styles.header}>
        <h1 className={styles.title}>Clipped Items</h1>
        <p className={styles.subtitle}>Your saved clips and excerpts</p>
      </div>

      <div className={styles.actionsBar}>
        <div className={styles.searchContainer}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            type="text"
            placeholder="Search clipped items..."
            className={styles.searchInput}
          />
        </div>
        <div className={styles.filterButtons}>
          <button className={styles.filterButton}>All</button>
          <button className={styles.filterButton}>Recent</button>
          <button className={styles.filterButton}>Favorites</button>
        </div>
      </div>

      <div className={styles.clippedList}>
        {clippedItems.map((item) => (
          <div key={item.id} className={styles.clippedCard}>
            <div className={styles.cardHeader}>
              <h3 className={styles.cardTitle}>{item.title}</h3>
              <div className={styles.cardMeta}>
                <span className={styles.source}>{item.source}</span>
                <span className={styles.date}>{item.date}</span>
              </div>
            </div>
            <p className={styles.preview}>{item.preview}</p>
            <div className={styles.tags}>
              {item.tags.map((tag, index) => (
                <span key={index} className={styles.tag}>
                  {tag}
                </span>
              ))}
            </div>
            <div className={styles.cardActions}>
              <button className={styles.actionButton}>📖 Read</button>
              <button className={styles.actionButton}>📝 Note</button>
              <button className={styles.actionButton}>🔗 Share</button>
              <button className={styles.actionButton}>🗑️ Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
