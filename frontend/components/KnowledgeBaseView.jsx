import { useState } from "react";
import styles from "./KnowledgeBaseView.module.css";

export default function KnowledgeBaseView() {
  const [knowledgeItems, setKnowledgeItems] = useState([
    {
      id: 1,
      title: "Machine Learning Fundamentals",
      category: "AI & ML",
      type: "Article Collection",
      lastUpdated: "2024-12-15",
      tags: ["Machine Learning", "Fundamentals", "AI"],
      description:
        "Comprehensive collection of machine learning concepts, algorithms, and practical applications.",
      items: 24,
      views: 156,
      icon: "🤖",
    },
    {
      id: 2,
      title: "Web Development Best Practices",
      category: "Development",
      type: "Guide",
      lastUpdated: "2024-12-14",
      tags: ["Web Dev", "Best Practices", "Frontend"],
      description:
        "Curated guide covering modern web development practices, frameworks, and tools.",
      items: 18,
      views: 89,
      icon: "💻",
    },
    {
      id: 3,
      title: "Data Science Methodology",
      category: "Data Science",
      type: "Methodology",
      lastUpdated: "2024-12-13",
      tags: ["Data Science", "Methodology", "Analytics"],
      description:
        "Step-by-step methodology for data science projects from problem definition to deployment.",
      items: 12,
      views: 203,
      icon: "📊",
    },
    {
      id: 4,
      title: "UX Design Principles",
      category: "Design",
      type: "Reference",
      lastUpdated: "2024-12-12",
      tags: ["UX", "Design", "Principles"],
      description:
        "Essential UX design principles and guidelines for creating user-centered experiences.",
      items: 15,
      views: 127,
      icon: "🎨",
    },
    {
      id: 5,
      title: "Blockchain Technology Overview",
      category: "Technology",
      type: "Research",
      lastUpdated: "2024-12-10",
      tags: ["Blockchain", "Cryptocurrency", "Technology"],
      description:
        "Comprehensive overview of blockchain technology, applications, and future trends.",
      items: 8,
      views: 74,
      icon: "⛓️",
    },
  ]);

  const [selectedCategory, setSelectedCategory] = useState("All");
  const [viewMode, setViewMode] = useState("grid");

  const categories = [
    "All",
    "AI & ML",
    "Development",
    "Data Science",
    "Design",
    "Technology",
  ];

  const filteredItems =
    selectedCategory === "All"
      ? knowledgeItems
      : knowledgeItems.filter((item) => item.category === selectedCategory);

  return (
    <div className={styles.knowledgeContainer}>
      <div className={styles.header}>
        <h1 className={styles.title}>Knowledge Base</h1>
        <p className={styles.subtitle}>
          Organized collection of insights, research, and documentation
        </p>
      </div>

      <div className={styles.actionsBar}>
        <div className={styles.searchContainer}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            type="text"
            placeholder="Search knowledge base..."
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

        <div className={styles.viewControls}>
          <button
            className={`${styles.viewButton} ${
              viewMode === "grid" ? styles.active : ""
            }`}
            onClick={() => setViewMode("grid")}
          >
            ⊞
          </button>
          <button
            className={`${styles.viewButton} ${
              viewMode === "list" ? styles.active : ""
            }`}
            onClick={() => setViewMode("list")}
          >
            ≡
          </button>
        </div>

        <button className={styles.createButton}>
          <span className={styles.plusIcon}>+</span>
          Create New
        </button>
      </div>

      <div
        className={`${styles.knowledgeGrid} ${
          viewMode === "list" ? styles.listView : ""
        }`}
      >
        {filteredItems.map((item) => (
          <div key={item.id} className={styles.knowledgeCard}>
            <div className={styles.cardHeader}>
              <div className={styles.iconContainer}>
                <span className={styles.cardIcon}>{item.icon}</span>
              </div>
              <div className={styles.cardInfo}>
                <h3 className={styles.cardTitle}>{item.title}</h3>
                <div className={styles.cardMeta}>
                  <span className={styles.category}>{item.category}</span>
                  <span className={styles.type}>{item.type}</span>
                </div>
              </div>
            </div>

            <p className={styles.description}>{item.description}</p>

            <div className={styles.tags}>
              {item.tags.map((tag, index) => (
                <span key={index} className={styles.tag}>
                  {tag}
                </span>
              ))}
            </div>

            <div className={styles.cardStats}>
              <div className={styles.stat}>
                <span className={styles.statIcon}>📄</span>
                <span className={styles.statValue}>{item.items} items</span>
              </div>
              <div className={styles.stat}>
                <span className={styles.statIcon}>👁️</span>
                <span className={styles.statValue}>{item.views} views</span>
              </div>
              <div className={styles.stat}>
                <span className={styles.statIcon}>📅</span>
                <span className={styles.statValue}>{item.lastUpdated}</span>
              </div>
            </div>

            <div className={styles.cardActions}>
              <button className={styles.actionButton}>📖 View</button>
              <button className={styles.actionButton}>✏️ Edit</button>
              <button className={styles.actionButton}>🔗 Share</button>
              <button className={styles.actionButton}>⋮</button>
            </div>
          </div>
        ))}
      </div>

      {filteredItems.length === 0 && (
        <div className={styles.emptyState}>
          <div className={styles.emptyIcon}>🧠</div>
          <h3>No knowledge items found</h3>
          <p>Create your first knowledge base entry to get started</p>
          <button className={styles.emptyCreateButton}>
            <span className={styles.plusIcon}>+</span>
            Create Knowledge Item
          </button>
        </div>
      )}

      <div className={styles.knowledgeStats}>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>{knowledgeItems.length}</div>
          <div className={styles.statLabel}>Knowledge Items</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>{categories.length - 1}</div>
          <div className={styles.statLabel}>Categories</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {knowledgeItems.reduce((total, item) => total + item.items, 0)}
          </div>
          <div className={styles.statLabel}>Total Items</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {knowledgeItems.reduce((total, item) => total + item.views, 0)}
          </div>
          <div className={styles.statLabel}>Total Views</div>
        </div>
      </div>
    </div>
  );
}
