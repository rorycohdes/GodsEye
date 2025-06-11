"use client";

import { CompanyCard } from "@/components/company-card";
import { CompanySkeletonCard } from "@/components/company-skeleton-card";
import { useEffect, useState } from "react";

// Interface for API response
interface ApiCompany {
  id: string;
  company_name?: string;
  location?: string;
  url?: string;
  created_at?: string;
  contents: string;
}

interface ApiResponse {
  data?: ApiCompany[];
  timestamp?: number;
  error?: string;
}

// Interface for frontend company card - must match CompanyCard props
interface Company {
  id: number;
  name: string;
  pitch: string;
  features: string[];
  problem: string;
}

// Function to transform API data to frontend format
const transformApiCompany = (
  apiCompany: ApiCompany,
  index: number
): Company => {
  // Extract features from contents - look for common patterns
  const extractFeatures = (contents: string): string[] => {
    const features: string[] = [];

    // Look for tag-based features
    const tagMatch = contents.match(/Tags: (.+?)(?:\.|$)/);
    if (tagMatch) {
      const tags = tagMatch[1].split(", ").map((tag) => tag.trim());
      features.push(...tags.map((tag) => `${tag} - Industry focus`));
    }

    // If no specific features found, create generic ones
    if (features.length === 0) {
      features.push(
        "Innovative Technology",
        "Market Leadership",
        "Growth Focus"
      );
    }

    return features.slice(0, 6); // Limit to 6 features
  };

  // Extract or generate problem statement
  const generateProblem = (name: string, contents: string): string => {
    // Try to extract description for problem context
    const descMatch = contents.match(
      /Description: (.+?)(?:\.|(?:Tags:|Location:|$))/
    );
    const description = descMatch ? descMatch[1].trim() : "";

    if (description) {
      return `${name} identified market challenges that required ${description.toLowerCase()}. They recognized the opportunity to innovate and provide solutions that address these critical industry needs.`;
    }

    return `${name} identified significant market opportunities and challenges in their industry. They developed innovative solutions to address these needs and create value for their target market.`;
  };

  // Extract or generate pitch
  const generatePitch = (name: string, contents: string): string => {
    const descMatch = contents.match(
      /Description: (.+?)(?:\.|(?:Tags:|Location:|$))/
    );
    if (descMatch) {
      return descMatch[1].trim();
    }

    return `${name} is an innovative company focused on delivering cutting-edge solutions and exceptional value to their customers through advanced technology and strategic market positioning.`;
  };

  return {
    id: 1000 + index, // Use numeric IDs starting from 1000 for API companies
    name: apiCompany.company_name || `Company ${index + 1}`,
    pitch: generatePitch(
      apiCompany.company_name || `Company ${index + 1}`,
      apiCompany.contents
    ),
    features: extractFeatures(apiCompany.contents),
    problem: generateProblem(
      apiCompany.company_name || `Company ${index + 1}`,
      apiCompany.contents
    ),
  };
};

// Keep a few predefined companies as requested
const predefinedCompanies: Company[] = [
  {
    id: 1,
    name: "Apple",
    pitch:
      "Apple designs and manufactures consumer electronics, software, and online services. Known for innovative products that seamlessly integrate hardware and software.",
    features: [
      "iPhone - Revolutionary smartphone",
      "MacBook - Premium laptops",
      "iPad - Tablet computing",
      "Apple Watch - Wearable technology",
      "AirPods - Wireless audio",
      "iOS/macOS - Operating systems",
    ],
    problem:
      "Before Apple's innovations, personal computing was fragmented with poor user experiences. Mobile phones were primarily for calls, and digital music was plagued by piracy. Apple identified the need for intuitive, beautifully designed technology that seamlessly integrates hardware and software to create magical user experiences.",
  },
  {
    id: 2,
    name: "Google",
    pitch:
      "Google organizes the world's information and makes it universally accessible. Leading in search, advertising, cloud computing, and artificial intelligence.",
    features: [
      "Search Engine - Web search",
      "Google Cloud - Cloud computing",
      "Android - Mobile OS",
      "YouTube - Video platform",
      "Gmail - Email service",
    ],
    problem:
      "In the early internet era, finding relevant information was extremely difficult with existing search engines providing poor, spam-filled results. The web was growing exponentially but lacked an effective way to organize and retrieve information, creating a massive barrier to knowledge access.",
  },
  {
    id: 3,
    name: "Tesla",
    pitch:
      "Tesla accelerates the world's transition to sustainable energy through electric vehicles, energy storage, and solar panel manufacturing.",
    features: [
      "Model S/3/X/Y - Electric vehicles",
      "Supercharger - Charging network",
      "Autopilot - Self-driving tech",
      "Solar Roof - Solar energy",
      "Powerwall - Energy storage",
    ],
    problem:
      "The automotive industry was heavily dependent on fossil fuels, contributing to climate change and air pollution. Electric vehicles were seen as impractical with limited range, poor performance, and lack of charging infrastructure. Tesla aimed to prove that electric vehicles could be superior to gasoline cars.",
  },
];

export default function MasonryPage() {
  const [apiCompanies, setApiCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  // Fetch companies from the real-time API
  const fetchCompanies = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/realtime/latest?limit=15"
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ApiResponse = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      // Transform API data to frontend format
      const transformedCompanies =
        data.data?.map((apiCompany, index) =>
          transformApiCompany(apiCompany, index)
        ) || [];

      setApiCompanies(transformedCompanies);
      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      console.error("Error fetching companies:", err);
      setError(
        err instanceof Error ? err.message : "Failed to fetch companies"
      );
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchCompanies();

    // Set up periodic refresh every 30 seconds
    const interval = setInterval(fetchCompanies, 30000);

    return () => clearInterval(interval);
  }, []);

  // Combine predefined and API companies
  const allCompanies = [...predefinedCompanies, ...apiCompanies];

  // Generate skeleton cards with different variants for varied heights
  const skeletonCards = [
    { id: "skeleton-0", variant: "medium" as const },
    { id: "skeleton-1", variant: "large" as const },
    { id: "skeleton-2", variant: "small" as const },
    { id: "skeleton-3", variant: "medium" as const },
    { id: "skeleton-4", variant: "large" as const },
    { id: "skeleton-5", variant: "small" as const },
  ];

  return (
    <div className="dark min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            Company Showcase
          </h1>
          <p className="text-muted-foreground text-lg mb-4">
            Explore leading technology companies and their key features
          </p>

          {/* Status indicator */}
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  error
                    ? "bg-red-500"
                    : loading
                    ? "bg-yellow-500"
                    : "bg-green-500"
                }`}
              ></div>
              <span>
                {error
                  ? "Connection Error"
                  : loading
                  ? "Loading..."
                  : "Live Data Connected"}
              </span>
            </div>
            {lastUpdated && (
              <span>Last updated: {lastUpdated.toLocaleTimeString()}</span>
            )}
            <button
              onClick={fetchCompanies}
              disabled={loading}
              className="text-blue-400 hover:text-blue-300 underline disabled:opacity-50"
            >
              Refresh
            </button>
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-200">
              <p className="font-medium">Error fetching live data:</p>
              <p className="text-sm">{error}</p>
              <p className="text-xs mt-1">
                Showing predefined companies only. Make sure the backend is
                running on http://localhost:8000
              </p>
            </div>
          )}
        </div>

        {/* Masonry Grid */}
        <div className="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-6 space-y-0">
          {/* Company Cards */}
          {allCompanies.map((company) => (
            <div
              key={company.id}
              className={`break-inside-avoid mb-6 ${
                company.id >= 1000 ? "ring-1 ring-blue-500/30 rounded-lg" : ""
              }`}
            >
              <CompanyCard company={company} />
            </div>
          ))}

          {/* Skeleton Cards - only show while loading initial data */}
          {loading &&
            skeletonCards.map((skeleton) => (
              <div key={skeleton.id} className="break-inside-avoid mb-6">
                <CompanySkeletonCard variant={skeleton.variant} />
              </div>
            ))}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <p className="text-muted-foreground">
            Showing {predefinedCompanies.length} featured companies,{" "}
            {apiCompanies.length} live companies
            {loading && `, and ${skeletonCards.length} loading placeholders`}
          </p>
          <p className="text-xs text-muted-foreground mt-2">
            🔵 Blue ring indicates live scraped data from YCombinator
          </p>
        </div>
      </div>
    </div>
  );
}
