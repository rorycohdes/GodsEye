"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface CompanySkeletonCardProps {
  featureCount?: number;
}

export function CompanySkeletonCard({}: CompanySkeletonCardProps) {
  return (
    <Card className="bg-card/80 border-border/50">
      <CardContent className="p-6 flex flex-col">
        {/* Header skeleton */}
        <div className="flex items-center gap-3 mb-4">
          <Skeleton className="w-10 h-10 rounded-lg" />
          <Skeleton className="h-5 w-32" />
        </div>

        {/* Content skeleton */}
        <div>
          <Skeleton className="h-3 w-24 mb-2" />
          <div className="space-y-2">
            <Skeleton className="h-3 w-full" />
            <Skeleton className="h-3 w-4/5" />
            <Skeleton className="h-3 w-3/5" />
          </div>
        </div>

        {/* Footer skeleton */}
        <div className="pt-4 border-t border-border/50">
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
