import React, { useState, useEffect } from 'react';
import { lucideReact as icons } from 'lucide-react';

const traits = [
  { code: 'NC', name: 'Non-Coercion', description: 'Avoiding manipulative or coercive actions.' },
  { code: 'DI', name: 'Dignity Preservation', description: 'Upholding the dignity of all individuals.' },
  { code: 'CS', name: 'Community Solidarity', description: 'Fostering transparent, fair community bonds.' },
  { code: 'TC', name: 'Task Completion', description: 'Efficiently fulfilling responsibilities with accountability.' },
];

const App = () => {
  const [dilemma, setDilemma] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleProcess = async () => {
    if (dilemma.trim() === '') {
      setError("Please enter an ethical dilemma to process.");
      return;
    }
    setError(null);
    setLoading(true);
    setResults(null);

    // Simulate API call and processing with a delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    try {
      // Mock the CoCorels processing logic
      const initialScores = {};
      traits.forEach(trait => {
        initialScores[trait.code] = Math.floor(Math.random() * 100) + 1; // Random score 1-100
      });

      // Mock conflict detection
      let conflicts = [];
      let updatedScores = { ...initialScores };
      
      // A mock conflict: High Task Completion (TC) vs. Low Non-Coercion (NC)
      if (initialScores.TC > 80 && initialScores.NC < 30) {
        conflicts.push("TC vs NC: High Task Completion seems to conflict with low Non-Coercion. Resolution is needed.");
        // Mock resolution: boost NC slightly and reduce TC slightly
        updatedScores.NC = Math.min(100, updatedScores.NC + 20);
        updatedScores.TC = Math.max(1, updatedScores.TC - 10);
      }
      
      // Another mock conflict: Low Dignity Preservation (DI) vs. High Community Solidarity (CS)
      if (initialScores.DI < 20 && initialScores.CS > 85) {
        conflicts.push("DI vs CS: Low Dignity Preservation conflicts with high Community Solidarity. Resolution is needed.");
        // Mock resolution: boost DI
        updatedScores.DI = Math.min(100, updatedScores.DI + 30);
      }

      // Mock final scores
      const mcdaScore = Object.values(updatedScores).reduce((sum, score) => sum + score, 0) / traits.length;
      const balanceScore = 1 - (Math.max(...Object.values(updatedScores)) - Math.min(...Object.values(updatedScores))) / 100;

      setResults({
        initialScores,
        updatedScores,
        conflicts,
        mcdaScore: mcdaScore.toFixed(2),
        balanceScore: balanceScore.toFixed(2),
      });

    } catch (e) {
      setError("An error occurred during processing.");
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const getBarColor = (score) => {
    if (score < 30) return 'bg-red-500';
    if (score < 60) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8 flex items-center justify-center font-sans">
      <div className="w-full max-w-3xl bg-gray-800 rounded-2xl shadow-2xl p-8 md:p-12 border border-gray-700">
        <div className="flex flex-col items-center text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-extrabold text-blue-400 mb-2">CoCorels</h1>
          <p className="text-xl text-gray-300">The Operationalization of Ethics</p>
        </div>

        <div className="space-y-6">
          <div>
            <label htmlFor="dilemma" className="block text-lg font-medium text-gray-200 mb-2">
              Enter an Ethical Dilemma
            </label>
            <textarea
              id="dilemma"
              rows="4"
              className="w-full p-4 bg-gray-700 rounded-lg border border-gray-600 focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400 text-gray-100 resize-none"
              placeholder="e.g., Should an AI prioritize safety or innovation in autonomous vehicle design?"
              value={dilemma}
              onChange={(e) => setDilemma(e.target.value)}
            />
          </div>

          {error && (
            <div className="bg-red-900 bg-opacity-30 text-red-300 p-4 rounded-lg flex items-center space-x-2">
              <icons.AlertCircle size={20} />
              <span>{error}</span>
            </div>
          )}

          <div className="flex justify-center">
            <button
              onClick={handleProcess}
              disabled={loading}
              className="w-full md:w-auto px-8 py-4 text-lg font-bold rounded-full text-white transition-all duration-300 transform bg-blue-600 hover:bg-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center space-x-2">
                  <icons.Loader2 size={24} className="animate-spin" />
                  <span>Processing...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <span>Process Dilemma</span>
                  <icons.ArrowRightCircle size={24} />
                </div>
              )}
            </button>
          </div>
        </div>

        {results && (
          <div className="mt-12 space-y-8 animate-fade-in">
            <h2 className="text-3xl font-bold text-gray-200 border-b border-gray-700 pb-4">Analysis Results</h2>

            <div>
              <h3 className="text-xl font-semibold text-gray-300 mb-4">Trait Scores</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {traits.map(trait => (
                  <div key={trait.code} className="bg-gray-700 p-5 rounded-xl shadow-inner border border-gray-600">
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-xl font-bold text-blue-400">{trait.code}</span>
                      <span className="text-sm text-gray-400">{trait.name}</span>
                    </div>
                    <p className="text-sm text-gray-300 mb-4">{trait.description}</p>
                    <div className="w-full bg-gray-600 rounded-full h-4">
                      <div
                        className={`h-4 rounded-full transition-all duration-700 ease-out ${getBarColor(results.updatedScores[trait.code])}`}
                        style={{ width: `${results.updatedScores[trait.code]}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-sm font-medium mt-1">
                      <span className="text-gray-400">Initial: {results.initialScores[trait.code]}</span>
                      <span className="text-gray-200 font-bold">Final: {results.updatedScores[trait.code]}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {results.conflicts.length > 0 && (
              <div className="bg-orange-900 bg-opacity-30 text-orange-300 p-6 rounded-xl border border-orange-700">
                <h3 className="text-xl font-semibold mb-3 flex items-center space-x-2">
                  <icons.AlertTriangle size={24} />
                  <span>Detected Conflicts & Resolutions</span>
                </h3>
                <ul className="list-disc list-inside space-y-2 text-sm">
                  {results.conflicts.map((conflict, index) => (
                    <li key={index}>{conflict}</li>
                  ))}
                </ul>
              </div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-purple-900 bg-opacity-30 p-6 rounded-xl border border-purple-700 flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-purple-300">Final MCDA Score</h3>
                  <p className="text-sm text-purple-400">Multi-Criteria Decision Analysis</p>
                </div>
                <span className="text-4xl font-bold text-white">{results.mcdaScore}</span>
              </div>
              <div className="bg-green-900 bg-opacity-30 p-6 rounded-xl border border-green-700 flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-green-300">System Balance Score</h3>
                  <p className="text-sm text-green-400">Harmony across all traits</p>
                </div>
                <span className="text-4xl font-bold text-white">{results.balanceScore}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
