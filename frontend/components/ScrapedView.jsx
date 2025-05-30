import { useState } from "react";
import styles from "./ScrapedView.module.css";

export default function ScrapedView() {
  const [scrapedData, setScrapedData] = useState([
    {
      id: 1,
      url: "https://arxiv.org/abs/2023.12345",
      title: "Advances in Neural Network Architecture",
      domain: "arxiv.org",
      scrapedAt: "2024-12-15 14:30",
      status: "completed",
      dataSize: "2.3 MB",
      type: "Research Paper",
      tags: ["AI", "Neural Networks", "Research"],
      preview:
        "This paper presents novel approaches to neural network design...",
    },
    {
      id: 2,
      url: "https://techcrunch.com/2024/12/14/ai-startup-funding",
      title: "AI Startup Raises $50M in Series B Funding",
      domain: "techcrunch.com",
      scrapedAt: "2024-12-14 09:15",
      status: "completed",
      dataSize: "1.8 MB",
      type: "News Article",
      tags: ["Startup", "Funding", "AI"],
      preview:
        "A promising AI startup focused on enterprise solutions has secured...",
    },
    {
      id: 3,
      url: "https://github.com/user/awesome-project",
      title: "Awesome Machine Learning Project",
      domain: "github.com",
      scrapedAt: "2024-12-13 16:45",
      status: "processing",
      dataSize: "5.1 MB",
      type: "Code Repository",
      tags: ["GitHub", "Machine Learning", "Open Source"],
      preview:
        "A comprehensive machine learning framework with extensive documentation...",
    },
    {
      id: 4,
      url: "https://blog.openai.com/gpt-4-research",
      title: "GPT-4 Research Insights and Applications",
      domain: "blog.openai.com",
      scrapedAt: "2024-12-12 11:20",
      status: "failed",
      dataSize: "0 MB",
      type: "Blog Post",
      tags: ["OpenAI", "GPT-4", "Research"],
      preview: "Error: Access denied - content requires authentication",
    },
  ]);

  const [selectedStatus, setSelectedStatus] = useState("All");
  const statusFilters = ["All", "Completed", "Processing", "Failed"];

  const filteredData = scrapedData.filter((item) => {
    if (selectedStatus === "All") return true;
    return item.status === selectedStatus.toLowerCase();
  });

  const getStatusColor = (status) => {
    switch (status) {
      case "completed":
        return "#57f287";
      case "processing":
        return "#faa61a";
      case "failed":
        return "#ed4245";
      default:
        return "#747f8d";
    }
  };

  const retryScrap = (id) => {
    setScrapedData(
      scrapedData.map((item) =>
        item.id === id ? { ...item, status: "processing" } : item
      )
    );
  };

  return (
    <div className={styles.scrapedContainer}>
      <div className={styles.header}>
        <h1 className={styles.title}>Scraped Data</h1>
        <p className={styles.subtitle}>
          Web content and data extraction results
        </p>
      </div>

      <div className={styles.actionsBar}>
        <div className={styles.searchContainer}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            type="text"
            placeholder="Search scraped content..."
            className={styles.searchInput}
          />
        </div>
        <div className={styles.statusFilter}>
          {statusFilters.map((status) => (
            <button
              key={status}
              className={`${styles.statusButton} ${
                selectedStatus === status ? styles.active : ""
              }`}
              onClick={() => setSelectedStatus(status)}
            >
              {status}
            </button>
          ))}
        </div>
        <button className={styles.newScrapButton}>
          <span className={styles.plusIcon}>+</span>
          New Scrape
        </button>
      </div>

      <div className={styles.scrapedList}>
        {filteredData.map((item) => (
          <div key={item.id} className={styles.scrapedCard}>
            <div className={styles.cardHeader}>
              <div className={styles.urlInfo}>
                <h3 className={styles.cardTitle}>{item.title}</h3>
                <div className={styles.urlDetails}>
                  <span className={styles.domain}>{item.domain}</span>
                  <span className={styles.url}>{item.url}</span>
                </div>
              </div>
              <div className={styles.statusBadge}>
                <div
                  className={styles.statusIndicator}
                  style={{ backgroundColor: getStatusColor(item.status) }}
                ></div>
                <span className={styles.statusText}>{item.status}</span>
              </div>
            </div>

            <div className={styles.cardMeta}>
              <div className={styles.metaItem}>
                <span className={styles.metaLabel}>Scraped:</span>
                <span className={styles.metaValue}>{item.scrapedAt}</span>
              </div>
              <div className={styles.metaItem}>
                <span className={styles.metaLabel}>Size:</span>
                <span className={styles.metaValue}>{item.dataSize}</span>
              </div>
              <div className={styles.metaItem}>
                <span className={styles.metaLabel}>Type:</span>
                <span className={styles.metaValue}>{item.type}</span>
              </div>
            </div>

            <div className={styles.preview}>
              <p className={styles.previewText}>{item.preview}</p>
            </div>

            <div className={styles.tags}>
              {item.tags.map((tag, index) => (
                <span key={index} className={styles.tag}>
                  {tag}
                </span>
              ))}
            </div>

            <div className={styles.cardActions}>
              {item.status === "completed" && (
                <>
                  <button className={styles.actionButton}>📖 View Data</button>
                  <button className={styles.actionButton}>💾 Export</button>
                  <button className={styles.actionButton}>📊 Analyze</button>
                </>
              )}
              {item.status === "processing" && (
                <button className={styles.actionButton} disabled>
                  ⏳ Processing...
                </button>
              )}
              {item.status === "failed" && (
                <button
                  className={styles.actionButton}
                  onClick={() => retryScrap(item.id)}
                >
                  🔄 Retry
                </button>
              )}
              <button className={styles.actionButton}>🗑️ Delete</button>
            </div>
          </div>
        ))}
      </div>

      {filteredData.length === 0 && (
        <div className={styles.emptyState}>
          <div className={styles.emptyIcon}>🕷️</div>
          <h3>No scraped data found</h3>
          <p>Start scraping web content to see results here</p>
        </div>
      )}

      <div className={styles.scrapingStats}>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>{scrapedData.length}</div>
          <div className={styles.statLabel}>Total Scrapes</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {scrapedData.filter((item) => item.status === "completed").length}
          </div>
          <div className={styles.statLabel}>Completed</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {scrapedData
              .reduce((total, item) => {
                const size = parseFloat(item.dataSize);
                return total + (isNaN(size) ? 0 : size);
              }, 0)
              .toFixed(1)}{" "}
            MB
          </div>
          <div className={styles.statLabel}>Total Data</div>
        </div>
      </div>
    </div>
  );
}
