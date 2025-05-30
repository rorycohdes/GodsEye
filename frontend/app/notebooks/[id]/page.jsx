"use client";

import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import styles from "./NotebookDetail.module.css";

export default function NotebookDetailPage() {
  const params = useParams();
  const [notebook, setNotebook] = useState(null);
  const [loading, setLoading] = useState(true);

  // Sample notebook data - in a real app, this would come from an API
  const notebooks = [
    {
      id: "1",
      title: "Untitled notebook",
      date: "May 18, 2025",
      sources: 0,
      icon: "📔",
      content:
        "This is your untitled notebook. Start writing your thoughts and ideas here.",
    },
    {
      id: "2",
      title: "Apples and Oranges",
      date: "May 2, 2025",
      sources: 1,
      icon: "🍎",
      content:
        "A comprehensive comparison between apples and oranges, exploring their nutritional values, origins, and cultural significance.",
    },
    {
      id: "3",
      title: "Einstein and Relativity: Abridged",
      date: "Mar 20, 2025",
      sources: 1,
      icon: "💡",
      content:
        "An exploration of Einstein's theory of relativity, breaking down complex concepts into digestible explanations.",
    },
    {
      id: "4",
      title: "Clausius, Entropy, and the Second Law of Thermodynamics",
      date: "Mar 10, 2025",
      sources: 2,
      icon: "🔥",
      content:
        "Diving deep into thermodynamics, exploring Clausius's contributions and the fundamental concept of entropy.",
    },
    {
      id: "5",
      title: "Five Equations That Changed the World",
      date: "Feb 19, 2025",
      sources: 1,
      icon: "💡",
      content:
        "An analysis of the most influential mathematical equations in human history and their impact on science.",
    },
    {
      id: "6",
      title: "Between a Rock and a Hard Life: Daniel's Story",
      date: "Feb 6, 2025",
      sources: 1,
      icon: "✈️",
      content:
        "A personal narrative exploring challenges, resilience, and personal growth through difficult circumstances.",
    },
    {
      id: "7",
      title: "Five Equations That Changed the World",
      date: "Feb 19, 2025",
      sources: 2,
      icon: "💡",
      content:
        "A deeper dive into mathematical equations that revolutionized our understanding of the universe.",
    },
    {
      id: "8",
      title: "inGenius: A Crash Course on Creativity",
      date: "Feb 20, 2025",
      sources: 1,
      icon: "💡",
      content:
        "Exploring the science and art of creativity, with practical techniques for enhancing innovative thinking.",
    },
  ];

  useEffect(() => {
    const foundNotebook = notebooks.find((nb) => nb.id === params.id);
    setNotebook(foundNotebook);
    setLoading(false);
  }, [params.id]);

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.spinner}></div>
        <p>Loading notebook...</p>
      </div>
    );
  }

  if (!notebook) {
    return (
      <div className={styles.notFoundContainer}>
        <h1>Notebook Not Found</h1>
        <p>The notebook you're looking for doesn't exist.</p>
        <a href="/notebooks" className={styles.backLink}>
          ← Back to Notebooks
        </a>
      </div>
    );
  }

  return (
    <div className={styles.notebookContainer}>
      <div className={styles.header}>
        <a href="/notebooks" className={styles.backLink}>
          ← Back to Notebooks
        </a>
        <div className={styles.notebookInfo}>
          <div className={styles.titleSection}>
            <span className={styles.icon}>{notebook.icon}</span>
            <h1 className={styles.title}>{notebook.title}</h1>
          </div>
          <p className={styles.meta}>
            {notebook.date} • {notebook.sources}{" "}
            {notebook.sources === 1 ? "source" : "sources"}
          </p>
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.editor}>
          <h2>Content</h2>
          <div className={styles.textArea}>{notebook.content}</div>
        </div>

        <div className={styles.sidebar}>
          <div className={styles.sources}>
            <h3>Sources</h3>
            {notebook.sources === 0 ? (
              <p className={styles.noSources}>No sources added yet</p>
            ) : (
              <div className={styles.sourcesList}>
                {Array.from({ length: notebook.sources }, (_, i) => (
                  <div key={i} className={styles.source}>
                    <div className={styles.sourceIcon}>📄</div>
                    <span>Source {i + 1}</span>
                  </div>
                ))}
              </div>
            )}
            <button className={styles.addSourceButton}>+ Add Source</button>
          </div>

          <div className={styles.chat}>
            <h3>Chat with Notebook</h3>
            <div className={styles.chatArea}>
              <p className={styles.chatPlaceholder}>
                Ask questions about your notebook...
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
