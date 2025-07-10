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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg">
              <Database className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              SQL Query Agent
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered database assistant for generating, correcting, and exploring SQL queries
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-xl p-2 shadow-lg border border-gray-100">
            <div className="flex space-x-2">
              {tabs.map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  onClick={() => setActiveTab(id)}
                  className={cn(
                    'flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all duration-200',
                    activeTab === id
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md transform scale-105'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  )}
                >
                  <Icon className="h-5 w-5" />
                  <span>{label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="animate-slide-up">
          {/* SQL Generator */}
          {activeTab === 'generator' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                  <Wand2 className="h-6 w-6 text-blue-600 mr-3" />
                  Natural Language to SQL
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Describe what you want to query
                    </label>
                    <textarea
                      value={naturalLanguage}
                      onChange={(e) => setNaturalLanguage(e.target.value)}
                      placeholder="Example: Show me all customers from New York who made orders in the last 30 days"
                      className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    />
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <p className="text-sm text-gray-500">
                      Be specific about tables, columns, and conditions for better results
                    </p>
                    <button
                      onClick={handleGenerate}
                      disabled={!naturalLanguage.trim() || generateLoading}
                      className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105"
                    >
                      {generateLoading ? (
                        <>
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span>Generating...</span>
                        </>
                      ) : (
                        <>
                          <Wand2 className="h-4 w-4" />
                          <span>Generate SQL</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {generateError && (
                  <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2">
                    <XCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
                    <p className="text-red-800">{generateError}</p>
                  </div>
                )}

                {generatedSQL && (
                  <div className="mt-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                        <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                        Generated SQL
                      </h3>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => copyToClipboard(generatedSQL)}
                          className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                          <Copy className="h-4 w-4" />
                          <span>Copy</span>
                        </button>
                        <button
                          onClick={() => downloadSQL(generatedSQL, 'generated-query.sql')}
                          className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                          <Download className="h-4 w-4" />
                          <span>Download</span>
                        </button>
                      </div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-4 border">
                      <pre className="font-mono text-sm overflow-x-auto whitespace-pre-wrap text-gray-800">
                        {generatedSQL}
                      </pre>
                    </div>
                  </div>
                )}
              </div>

              {/* Examples */}
              <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Example Queries</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {[
                    "Show me all customers from New York",
                    "Find the top 10 products by sales",
                    "List customers who haven't placed orders recently",
                    "Calculate total revenue by month"
                  ].map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setNaturalLanguage(example)}
                      className="text-left p-3 bg-blue-50 rounded-lg border border-blue-200 hover:border-blue-300 hover:bg-blue-100 transition-all"
                    >
                      <p className="text-sm text-gray-700">{example}</p>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* SQL Corrector */}
          {activeTab === 'corrector' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                  <Wrench className="h-6 w-6 text-purple-600 mr-3" />
                  SQL Query Corrector
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Paste your SQL query that needs correction
                    </label>
                    <textarea
                      value={sqlToCorrect}
                      onChange={(e) => setSqlToCorrect(e.target.value)}
                      placeholder="Example: SELEC * FRM customerinfo WHER person_first_name = 'John'"
                      className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg resize-none font-mono text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    />
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <p className="text-sm text-gray-500">
                      Paste your broken SQL query and we'll fix syntax and logic errors
                    </p>
                    <button
                      onClick={handleCorrect}
                      disabled={!sqlToCorrect.trim() || correctLoading}
                      className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg font-medium hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105"
                    >
                      {correctLoading ? (
                        <>
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span>Correcting...</span>
                        </>
                      ) : (
                        <>
                          <Wrench className="h-4 w-4" />
                          <span>Correct SQL</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {correctError && (
                  <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2">
                    <XCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
                    <p className="text-red-800">{correctError}</p>
                  </div>
                )}

                {correctedSQL && (
                  <div className="mt-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                        <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                        Corrected SQL
                      </h3>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => copyToClipboard(correctedSQL)}
                          className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                          <Copy className="h-4 w-4" />
                          <span>Copy</span>
                        </button>
                        <button
                          onClick={() => downloadSQL(correctedSQL, 'corrected-query.sql')}
                          className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                          <Download className="h-4 w-4" />
                          <span>Download</span>
                        </button>
                      </div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-4 border">
                      <pre className="font-mono text-sm overflow-x-auto whitespace-pre-wrap text-gray-800">
                        {correctedSQL}
                      </pre>
                    </div>
                  </div>
                )}
              </div>

              {/* Common Errors */}
              <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Common SQL Errors We Fix</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium text-gray-800 mb-2">Syntax Errors</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• Missing keywords (SELECT, FROM, WHERE)</li>
                      <li>• Incorrect spelling (SELEC → SELECT)</li>
                      <li>• Missing semicolons</li>
                      <li>• Unmatched quotes or parentheses</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-800 mb-2">Logic Errors</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• Incorrect JOIN conditions</li>
                      <li>• Missing GROUP BY clauses</li>
                      <li>• Wrong aggregate functions</li>
                      <li>• Improper WHERE conditions</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Schema Explorer */}
          {activeTab === 'schema' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                  <Database className="h-6 w-6 text-green-600 mr-3" />
                  Database Schema Explorer
                </h2>

                {schemaLoading && (
                  <div className="flex items-center justify-center py-12">
                    <div className="text-center">
                      <Loader2 className="h-8 w-8 animate-spin text-green-600 mx-auto mb-4" />
                      <p className="text-gray-600">Loading database schema...</p>
                    </div>
                  </div>
                )}

                {schemaError && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2">
                    <XCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
                    <p className="text-red-800">{schemaError}</p>
                  </div>
                )}

                {schemaData && (
                  <div>
                    <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                      <p className="text-green-800 font-medium">
                        Found {Object.keys(schemaData).length} tables in your database
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {Object.entries(schemaData).map(([tableName, columns]) => (
                        <div 
                          key={tableName} 
                          className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md hover:border-green-300 transition-all"
                        >
                          <div className="flex items-center space-x-2 mb-4">
                            <Database className="h-5 w-5 text-green-600" />
                            <h3 className="text-lg font-semibold text-gray-900">{tableName}</h3>
                          </div>
                          
                          <p className="text-sm text-gray-600 mb-3">
                            {columns.length} column{columns.length !== 1 ? 's' : ''}
                          </p>
                          
                          <div className="space-y-2 max-h-32 overflow-y-auto">
                            {columns.map((column, index) => (
                              <div key={index} className="flex items-center space-x-2 py-1">
                                <div className="w-2 h-2 bg-blue-400 rounded-full flex-shrink-0" />
                                <span className="text-sm text-gray-700 font-mono">{column}</span>
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
