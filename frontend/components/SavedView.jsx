import { useState } from "react";
import styles from "./SavedView.module.css";

export default function SavedView() {
  const [savedItems, setSavedItems] = useState([
    {
      id: 1,
      title: "Machine Learning Fundamentals",
      type: "Article",
      source: "Medium",
      date: "Dec 15, 2024",
      category: "Education",
      isFavorite: true,
      thumbnail: "📚",
    },
    {
      id: 2,
      title: "React Performance Optimization",
      type: "Video",
      source: "YouTube",
      date: "Dec 14, 2024",
      category: "Development",
      isFavorite: false,
      thumbnail: "🎥",
    },
    {
      id: 3,
      title: "Design System Guidelines",
      type: "Document",
      source: "Figma",
      date: "Dec 12, 2024",
      category: "Design",
      isFavorite: true,
      thumbnail: "🎨",
    },
    {
      id: 4,
      title: "API Documentation Best Practices",
      type: "Article",
      source: "Dev.to",
      date: "Dec 10, 2024",
      category: "Development",
      isFavorite: false,
      thumbnail: "📖",
    },
  ]);

  const [selectedCategory, setSelectedCategory] = useState("All");
  const categories = ["All", "Education", "Development", "Design", "Research"];

  const filteredItems =
    selectedCategory === "All"
      ? savedItems
      : savedItems.filter((item) => item.category === selectedCategory);

  const toggleFavorite = (id) => {
    setSavedItems(
      savedItems.map((item) =>
        item.id === id ? { ...item, isFavorite: !item.isFavorite } : item
      )
    );
  };

  return (
    <div className={styles.savedContainer}>
      <div className={styles.header}>
        <h1 className={styles.title}>Saved Items</h1>
        <p className={styles.subtitle}>Your bookmarked content and resources</p>
      </div>

      <div className={styles.actionsBar}>
        <div className={styles.searchContainer}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            type="text"
            placeholder="Search saved items..."
            className={styles.searchInput}
          />
        </div>
        <div className={styles.categoryFilter}>
          {categories.map((category) => (
            <button
              key={category}
              className={`${styles.categoryButton} ${
                selectedCategory === category ? styles.active : ""
              }`}
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.savedGrid}>
        {filteredItems.map((item) => (
          <div key={item.id} className={styles.savedCard}>
            <div className={styles.cardThumbnail}>
              <span className={styles.thumbnailIcon}>{item.thumbnail}</span>
              <button
                className={`${styles.favoriteButton} ${
                  item.isFavorite ? styles.favorited : ""
                }`}
                onClick={() => toggleFavorite(item.id)}
              >
                {item.isFavorite ? "❤️" : "🤍"}
              </button>
            </div>
            <div className={styles.cardContent}>
              <div className={styles.cardHeader}>
                <h3 className={styles.cardTitle}>{item.title}</h3>
                <span className={styles.cardType}>{item.type}</span>
              </div>
              <div className={styles.cardMeta}>
                <span className={styles.source}>{item.source}</span>
                <span className={styles.date}>{item.date}</span>
              </div>
              <div className={styles.cardCategory}>
                <span className={styles.categoryTag}>{item.category}</span>
              </div>
            </div>
            <div className={styles.cardActions}>
              <button className={styles.actionButton}>📖 Open</button>
              <button className={styles.actionButton}>📝 Note</button>
              <button className={styles.actionButton}>🔗 Share</button>
              <button className={styles.actionButton}>🗑️ Remove</button>
            </div>
          </div>
        ))}
      </div>

      {filteredItems.length === 0 && (
        <div className={styles.emptyState}>
          <div className={styles.emptyIcon}>💾</div>
          <h3>No saved items found</h3>
          <p>Items you save will appear here</p>
        </div>
      )}
    </div>
  );
}
