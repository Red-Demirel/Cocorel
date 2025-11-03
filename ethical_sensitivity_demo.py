import React, { useState, useEffect } from 'react';
import { lucideReact as icons } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const traits = [
  { code: 'NC', name: 'Non-Coercion', description: 'Avoiding manipulative or coercive actions.' },
  { code: 'DI', name: 'Dignity Preservation', description: 'Upholding the dignity of all individuals.' },
  { code: 'CS', name: 'Community Solidarity', description: 'Fostering transparent, fair community bonds.' },
  { code: 'TC', name: 'Task Completion', description: 'Efficiently fulfilling responsibilities with accountability.' },
];

// Mock data to simulate conflicts based on a threshold
const mockConflictData = (initialScores, threshold) => {
  let conflicts = [];
  let updatedScores = { ...initialScores };
  let conflictDetected = false;

  const scoreDiff = (s1, s2) => Math.abs(s1 - s2);
  const conflictThreshold = (20000 - threshold) / 100; // Inverse relationship to make it intuitive

  if (scoreDiff(initialScores.TC, initialScores.NC) > conflictThreshold && initialScores.TC > 50) {
    conflicts.push(`TC (${initialScores.TC}) vs NC (${initialScores.NC}): High disparity detected. Resolution initiated.`);
    updatedScores.NC = Math.min(100, initialScores.NC + 20);
    updatedScores.TC = Math.max(1, initialScores.TC - 10);
    conflictDetected = true;
  }

  if (scoreDiff(initialScores.DI, initialScores.CS) > conflictThreshold && initialScores.DI < 50) {
    conflicts.push(`DI (${initialScores.DI}) vs CS (${initialScores.CS}): High disparity detected. Resolution initiated.`);
    updatedScores.DI = Math.min(100, initialScores.DI + 30);
    conflictDetected = true;
  }
  
  if (!conflictDetected && threshold < 8000) {
      // Add a fallback conflict for demonstration purposes if no other conflict is detected
      conflicts.push(`Minor Disparity Detected: A low complexity threshold of ${threshold} has identified a minor tension between traits. Resolution applied.`);
      const trait1 = traits[Math.floor(Math.random() * traits.length)].code;
      const trait2 = traits.find(t => t.code !== trait1).code;
      updatedScores[trait1] = Math.min(100, updatedScores[trait1] + 5);
      updatedScores[trait2] = Math.max(1, updatedScores[trait2] - 5);
  }

  return { conflicts, updatedScores };
};

const App = () => {
  const [dilemma, setDilemma] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [complexityThreshold, setComplexityThreshold] = useState(7000);

  const handleProcess = async () => {
    if (dilemma.trim() === '') {
      setError("Please enter an ethical dilemma to process.");
      return;
    }
    setError(null);
    setLoading(true);
    setResults(null);

    await new Promise(resolve => setTimeout(resolve, 1500));

    try {
      const initialScores = {};
      traits.forEach(trait => {
        initialScores[trait.code] = Math.floor(Math.random() * 100) + 1;
      });

      const { conflicts, updatedScores } = mockConflictData(initialScores, complexityThreshold);
      
      const mcdaScore = Object.values(updatedScores).reduce((sum, score) => sum + score, 0) / traits.length;
      const scoresArray = Object.values(updatedScores);
      const balanceScore = 1 - (Math.max(...scoresArray) - Math.min(...scoresArray)) / 100;

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

  const getSensitivityColor = (threshold) => {
    if (threshold > 12000) return 'text-red-400';
    if (threshold > 8000) return 'text-yellow-400';
    return 'text-green-400';
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8 flex items-center justify-center font-sans">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-3xl bg-gray-800 rounded-2xl shadow-2xl p-8 md:p-12 border border-gray-700"
      >
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
          
          <div className="flex flex-col md:flex-row md:items-center justify-between bg-gray-700 p-5 rounded-xl border border-gray-600">
            <div className="mb-4 md:mb-0">
              <h3 className="text-lg font-semibold text-gray-200">
                Conflict Sensitivity
              </h3>
              <p className="text-sm text-gray-400">
                Adjusting the `COMPLEXITY_THRESHOLD` to fit the domain's needs.
              </p>
            </div>
            <div className="flex-1 md:ml-6 flex items-center space-x-4">
              <input
                type="range"
                min="5000"
                max="15000"
                step="100"
                value={complexityThreshold}
                onChange={(e) => setComplexityThreshold(Number(e.target.value))}
                className="w-full h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer"
              />
              <span className={`text-lg font-bold w-20 text-right ${getSensitivityColor(complexityThreshold)}`}>
                {complexityThreshold}
              </span>
            </div>
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

        <AnimatePresence>
          {results && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className="mt-12 space-y-8 overflow-hidden"
            >
              <h2 className="text-3xl font-bold text-gray-200 border-b border-gray-700 pb-4">Analysis Results</h2>

              <div>
                <h3 className="text-xl font-semibold text-gray-300 mb-4">Trait Scores</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {traits.map(trait => (
                    <motion.div
                      key={trait.code}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.5, delay: 0.2 }}
                      className="bg-gray-700 p-5 rounded-xl shadow-inner border border-gray-600"
                    >
                      <div className="flex justify-between items-center mb-3">
                        <span className="text-xl font-bold text-blue-400">{trait.code}</span>
                        <span className="text-sm text-gray-400">{trait.name}</span>
                      </div>
                      <p className="text-sm text-gray-300 mb-4">{trait.description}</p>
                      <div className="w-full bg-gray-600 rounded-full h-4">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${results.updatedScores[trait.code]}%` }}
                          transition={{ duration: 1, ease: "easeOut" }}
                          className={`h-4 rounded-full ${getBarColor(results.updatedScores[trait.code])}`}
                        ></motion.div>
                      </div>
                      <div className="flex justify-between text-sm font-medium mt-1">
                        <span className="text-gray-400">Initial: {results.initialScores[trait.code]}</span>
                        <span className="text-gray-200 font-bold">Final: {results.updatedScores[trait.code]}</span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {results.conflicts.length > 0 && (
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.3 }}
                  className="bg-orange-900 bg-opacity-30 text-orange-300 p-6 rounded-xl border border-orange-700"
                >
                  <h3 className="text-xl font-semibold mb-3 flex items-center space-x-2">
                    <icons.AlertTriangle size={24} />
                    <span>Detected Conflicts & Resolutions</span>
                  </h3>
                  <ul className="list-disc list-inside space-y-2 text-sm">
                    {results.conflicts.map((conflict, index) => (
                      <li key={index}>{conflict}</li>
                    ))}
                  </ul>
                </motion.div>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                  className="bg-purple-900 bg-opacity-30 p-6 rounded-xl border border-purple-700 flex items-center justify-between"
                >
                  <div>
                    <h3 className="text-lg font-semibold text-purple-300">Final MCDA Score</h3>
                    <p className="text-sm text-purple-400">Multi-Criteria Decision Analysis</p>
                  </div>
                  <span className="text-4xl font-bold text-white">{results.mcdaScore}</span>
                </motion.div>
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ duration: 0.5, delay: 0.6 }}
                  className="bg-green-900 bg-opacity-30 p-6 rounded-xl border border-green-700 flex items-center justify-between"
                >
                  <div>
                    <h3 className="text-lg font-semibold text-green-300">System Balance Score</h3>
                    <p className="text-sm text-green-400">Harmony across all traits</p>
                  </div>
                  <span className="text-4xl font-bold text-white">{results.balanceScore}</span>
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
};

export default App;
