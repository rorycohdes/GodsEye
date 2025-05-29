"use client";

import { Card, CardContent } from "@/components/ui/card";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useState } from "react";

interface CompanyCardProps {
  company: {
    id: number;
    name: string;
    logo?: string;
    pitch: string;
    features: string[];
    problem?: string;
  };
}

export function CompanyCard({ company }: CompanyCardProps) {
  const [currentView, setCurrentView] = useState(0);
  const totalViews = 2; // Only two views now

  const handlePrevView = () => {
    setCurrentView((prev) => (prev > 0 ? prev - 1 : totalViews - 1));
  };

  const handleNextView = () => {
    setCurrentView((prev) => (prev < totalViews - 1 ? prev + 1 : 0));
  };

  const handleDotClick = (index: number) => {
    setCurrentView(index);
  };

  return (
    <Card className="bg-card/80 border-border/50 hover:bg-card/90 transition-colors duration-200">
      <CardContent className="p-6 flex flex-col">
        {/* Header with logo and company name - always visible */}
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-muted rounded-lg flex items-center justify-center overflow-hidden">
            {company.logo ? (
              <Image
                src={company.logo || "/placeholder.svg"}
                alt={`${company.name} logo`}
                width={40}
                height={40}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-8 h-8 bg-primary/20 rounded flex items-center justify-center">
                <span className="text-primary font-semibold text-sm">
                  {company.name.charAt(0)}
                </span>
              </div>
            )}
          </div>
          <h3 className="font-semibold text-foreground text-lg">
            {company.name}
          </h3>
        </div>

        {/* View 1: Pitch and Features */}
        {currentView === 0 && (
          <>
            {/* Pitch section */}
            <div className="mb-4">
              <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
                Pitch
              </div>
              <p className="text-sm text-foreground/80 leading-relaxed">
                {company.pitch}
              </p>
            </div>

            {/* Feature Summary section */}
            <div>
              <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">
                Feature Summary
              </div>
              <div className="space-y-1">
                {company.features.map((feature, index) => (
                  <div
                    key={index}
                    className="px-3 py-2 rounded-md text-sm text-foreground/90 hover:bg-muted/50 hover:border hover:border-border transition-all duration-150 cursor-default break-words"
                  >
                    {feature}
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {/* View 2: Problem/Background */}
        {currentView === 1 && (
          <div>
            <div className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
              Problem / Background
            </div>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {company.problem ||
                "This company addresses significant challenges in their industry through innovative solutions and strategic approaches to market problems."}
            </p>
          </div>
        )}

        {/* Footer with views navigation */}
        <div className="pt-4 border-t border-border/50">
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground font-medium">
              views
            </span>

            <div className="flex items-center gap-2">
              <button
                onClick={handlePrevView}
                className="p-1 hover:bg-muted/50 rounded transition-colors duration-150"
              >
                <ChevronLeft className="h-3 w-3 text-muted-foreground" />
              </button>

              <div className="flex items-center gap-1">
                {Array.from({ length: totalViews }, (_, index) => (
                  <button
                    key={index}
                    onClick={() => handleDotClick(index)}
                    className={`rounded-full transition-all duration-200 ${
                      index === currentView
                        ? "w-2.5 h-2.5 bg-foreground"
                        : "w-1.5 h-1.5 bg-muted-foreground/50 hover:bg-muted-foreground/70"
                    }`}
                  />
                ))}
              </div>

              <button
                onClick={handleNextView}
                className="p-1 hover:bg-muted/50 rounded transition-colors duration-150"
              >
                <ChevronRight className="h-3 w-3 text-muted-foreground" />
              </button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
