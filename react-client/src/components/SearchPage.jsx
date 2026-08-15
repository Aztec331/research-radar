import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { getPapers } from "../api/papers";

const TOPICS = ["All Topics", "NLP", "Computer Vision"];
const YEARS = ["All Years", 2026, 2025, 2024, 2023, 2022];

//Actual Component--------------------------------------------------------------------
export default function SearchPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const page = Number(searchParams.get("page")) || 1;
  const query = searchParams.get("q") || "";
  const topic = searchParams.get("topic") || "All Topics";
  const year = searchParams.get("year") || "All Years";
  const authorQuery = searchParams.get("author") || "";


  const [papers, setPapers] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [debouncedAuthor, setDebouncedAuthor] = useState("");

  function updateParams(changes) {
  const next = new URLSearchParams(searchParams);

  Object.entries(changes).forEach(([key, value]) => {
    if (
      value &&
      value !== "All Topics" &&
      value !== "All Years"
    ) {
      next.set(key, value);
    } else {
      next.delete(key);
    }
  });

  setSearchParams(next);
}


useEffect(() => {
  const timer = setTimeout(() => {
    setDebouncedQuery(query);
  }, 300);

  return () => clearTimeout(timer);
}, [query]);

useEffect(() => {
  const timer = setTimeout(() => {
    setDebouncedAuthor(authorQuery);
  }, 300);

  return () => clearTimeout(timer);
}, [authorQuery]);

useEffect(() => {
  let cancelled = false;

  async function fetchPapers() {
    setLoading(true);
    setError(null);

    try {
      const response = await getPapers({
        search: debouncedQuery.trim() || undefined,
        topic: topic === "All Topics" ? undefined : topic,
        year: year === "All Years" ? undefined : Number(year),
        author: debouncedAuthor.trim() || undefined,
        page,
        limit: 4,
      });

      if (cancelled) {
        return;
      }

      setPapers(response.data.items);
      setTotal(response.data.total);
    } catch (error) {
      if (cancelled) {
        return;
      }

      console.error("Failed to fetch papers:", error);
      setError("Couldn't load papers. Try again.");
    } finally {
      if (!cancelled) {
        setLoading(false);
      }
    }
  }

  fetchPapers();

  return () => {
    cancelled = true;
  };
}, [debouncedQuery, topic, year, debouncedAuthor, page]);


  const hasActiveFilters =
    topic !== "All Topics" || year !== "All Years" || authorQuery || query;

  const totalPages = Math.max(1, Math.ceil(total / 4));
  const currentPage = page;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">

      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-slate-200 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-4">

          <button
          onClick={() => navigate("/")}
          className="text-xl font-semibold"
          >
          Research Radar
          </button>

          <p className="text-sm text-slate-500">Search recent papers</p>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="max-w-5xl mx-auto px-4 py-6">

        {/* Search box */}
        <div className="mb-4">
          <input
            type="text"
            value={query}
            onChange={(e) => {
            updateParams({
            q: e.target.value,
            page: "1",
            });
            }}
            placeholder="Search by title or abstract..."
            className="w-full rounded-md border border-slate-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3 mb-6">

          <select
            value={topic}
            onChange={(e) => {
            updateParams({
            topic: e.target.value,
            page: "1",
            });
            }}
            className="rounded-md border border-slate-300 px-3 py-1.5 text-sm bg-white"
          >
            {TOPICS.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>

          <select
            value={year}
            onChange={(e) => {
            updateParams({
            year: e.target.value,
            page: "1",
            });
            }}
            className="rounded-md border border-slate-300 px-3 py-1.5 text-sm bg-white"
          >
            {YEARS.map((y) => <option key={y} value={y}>{y}</option>)}
          </select>

          {/* Author: text search instead of dropdown - too many distinct values for a select */}
          <input
            type="text"
            value={authorQuery}
            onChange={(e) => {
            updateParams({
            author: e.target.value,
            page: "1",
            });
            }}
            placeholder="Filter by author..."
            className="rounded-md border border-slate-300 px-3 py-1.5 text-sm bg-white w-48"
          />

          {hasActiveFilters && (
            <button
              onClick={() => setSearchParams({})}
              className="text-sm text-slate-500 underline px-2"
            >
              Clear filters
            </button>
          )}
        </div>

        {/* Result count */}
        <p className="text-sm text-slate-500 mb-3">
          {total} paper{total !== 1 ? "s" : ""} found
        </p>

        {/* Results list */}
        {error ? (
          <div className="text-center py-16 border border-dashed border-red-200 rounded-md">
            <p className="text-sm text-red-500">{error}</p>
          </div>
        ) : loading && papers.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-sm text-slate-400">Loading papers...</p>
          </div>
        ) : papers.length === 0 ? (
          <div className="text-center py-16 border border-dashed border-slate-300 rounded-md">
            <p className="text-slate-500">No papers match your search.</p>
            <p className="text-sm text-slate-400 mt-1">
              Try adjusting your filters.
            </p>
          </div>
        ) : (
          <ul
            className={`space-y-3 transition-opacity duration-150 ${
              loading ? "opacity-50" : "opacity-100"
            }`}
          >
            {papers.map((paper) => (
              <li
                key={paper.id}
                onClick={() => navigate(`/papers/${paper.id}`)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    navigate(`/papers/${paper.id}`);
                  }
                }}
                role="button"
                tabIndex={0}
                className="border border-slate-200 bg-white rounded-md p-4 hover:border-slate-400 transition-colors cursor-pointer"
              >
                <h2 className="font-medium text-slate-900">{paper.title}</h2>

                <p className="text-sm text-slate-600 mt-1 line-clamp-2">
                  {paper.abstract || "No abstract available."}
                </p>

                <div className="flex flex-wrap gap-2 mt-3 text-xs text-slate-500">
                  <span className="px-2 py-0.5 bg-slate-100 rounded">
                    {paper.topics?.[0]?.name || "Unknown topic"}
                  </span>

                  <span className="px-2 py-0.5 bg-slate-100 rounded">
                    {paper.year || "Unknown year"}
                  </span>

                  <span>
                    {paper.authors?.map((author) => author.name).join(", ")}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-center gap-2 mt-6">
            <button
              onClick={() =>
              updateParams({ page: String(Math.max(1, page - 1)) })
              }
              disabled={currentPage === 1}
              className="px-3 py-1.5 text-sm rounded-md border border-slate-300 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="text-sm text-slate-500">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() =>
              updateParams({ page: String(Math.min(totalPages, page + 1)) })
              }
              disabled={currentPage === totalPages}
              className="px-3 py-1.5 text-sm rounded-md border border-slate-300 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        )}
      </main>

    </div>
  );
}