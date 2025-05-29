"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface CompanySkeletonCardProps {
  variant?: "small" | "medium" | "large";
}

export function CompanySkeletonCard({
  variant = "medium",
}: CompanySkeletonCardProps) {
  // Different content amounts based on variant
  const getSkeletonContent = () => {
    switch (variant) {
      case "small":
        return {
          pitchLines: 2,
          features: 3,
        };
      case "large":
        return {
          pitchLines: 4,
          features: 7,
        };
      default: // medium
        return {
          pitchLines: 3,
          features: 5,
        };
    }
  };

  const { pitchLines, features } = getSkeletonContent();

  return (
    <Card className="bg-card/80 border-border/50">
      <CardContent className="p-6 flex flex-col">
        {/* Header skeleton */}
        <div className="flex items-center gap-3 mb-4">
          <Skeleton className="w-10 h-10 rounded-lg" />
          <Skeleton className="h-5 w-32" />
        </div>

        {/* Pitch section skeleton */}
        <div className="mb-4">
          <Skeleton className="h-3 w-24 mb-2" />
          <div className="space-y-2">
            {Array.from({ length: pitchLines }, (_, index) => (
              <Skeleton
                key={index}
                className={`h-3 ${
                  index === pitchLines - 1
                    ? "w-3/5"
                    : index % 2 === 0
                    ? "w-full"
                    : "w-4/5"
                }`}
              />
            ))}
          </div>
        </div>

        {/* Features section skeleton */}
        <div>
          <Skeleton className="h-3 w-32 mb-3" />
          <div className="space-y-1">
            {Array.from({ length: features }, (_, index) => (
              <div key={index} className="px-3 py-2 rounded-md">
                <Skeleton
                  className={`h-3 ${
                    index % 3 === 0
                      ? "w-4/5"
                      : index % 3 === 1
                      ? "w-3/5"
                      : "w-full"
                  }`}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Footer skeleton */}
        <div className="pt-4 border-t border-border/50 mt-4">
          <div className="flex items-center justify-between">
            <Skeleton className="h-3 w-8" />
            <div className="flex items-center gap-2">
              <Skeleton className="h-3 w-3" />
              <div className="flex items-center gap-1">
                {Array.from({ length: 2 }, (_, index) => (
                  <Skeleton key={index} className="w-1.5 h-1.5 rounded-full" />
                ))}
              </div>
              <Skeleton className="h-3 w-3" />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
