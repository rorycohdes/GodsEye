import { useState } from "react";
import styles from "./JobBoardView.module.css";

export default function JobBoardView() {
  const [selectedFilters, setSelectedFilters] = useState([]);

  // Sample job data
  const jobs = [
    {
      id: 1,
      title: "Técnico de Mantenimiento",
      company: "COSVI",
      location: "Rio Piedras, PR, United States",
      type: "Full Time",
      timePosted: "7h",
      salary: "",
    },
    {
      id: 2,
      title: "Community Investment Analyst",
      company: "Connecting underserved communities",
      location: "Portland, Maine, United States",
      type: "Full Time",
      timePosted: "7h",
      salary: "$60k-$80k/yr",
    },
    {
      id: 3,
      title: "Facilities Coordinator II, R&M",
      company: "RSM Facility Solutions",
      location: "Toms River, New Jersey, United States",
      type: "Full Time",
      timePosted: "7h",
      salary: "$22-$25/hr",
    },
    {
      id: 4,
      title: "Mobile Deposit Capture Associate (Part Time)",
      company: "N/A",
      location: "Lubbock, Texas, United States",
      type: "Part Time",
      timePosted: "7h",
      salary: "",
    },
    {
      id: 5,
      title: "Teller CSR",
      company: "First Financial Bank",
      location: "Robinson, Illinois, United States",
      type: "Full Time",
      timePosted: "7h",
      salary: "",
    },
  ];

  // Filter categories
  const filterCategories = [
    { id: "departments", label: "Departments" },
    { id: "salary", label: "Salary" },
    { id: "commitment", label: "Commitment" },
    { id: "experience", label: "Experience" },
    { id: "jobTitles", label: "Job Titles & Keywords" },
    { id: "education", label: "Education" },
    { id: "licenses", label: "Licenses & Certifications" },
    { id: "security", label: "Security Clearance" },
    { id: "languages", label: "Languages" },
    { id: "shifts", label: "Shifts & Schedules" },
    { id: "travel", label: "Travel Requirement" },
    { id: "benefits", label: "Benefits & Perks" },
    { id: "encouraged", label: "Encouraged to Apply" },
  ];

  const secondaryFilters = [
    { id: "company", label: "Company" },
    { id: "industry", label: "Industry" },
    { id: "stage", label: "Stage & Funding" },
    { id: "size", label: "Size" },
    { id: "founding", label: "Founding Year" },
  ];

  const toggleFilter = (filterId) => {
    if (selectedFilters.includes(filterId)) {
      setSelectedFilters(selectedFilters.filter((id) => id !== filterId));
    } else {
      setSelectedFilters([...selectedFilters, filterId]);
    }
  };

  return (
    <div className={styles.jobBoardContainer}>
      <div className={styles.header}>
        <div className={styles.logo}>
          <div className={styles.logoIcon}>
            <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path d="M3 17h18a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zm0-6h18a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zm0-6h18a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2z" />
            </svg>
          </div>
          <h1 className={styles.logoText}>HiringCafe</h1>
        </div>

        <div className={styles.searchBar}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            type="text"
            placeholder="Search"
            className={styles.searchInput}
          />
        </div>

        <div className={styles.locationFilter}>
          <span className={styles.locationIcon}>📍</span>
          <div className={styles.locationText}>
            <div>United States</div>
            <div className={styles.locationSubtext}>
              Remote · Hybrid · Onsite · All Environments
            </div>
          </div>
          <span className={styles.dropdownIcon}>▼</span>
        </div>

        <button className={styles.loginButton}>Log in</button>
      </div>

      <div className={styles.filterSection}>
        <div className={styles.filterTags}>
          {filterCategories.map((filter) => (
            <button
              key={filter.id}
              className={`${styles.filterTag} ${
                selectedFilters.includes(filter.id) ? styles.selected : ""
              }`}
              onClick={() => toggleFilter(filter.id)}
            >
              {filter.label}
            </button>
          ))}
        </div>

        <div className={styles.secondaryFilters}>
          {secondaryFilters.map((filter) => (
            <button
              key={filter.id}
              className={`${styles.secondaryFilterTag} ${
                selectedFilters.includes(filter.id) ? styles.selected : ""
              }`}
              onClick={() => toggleFilter(filter.id)}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.jobListHeader}>
        <div className={styles.sortOptions}>
          <button className={styles.sortButton}>
            Relevance <span className={styles.dropdownArrow}>▼</span>
          </button>
          <button className={styles.sortButton}>
            3 months <span className={styles.dropdownArrow}>▼</span>
          </button>
          <button className={styles.sortButton}>
            All apply forms <span className={styles.dropdownArrow}>▼</span>
          </button>
          <button className={styles.sortButton}>
            Show all jobs <span className={styles.dropdownArrow}>▼</span>
          </button>
        </div>

        <div className={styles.communityButtons}>
          <button className={styles.communityButton}>
            Join our community <span className={styles.badge}>9</span>
          </button>
          <button className={styles.talentButton}>Talent Network</button>
        </div>
      </div>

      <div className={styles.jobCount}>
        2,020,723 jobs · 70,695 companies · Latest jobs in United States
      </div>

      <div className={styles.jobList}>
        {jobs.map((job) => (
          <div key={job.id} className={styles.jobCard}>
            <div className={styles.jobHeader}>
              <div className={styles.jobTitle}>{job.title}</div>
              <div className={styles.jobTime}>{job.timePosted}</div>
            </div>

            <div className={styles.jobLocation}>
              <span className={styles.locationDot}>📍</span> {job.location}
            </div>

            <div className={styles.jobDetails}>
              <span className={styles.jobType}>{job.type}</span>
              {job.salary && (
                <span className={styles.jobSalary}>{job.salary}</span>
              )}
            </div>

            <div className={styles.jobCompany}>
              <strong>{job.company}</strong>
            </div>

            <div className={styles.jobActions}>
              <button className={styles.viewButton}>See views</button>
              <button className={styles.viewAllButton}>View all</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
