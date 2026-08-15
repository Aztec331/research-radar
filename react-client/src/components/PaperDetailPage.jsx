import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getPaperById, getSimilarPapers } from "../api/papers";


export default function PaperDetailPage() {
  const { paperId } = useParams();
  const navigate = useNavigate();

  const [paper, setPaper] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [showSimilar, setShowSimilar] = useState(false);
  const [loadingSimilar, setLoadingSimilar] = useState(false);
  const [similarPapers, setSimilarPapers] = useState([]);
  const [similarError, setSimilarError] = useState(null);

//Effect- Get a single paper by its ID
  useEffect(() => {
  let cancelled = false;

  async function fetchPaper() {
    setLoading(true);
    setError(null);

    try {
      const response = await getPaperById(paperId);

      if (cancelled) {
        return;
      }

      setPaper(response.data);
    } catch (error) {
      if (cancelled) {
        return;
      }

      console.error("Failed to fetch paper:", error);
      setError(
        error.response?.data?.detail || "Couldn't load paper. Try again."
      );
    } finally {
      if (!cancelled) {
        setLoading(false);
      }
    }
  }

  fetchPaper();

  return () => {
    cancelled = true;
  };
}, [paperId]);


//Effect- Reset similar papers state when paperId changes
useEffect(() => {
  setShowSimilar(false);
  setSimilarPapers([]);
  setSimilarError(null);
  setLoadingSimilar(false);
}, [paperId]);



  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 text-slate-900">
        <main className="max-w-5xl mx-auto px-4 py-16 text-center">
          <p className="text-sm text-slate-400">Loading paper...</p>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 text-slate-900">
        <main className="max-w-5xl mx-auto px-4 py-16 text-center">
          <p className="text-sm text-red-500">{error}</p>

          <button
            onClick={() => navigate("/")}
            className="mt-4 text-sm text-slate-500 hover:text-slate-800 underline"
          >
            Back to search
          </button>
        </main>
      </div>
    );
  }

//Function to handle finding similar papers
  async function handleFindSimilar() {
  if (showSimilar) {
    setShowSimilar(false);
    setSimilarError(null);
    return;
  }

  setLoadingSimilar(true);
  setSimilarError(null);

  try {
    const response = await getSimilarPapers(paperId);

    setSimilarPapers(response.data);
    setShowSimilar(true);
  } catch (error) {
    console.error("Failed to fetch similar papers:", error);
    setSimilarError("Couldn't find similar papers. Try again.");
  } finally {
    setLoadingSimilar(false);
  }
}

  return (

    // Whole page container with a light background and dark text
    <div className="min-h-screen bg-slate-50 text-slate-900">

      {/* Header Section */}
      <header className="sticky top-0 z-10 border-b border-slate-200 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-4">

        <button
          onClick={() => navigate("/")}
          className="text-xl font-semibold"
        >
          Research Radar
        </button>

        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6">
        <button onClick={() => navigate(-1)} className="text-sm text-slate-500 hover:text-slate-800 mb-4 inline-flex items-center gap-1">
          ← Back to page
        </button>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          {/* Main Content Section */}
          <div className="md:col-span-2 bg-white border border-slate-200 rounded-md p-6">
            <div className="flex flex-wrap gap-2 mb-3 text-xs text-slate-500">
              <span className="px-2 py-0.5 bg-slate-100 rounded">
              {paper.topics?.[0]?.name || "Unknown topic"}
              </span>
              <span className="px-2 py-0.5 bg-slate-100 rounded">{paper.year}</span>
            </div>
            <h2 className="text-2xl font-semibold text-slate-900 mb-3">{paper.title}</h2>
            <p className="text-sm text-slate-500 mb-4">
            {paper.authors?.map((author) => author.name).join(", ") || "Unknown authors"}
            </p>
            <h3 className="text-sm font-medium text-slate-700 mb-1">Abstract</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
            {paper.abstract || "No abstract available."}
            </p>
          </div>

          {/* Similar Papers Section */}
          <div className="md:col-span-1">
            <div className="bg-white border border-slate-200 rounded-md p-4 sticky top-20">

              <h3 className="text-sm font-medium text-slate-700 mb-3">Similar Papers</h3>

              <button onClick={handleFindSimilar} disabled={loadingSimilar} className="w-full rounded-md bg-slate-900 text-white text-sm px-4 py-2 hover:bg-slate-700 transition-colors disabled:opacity-50">
                {loadingSimilar ? "Finding similar papers..." : showSimilar ? "Hide similar papers" : "Find similar papers"}
              </button>

              {similarError && (
                <p className="text-xs text-red-500 mt-3">
                {similarError}
              </p>
              )}

              {showSimilar && (
                <ul className="mt-4 space-y-2">
                  {similarPapers.map((similarPaper) => (
                    <li key={similarPaper.id}>
                      <button onClick={() => navigate(`/papers/${similarPaper.id}`)} className="text-left text-sm text-slate-700 hover:text-slate-900 hover:underline w-full">
                        {similarPaper.title}
                      </button>
                    </li>
                  ))}
                </ul>
              )}

              {!showSimilar && !loadingSimilar && <p className="text-xs text-slate-400 mt-3">Click above to see 5 papers most similar to this one.</p>}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
