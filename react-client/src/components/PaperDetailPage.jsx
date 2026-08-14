import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

// ---- Dummy data (replace with GET /papers/{id} + similar papers API call) ----
const DUMMY_PAPERS = [
  { id: 1, title: "Attention Is All You Need: A Retrospective on Transformer Architectures", abstract: "We revisit the transformer architecture and analyze its impact on modern NLP and vision systems, five years after its introduction. This paper surveys the key innovations that made transformers the dominant architecture across both language and vision tasks, and discusses open challenges in scaling and efficiency.", year: 2024, topic: "NLP", authors: ["A. Vaswani", "N. Shazeer"] },
  { id: 2, title: "Self-Supervised Contrastive Learning for Medical Image Segmentation", abstract: "A contrastive pretraining approach that improves segmentation accuracy on low-label medical imaging datasets.", year: 2025, topic: "Computer Vision", authors: ["R. Chen", "M. Patel"] },
  { id: 3, title: "Efficient Fine-Tuning of Large Language Models via Low-Rank Adaptation", abstract: "LoRA reduces trainable parameters by two orders of magnitude while matching full fine-tuning performance on downstream tasks.", year: 2023, topic: "NLP", authors: ["E. Hu", "Y. Shen"] },
  { id: 4, title: "Zero-Shot Object Detection with Vision-Language Models", abstract: "We show that CLIP-style embeddings can be repurposed for open-vocabulary detection without task-specific training.", year: 2024, topic: "Computer Vision", authors: ["L. Zhang", "S. Kumar"] },
  { id: 5, title: "Retrieval-Augmented Generation for Domain-Specific Question Answering", abstract: "Combining dense retrieval with generative models improves factual accuracy on closed-domain QA benchmarks.", year: 2025, topic: "NLP", authors: ["J. Lewis", "P. Singh"] },
  { id: 7, title: "Instruction Tuning at Scale: Lessons from Multi-Task Datasets", abstract: "We analyze how dataset diversity affects instruction-following behavior across 400 fine-tuned model checkpoints.", year: 2024, topic: "NLP", authors: ["M. Patel", "N. Shazeer"] },
  { id: 9, title: "Chain-of-Thought Prompting for Better Reasoning in Language Models", abstract: "We show that step-by-step prompting improves performance on multi-step reasoning benchmarks across diverse tasks.", year: 2025, topic: "NLP", authors: ["D. Wang", "K. Rao"] },
  { id: 13, title: "Sparse Attention Mechanisms for Long-Context Language Modeling", abstract: "We explore sparse attention patterns that reduce memory cost while preserving generation quality for long sequences.", year: 2025, topic: "NLP", authors: ["N. Gupta", "M. Flores"] },
];

const DUMMY_SIMILAR = [
  { id: 3, title: "Efficient Fine-Tuning of Large Language Models via Low-Rank Adaptation" },
  { id: 5, title: "Retrieval-Augmented Generation for Domain-Specific Question Answering" },
  { id: 7, title: "Instruction Tuning at Scale: Lessons from Multi-Task Datasets" },
  { id: 9, title: "Chain-of-Thought Prompting for Better Reasoning in Language Models" },
  { id: 13, title: "Sparse Attention Mechanisms for Long-Context Language Modeling" },
];

export default function PaperDetailPage() {
  const { paperId } = useParams();
  const navigate = useNavigate();
  const paper = DUMMY_PAPERS.find((item) => item.id === Number(paperId)) ?? DUMMY_PAPERS[0];
  const [showSimilar, setShowSimilar] = useState(false);
  const [loadingSimilar, setLoadingSimilar] = useState(false);

  function handleFindSimilar() {
    if (showSimilar) {
      setShowSimilar(false);
      return;
    }

    setLoadingSimilar(true);
    setTimeout(() => {
      setLoadingSimilar(false);
      setShowSimilar(true);
    }, 500);
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <h1 className="text-xl font-semibold">Research Radar</h1>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6">
        <button onClick={() => navigate("/")} className="text-sm text-slate-500 hover:text-slate-800 mb-4 inline-flex items-center gap-1">
          ← Back to search
        </button>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 bg-white border border-slate-200 rounded-md p-6">
            <div className="flex flex-wrap gap-2 mb-3 text-xs text-slate-500">
              <span className="px-2 py-0.5 bg-slate-100 rounded">{paper.topic}</span>
              <span className="px-2 py-0.5 bg-slate-100 rounded">{paper.year}</span>
            </div>
            <h2 className="text-2xl font-semibold text-slate-900 mb-3">{paper.title}</h2>
            <p className="text-sm text-slate-500 mb-4">{paper.authors.join(", ")}</p>
            <h3 className="text-sm font-medium text-slate-700 mb-1">Abstract</h3>
            <p className="text-sm text-slate-600 leading-relaxed">{paper.abstract}</p>
          </div>

          <div className="md:col-span-1">
            <div className="bg-white border border-slate-200 rounded-md p-4 sticky top-6">
              <h3 className="text-sm font-medium text-slate-700 mb-3">Similar Papers</h3>
              <button onClick={handleFindSimilar} disabled={loadingSimilar} className="w-full rounded-md bg-slate-900 text-white text-sm px-4 py-2 hover:bg-slate-700 transition-colors disabled:opacity-50">
                {loadingSimilar ? "Finding similar papers..." : showSimilar ? "Hide similar papers" : "Find similar papers"}
              </button>
              {showSimilar && (
                <ul className="mt-4 space-y-2">
                  {DUMMY_SIMILAR.map((similarPaper) => (
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
