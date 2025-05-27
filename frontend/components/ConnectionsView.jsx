import { useState } from "react";
import styles from "./ConnectionsView.module.css";

export default function ConnectionsView() {
  const [connections, setConnections] = useState([
    {
      id: 1,
      name: "Dr. Sarah Chen",
      title: "AI Research Scientist",
      company: "Stanford University",
      avatar: "👩‍🔬",
      status: "online",
      lastActive: "2 hours ago",
      mutualConnections: 12,
      tags: ["AI", "Machine Learning", "Research"],
    },
    {
      id: 2,
      name: "Marcus Johnson",
      title: "Senior Software Engineer",
      company: "Google",
      avatar: "👨‍💻",
      status: "away",
      lastActive: "1 day ago",
      mutualConnections: 8,
      tags: ["React", "Node.js", "Cloud"],
    },
    {
      id: 3,
      name: "Elena Rodriguez",
      title: "UX Design Lead",
      company: "Figma",
      avatar: "👩‍🎨",
      status: "online",
      lastActive: "30 minutes ago",
      mutualConnections: 15,
      tags: ["Design", "UX", "Product"],
    },
    {
      id: 4,
      name: "David Kim",
      title: "Data Scientist",
      company: "Netflix",
      avatar: "👨‍💼",
      status: "offline",
      lastActive: "3 days ago",
      mutualConnections: 6,
      tags: ["Data Science", "Analytics", "Python"],
    },
  ]);

  const [selectedFilter, setSelectedFilter] = useState("All");
  const filters = ["All", "Online", "Recent", "Favorites"];

  const filteredConnections = connections.filter((connection) => {
    if (selectedFilter === "All") return true;
    if (selectedFilter === "Online") return connection.status === "online";
    if (selectedFilter === "Recent")
      return (
        connection.lastActive.includes("hour") ||
        connection.lastActive.includes("minutes")
      );
    return false;
  });

  return (
    <div className={styles.connectionsContainer}>
      <div className={styles.header}>
        <h1 className={styles.title}>Connections</h1>
        <p className={styles.subtitle}>
          Your professional network and collaborators
        </p>
      </div>

      <div className={styles.actionsBar}>
        <div className={styles.searchContainer}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            type="text"
            placeholder="Search connections..."
            className={styles.searchInput}
          />
        </div>
        <div className={styles.filterButtons}>
          {filters.map((filter) => (
            <button
              key={filter}
              className={`${styles.filterButton} ${
                selectedFilter === filter ? styles.active : ""
              }`}
              onClick={() => setSelectedFilter(filter)}
            >
              {filter}
            </button>
          ))}
        </div>
        <button className={styles.addButton}>
          <span className={styles.plusIcon}>+</span>
          Add Connection
        </button>
      </div>

      <div className={styles.connectionsGrid}>
        {filteredConnections.map((connection) => (
          <div key={connection.id} className={styles.connectionCard}>
            <div className={styles.cardHeader}>
              <div className={styles.avatarContainer}>
                <span className={styles.avatar}>{connection.avatar}</span>
                <div
                  className={`${styles.statusIndicator} ${
                    styles[connection.status]
                  }`}
                ></div>
              </div>
              <div className={styles.connectionInfo}>
                <h3 className={styles.name}>{connection.name}</h3>
                <p className={styles.title}>{connection.title}</p>
                <p className={styles.company}>{connection.company}</p>
              </div>
            </div>

            <div className={styles.connectionMeta}>
              <div className={styles.metaItem}>
                <span className={styles.metaLabel}>Last Active:</span>
                <span className={styles.metaValue}>
                  {connection.lastActive}
                </span>
              </div>
              <div className={styles.metaItem}>
                <span className={styles.metaLabel}>Mutual:</span>
                <span className={styles.metaValue}>
                  {connection.mutualConnections} connections
                </span>
              </div>
            </div>

            <div className={styles.tags}>
              {connection.tags.map((tag, index) => (
                <span key={index} className={styles.tag}>
                  {tag}
                </span>
              ))}
            </div>

            <div className={styles.cardActions}>
              <button className={styles.actionButton}>💬 Message</button>
              <button className={styles.actionButton}>📧 Email</button>
              <button className={styles.actionButton}>👁️ Profile</button>
              <button className={styles.actionButton}>⋮</button>
            </div>
          </div>
        ))}
      </div>

      {filteredConnections.length === 0 && (
        <div className={styles.emptyState}>
          <div className={styles.emptyIcon}>🔗</div>
          <h3>No connections found</h3>
          <p>Try adjusting your filters or add new connections</p>
        </div>
      )}

      <div className={styles.networkStats}>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>{connections.length}</div>
          <div className={styles.statLabel}>Total Connections</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {connections.filter((c) => c.status === "online").length}
          </div>
          <div className={styles.statLabel}>Online Now</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {Math.round(
              connections.reduce((sum, c) => sum + c.mutualConnections, 0) /
                connections.length
            )}
          </div>
          <div className={styles.statLabel}>Avg. Mutual</div>
        </div>
      </div>
    </div>
  );
}
