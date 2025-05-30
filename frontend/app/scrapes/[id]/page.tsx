interface PageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function CompanyDetailPage({ params }: PageProps) {
  const { id } = await params;

  return (
    <div className="dark min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-foreground mb-4">
            Hello World
          </h1>
          <p className="text-muted-foreground text-lg">Company ID: {id}</p>
        </div>
      </div>
    </div>
  );
}
