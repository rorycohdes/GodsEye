"use client";

import { CompanyCard } from "@/components/company-card";
import { CompanySkeletonCard } from "@/components/company-skeleton-card";

// Big tech companies data with problem/background
const companies = [
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
    name: "Microsoft",
    pitch:
      "Microsoft develops, licenses, and supports software, services, devices and solutions worldwide. Empowering every person and organization to achieve more.",
    features: [
      "Windows - Operating system",
      "Office 365 - Productivity suite",
      "Azure - Cloud platform",
      "Teams - Collaboration tools",
      "Xbox - Gaming platform",
      "LinkedIn - Professional network",
      "GitHub - Developer platform",
      "Visual Studio - Development tools",
    ],
    problem:
      "Personal computers in the 1970s and 80s were complex, expensive, and required technical expertise. Business productivity was limited by incompatible software systems and lack of standardization. Microsoft saw the opportunity to democratize computing by creating accessible software platforms.",
  },
  {
    id: 4,
    name: "Amazon",
    pitch:
      "Amazon is a multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence.",
    features: [
      "Prime - Subscription service",
      "AWS - Cloud computing",
      "Alexa - Voice assistant",
      "Kindle - E-reader platform",
    ],
    problem:
      "Traditional retail was limited by physical constraints, inventory costs, and geographic reach. Businesses struggled with expensive IT infrastructure and complex server management. Amazon recognized the potential of the internet to revolutionize commerce and computing infrastructure.",
  },
  {
    id: 5,
    name: "Meta",
    pitch:
      "Meta builds technologies that help people connect, find communities, and grow businesses through social media and virtual reality platforms.",
    features: [
      "Facebook - Social network",
      "Instagram - Photo sharing",
      "WhatsApp - Messaging",
      "Messenger - Chat platform",
      "Meta Quest - VR headsets",
      "Threads - Text-based social",
    ],
    problem:
      "Before social media, staying connected with friends and family across distances was difficult and expensive. People lacked platforms to share experiences, build communities, and maintain relationships. Traditional communication methods were fragmented and limited in reach.",
  },
  {
    id: 6,
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
  {
    id: 7,
    name: "Netflix",
    pitch:
      "Netflix is a streaming entertainment service with over 230 million paid memberships in more than 190 countries enjoying TV series, films and games.",
    features: [
      "Streaming Platform - Video content",
      "Original Content - Netflix Originals",
      "Global Reach - 190+ countries",
      "Personalization - AI recommendations",
    ],
    problem:
      "Traditional entertainment distribution was controlled by cable companies and movie theaters, limiting consumer choice and convenience. People were frustrated with scheduled programming, late fees from video rentals, and limited content selection. The industry needed disruption through on-demand access.",
  },
  {
    id: 8,
    name: "Spotify",
    pitch:
      "Spotify is a digital music, podcast, and video service that gives you access to millions of songs and other content from creators all over the world.",
    features: [
      "Music Streaming - 100M+ songs",
      "Podcasts - Audio content",
      "Playlists - Curated music",
      "Spotify Connect - Multi-device",
      "Artist Tools - Creator platform",
    ],
    problem:
      "The music industry was struggling with piracy and declining CD sales. Consumers wanted convenient access to vast music libraries without purchasing individual albums. Artists needed better ways to reach audiences and monetize their content in the digital age.",
  },
];

export default function MasonryPage() {
  // Generate skeleton cards with predefined feature counts to avoid hydration issues
  const skeletonCards = [
    { id: "skeleton-0", featureCount: 4 },
    { id: "skeleton-1", featureCount: 6 },
    { id: "skeleton-2", featureCount: 3 },
    { id: "skeleton-3", featureCount: 5 },
    { id: "skeleton-4", featureCount: 4 },
    { id: "skeleton-5", featureCount: 7 },
  ];

  return (
    <div className="dark min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            Company Showcase
          </h1>
          <p className="text-muted-foreground text-lg">
            Explore leading technology companies and their key features
          </p>
        </div>

        {/* Masonry Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 auto-rows-[80px]">
          {/* Company Cards */}
          {companies.map((company) => (
            <CompanyCard key={company.id} company={company} />
          ))}

          {/* Skeleton Cards */}
          {skeletonCards.map((skeleton) => (
            <CompanySkeletonCard
              key={skeleton.id}
              featureCount={skeleton.featureCount}
            />
          ))}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <p className="text-muted-foreground">
            Showing {companies.length} companies and {skeletonCards.length}{" "}
            loading placeholders
          </p>
        </div>
      </div>
    </div>
  );
}
