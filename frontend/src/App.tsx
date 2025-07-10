import React, { useState, useEffect } from 'react';
import { Database, Wand2, Wrench, Copy, Download, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { useGenerateSQL, useCorrectSQL, useSchema } from './hooks/useApi';
import { cn } from './utils/cn';

export type ActiveTab = 'generator' | 'corrector' | 'schema';

function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('generator');
  const [naturalLanguage, setNaturalLanguage] = useState('');
  const [sqlToCorrect, setSqlToCorrect] = useState('');
  const [generatedSQL, setGeneratedSQL] = useState('');
  const [correctedSQL, setCorrectedSQL] = useState('');
  const [schemaData, setSchemaData] = useState<Record<string, string[]> | null>(null);

  const { generateSQL, loading: generateLoading, error: generateError } = useGenerateSQL();
  const { correctSQL, loading: correctLoading, error: correctError } = useCorrectSQL();
  const { fetchSchema, loading: schemaLoading, error: schemaError } = useSchema();

  useEffect(() => {
    if (activeTab === 'schema') {
      loadSchema();
    }
  }, [activeTab]);

  const handleGenerate = async () => {
    if (!naturalLanguage.trim()) return;
    try {
      const result = await generateSQL(naturalLanguage);
      if (result.success) {
        setGeneratedSQL(result.sql);
      }
    } catch (error) {
      console.error('Generation failed:', error);
    }
  };

  const handleCorrect = async () => {
    if (!sqlToCorrect.trim()) return;
    try {
      const result = await correctSQL(sqlToCorrect);
      if (result.success) {
        setCorrectedSQL(result.corrected_sql);
      }
    } catch (error) {
      console.error('Correction failed:', error);
    }
  };

  const loadSchema = async () => {
    try {
      const result = await fetchSchema();
      if (result.success) {
        setSchemaData(result.schema);
      }
    } catch (error) {
      console.error('Schema fetch failed:', error);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
    }
  };

  const downloadSQL = (sql: string, filename: string) => {
    const blob = new Blob([sql], { type: 'text/sql' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const tabs = [
    { id: 'generator' as ActiveTab, label: 'SQL Generator', icon: Wand2, color: 'text-blue-600' },
    { id: 'corrector' as ActiveTab, label: 'SQL Corrector', icon: Wrench, color: 'text-purple-600' },
    { id: 'schema' as ActiveTab, label: 'Schema Explorer', icon: Database, color: 'text-green-600' },
  ];

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10 animate-fade-in">
          <div className="flex items-center justify-center space-x-4 mb-5">
            <div className="p-4 bg-gradient-to-tr from-purple-700 via-pink-600 to-red-500 rounded-3xl shadow-lg">
              <Database className="h-10 w-10 text-white" />
            </div>
            <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-700 via-pink-600 to-red-500 bg-clip-text text-transparent">
              SQL Query Agent
            </h1>
          </div>
          <p className="text-lg text-gray-700 max-w-3xl mx-auto">
            AI-powered database assistant for generating, correcting, and exploring SQL queries
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-10">
          <div className="bg-white rounded-full p-1 shadow-xl border border-gray-200">
            <div className="flex space-x-3">
              {tabs.map(({ id, label, icon: Icon, color }) => (
                <button
                  key={id}
                  onClick={() => setActiveTab(id)}
                  className={cn(
                    'flex items-center space-x-3 px-8 py-3 rounded-full font-semibold transition-all duration-300 select-none cursor-pointer',
                    activeTab === id
                      ? `bg-gradient-to-r from-purple-600 to-pink-500 text-white shadow-lg scale-105 ${color}`
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  )}
                >
                  <Icon className="h-6 w-6" />
                  <span className="text-lg">{label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="animate-slide-up">
          {/* SQL Generator */}
          {activeTab === 'generator' && (
            <div className="space-y-8">
              <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-10">
                <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center">
                  <Wand2 className="h-8 w-8 text-purple-600 mr-4" />
                  Natural Language to SQL
                </h2>

                <div className="space-y-6">
                  <div>
                    <label className="block text-lg font-medium text-gray-700 mb-3">
                      Describe your query
                    </label>
                    <textarea
                      value={naturalLanguage}
                      onChange={e => setNaturalLanguage(e.target.value)}
                      placeholder="e.g. Show me all customers from New York who made orders in the last 30 days"
                      className="w-full h-36 px-5 py-4 border border-gray-300 rounded-xl shadow-sm resize-none focus:outline-none focus:ring-4 focus:ring-purple-400 transition"
                    />
                  </div>

                  <div className="flex justify-between items-center">
                    <p className="text-sm text-gray-500">
                      Be as specific as possible for better results
                    </p>
                    <button
                      onClick={handleGenerate}
                      disabled={!naturalLanguage.trim() || generateLoading}
                      className="inline-flex items-center space-x-3 bg-gradient-to-r from-purple-600 to-pink-500 text-white font-semibold px-6 py-3 rounded-xl shadow-lg hover:from-purple-700 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-transform transform hover:scale-105"
                    >
                      {generateLoading ? (
                        <>
                          <Loader2 className="h-5 w-5 animate-spin" />
                          <span>Generating...</span>
                        </>
                      ) : (
                        <>
                          <Wand2 className="h-5 w-5" />
                          <span>Generate SQL</span>
                        </>
                      )}
                    </button>
                  </div>

                  {generateError && (
                    <div className="mt-6 p-4 bg-red-100 border border-red-400 rounded-lg flex items-center space-x-3">
                      <XCircle className="h-6 w-6 text-red-600" />
                      <p className="text-red-700 font-semibold">{generateError}</p>
                    </div>
                  )}

                  {generatedSQL && (
                    <div className="mt-8">
                      <div className="flex justify-between items-center mb-4">
                        <h3 className="text-xl font-semibold text-gray-900 flex items-center">
                          <CheckCircle className="h-6 w-6 text-green-600 mr-3" />
                          Generated SQL
                        </h3>
                        <div className="flex space-x-4">
                          <button
                            onClick={() => copyToClipboard(generatedSQL)}
                            className="inline-flex items-center space-x-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg shadow hover:bg-gray-200 transition"
                          >
                            <Copy className="h-5 w-5" />
                            <span>Copy</span>
                          </button>
                          <button
                            onClick={() => downloadSQL(generatedSQL, 'generated-query.sql')}
                            className="inline-flex items-center space-x-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg shadow hover:bg-gray-200 transition"
                          >
                            <Download className="h-5 w-5" />
                            <span>Download</span>
                          </button>
                        </div>
                      </div>
                      <pre className="bg-gray-50 p-6 rounded-xl border border-gray-200 font-mono text-sm text-gray-800 overflow-x-auto">
                        {generatedSQL}
                      </pre>
                    </div>
                  )}
                </div>
              </div>

              <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Examples</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[
                    "Show me all customers from New York",
                    "Find the top 10 products by sales",
                    "List customers who haven't placed orders recently",
                    "Calculate total revenue by month"
                  ].map((example, idx) => (
                    <button
                      key={idx}
                      onClick={() => setNaturalLanguage(example)}
                      className="text-left p-4 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl border border-purple-300 hover:from-purple-200 hover:to-pink-200 transition"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* SQL Corrector */}
          {activeTab === 'corrector' && (
            <div className="space-y-8">
              <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-10">
                <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center">
                  <Wrench className="h-8 w-8 text-pink-600 mr-4" />
                  SQL Query Corrector
                </h2>

                <div className="space-y-6">
                  <div>
                    <label className="block text-lg font-medium text-gray-700 mb-3">
                      Paste your SQL query that needs correction
                    </label>
                    <textarea
                      value={sqlToCorrect}
                      onChange={e => setSqlToCorrect(e.target.value)}
                      placeholder="e.g. SELEC * FRM customer WHERE id = 1"
                      className="w-full h-36 px-5 py-4 border border-gray-300 rounded-xl shadow-sm resize-none font-mono focus:outline-none focus:ring-4 focus:ring-pink-400 transition"
                    />
                  </div>

                  <div className="flex justify-between items-center">
                    <p className="text-sm text-gray-500">
                      Paste broken SQL and get corrected version
                    </p>
                    <button
                      onClick={handleCorrect}
                      disabled={!sqlToCorrect.trim() || correctLoading}
                      className="inline-flex items-center space-x-3 bg-gradient-to-r from-pink-600 to-purple-600 text-white font-semibold px-6 py-3 rounded-xl shadow-lg hover:from-pink-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-transform transform hover:scale-105"
                    >
                      {correctLoading ? (
                        <>
                          <Loader2 className="h-5 w-5 animate-spin" />
                          <span>Correcting...</span>
                        </>
                      ) : (
                        <>
                          <Wrench className="h-5 w-5" />
                          <span>Correct SQL</span>
                        </>
                      )}
                    </button>
                  </div>

                  {correctError && (
                    <div className="mt-6 p-4 bg-red-100 border border-red-400 rounded-lg flex items-center space-x-3">
                      <XCircle className="h-6 w-6 text-red-600" />
                      <p className="text-red-700 font-semibold">{correctError}</p>
                    </div>
                  )}

                  {correctedSQL && (
                    <div className="mt-8">
                      <div className="flex justify-between items-center mb-4">
                        <h3 className="text-xl font-semibold text-gray-900 flex items-center">
                          <CheckCircle className="h-6 w-6 text-green-600 mr-3" />
                          Corrected SQL
                        </h3>
                        <div className="flex space-x-4">
                          <button
                            onClick={() => copyToClipboard(correctedSQL)}
                            className="inline-flex items-center space-x-3 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg shadow hover:bg-gray-200 transition"
                          >
                            <Copy className="h-5 w-5" />
                            <span>Copy</span>
                          </button>
                          <button
                            onClick={() => downloadSQL(correctedSQL, 'corrected-query.sql')}
                            className="inline-flex items-center space-x-3 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg shadow hover:bg-gray-200 transition"
                          >
                            <Download className="h-5 w-5" />
                            <span>Download</span>
                          </button>
                        </div>
                      </div>
                      <pre className="bg-gray-50 p-6 rounded-xl border border-gray-200 font-mono text-sm text-gray-800 overflow-x-auto">
                        {correctedSQL}
                      </pre>
                    </div>
                  )}
                </div>
              </div>

              <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Common Errors</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium text-gray-800 mb-3">Syntax Errors</h4>
                    <ul className="text-sm text-gray-600 space-y-2 list-disc list-inside">
                      <li>Missing keywords (SELECT, FROM, WHERE)</li>
                      <li>Incorrect spelling (e.g., SELEC → SELECT)</li>
                      <li>Missing semicolons</li>
                      <li>Unmatched quotes or parentheses</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-800 mb-3">Logic Errors</h4>
                    <ul className="text-sm text-gray-600 space-y-2 list-disc list-inside">
                      <li>Incorrect JOIN conditions</li>
                      <li>Missing GROUP BY clauses</li>
                      <li>Wrong aggregate functions</li>
                      <li>Improper WHERE conditions</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Schema Explorer */}
          {activeTab === 'schema' && (
            <div className="space-y-8">
              <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-10">
                <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center">
                  <Database className="h-8 w-8 text-green-600 mr-4" />
                  Database Schema Explorer
                </h2>

                {schemaLoading && (
                  <div className="flex justify-center items-center py-16">
                    <Loader2 className="h-10 w-10 animate-spin text-green-600" />
                    <span className="ml-4 text-lg text-gray-600">Loading schema...</span>
                  </div>
                )}

                {schemaError && (
                  <div className="p-6 bg-red-100 border border-red-400 rounded-lg flex items-center space-x-4">
                    <XCircle className="h-8 w-8 text-red-600" />
                    <p className="text-red-700 font-semibold">{schemaError}</p>
                  </div>
                )}

                {schemaData && (
                  <div>
                    <div className="mb-8 p-6 bg-green-50 border border-green-300 rounded-lg">
                      <p className="text-green-700 font-semibold">
                        Found {Object.keys(schemaData).length} tables in your database
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                      {Object.entries(schemaData).map(([tableName, columns]) => (
                        <div key={tableName} className="bg-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition">
                          <div className="flex items-center space-x-3 mb-4">
                            <Database className="h-6 w-6 text-green-600" />
                            <h3 className="text-xl font-semibold text-gray-900">{tableName}</h3>
                          </div>
                          <p className="text-gray-700 mb-3">{columns.length} columns</p>
                          <div className="max-h-40 overflow-y-auto">
                            {columns.map((col, idx) => (
                              <div key={idx} className="flex items-center space-x-2 py-1">
                                <div className="w-3 h-3 bg-green-400 rounded-full" />
                                <span className="text-sm font-mono text-gray-800">{col}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
