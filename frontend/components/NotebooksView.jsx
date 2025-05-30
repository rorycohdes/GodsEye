import { useState } from "react";
import Link from "next/link";
import styles from "./NotebooksView.module.css";

export default function NotebooksView() {
  const [viewMode, setViewMode] = useState("grid");

  // Sample notebook data
  const notebooks = [
    {
      id: 1,
      title: "Untitled notebook",
      date: "May 18, 2025",
      sources: 0,
      icon: "📔",
    },
    {
      id: 2,
      title: "Apples and Oranges",
      date: "May 2, 2025",
      sources: 1,
      icon: "🍎",
    },
    {
      id: 3,
      title: "Einstein and Relativity: Abridged",
      date: "Mar 20, 2025",
      sources: 1,
      icon: "💡",
    },
    {
      id: 4,
      title: "Clausius, Entropy, and the Second Law of Thermodynamics",
      date: "Mar 10, 2025",
      sources: 2,
      icon: "🔥",
    },
    {
      id: 5,
      title: "Five Equations That Changed the World",
      date: "Feb 19, 2025",
      sources: 1,
      icon: "💡",
    },
    {
      id: 6,
      title: "Between a Rock and a Hard Life: Daniel's Story",
      date: "Feb 6, 2025",
      sources: 1,
      icon: "✈️",
    },
    {
      id: 7,
      title: "Five Equations That Changed the World",
      date: "Feb 19, 2025",
      sources: 2,
      icon: "💡",
    },
    {
      id: 8,
      title: "inGenius: A Crash Course on Creativity",
      date: "Feb 20, 2025",
      sources: 1,
      icon: "💡",
    },
  ];

  return (
    <div className={styles.notebooksContainer}>
      <div className={styles.header}>
        <h1 className={styles.title}>Welcome to NotebookLM</h1>
      </div>

      <div className={styles.actionsBar}>
        <button className={styles.createButton}>
          <span className={styles.plusIcon}>+</span> Create new
        </button>

        <div className={styles.viewControls}>
          <button
            className={`${styles.viewButton} ${
              viewMode === "list" ? styles.active : ""
            }`}
            onClick={() => setViewMode("list")}
          >
            <span className={styles.listIcon}>≡</span>
          </button>
          <button
            className={`${styles.viewButton} ${
              viewMode === "grid" ? styles.active : ""
            }`}
            onClick={() => setViewMode("grid")}
          >
            <span className={styles.gridIcon}>⊞</span>
          </button>
          <div className={styles.sortDropdown}>
            Most recent <span className={styles.dropdownArrow}>▼</span>
          </div>
        </div>
      </div>

      <div
        className={`${styles.notebooksGrid} ${
          viewMode === "list" ? styles.listView : ""
        }`}
      >
        {notebooks.map((notebook) => (
          <Link
            key={notebook.id}
            href={`/notebooks/${notebook.id}`}
            className={styles.notebookLink}
          >
            <div className={styles.notebookCard}>
              <div className={styles.notebookIcon}>{notebook.icon}</div>
              <div className={styles.notebookInfo}>
                <h3 className={styles.notebookTitle}>{notebook.title}</h3>
                <p className={styles.notebookMeta}>
                  {notebook.date} • {notebook.sources}{" "}
                  {notebook.sources === 1 ? "source" : "sources"}
                </p>
              </div>
              <button
                className={styles.moreButton}
                onClick={(e) => e.preventDefault()}
              >
                ⋮
              </button>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
