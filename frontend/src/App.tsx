import React, { useState } from 'react';
import { Search, Upload, BookOpen, Database, ShieldAlert, Cpu, ListFilter, ArrowRight, BarChart2 } from 'lucide-react';

// Types for Mock State
interface Filing {
  id: number;
  filename: string;
  ticker: string;
  formType: string;
  status: 'completed' | 'processing' | 'pending' | 'failed';
  date: string;
}

export default function App() {
  const [query, setQuery] = useState('');
  const [tickerFilter, setTickerFilter] = useState('');
  const [formTypeFilter, setFormTypeFilter] = useState('10-K');
  const [isLoading, setIsLoading] = useState(false);
  const [mockAnswer, setMockAnswer] = useState<string | null>(null);

  // Mock Filings List
  const [filings] = useState<Filing[]>([
    { id: 1, filename: 'apple_10k_2025.pdf', ticker: 'AAPL', formType: '10-K', status: 'completed', date: '2025-10-24' },
    { id: 2, filename: 'microsoft_10q_q2_2025.pdf', ticker: 'MSFT', formType: '10-Q', status: 'completed', date: '2025-01-30' },
    { id: 3, filename: 'nvidia_10k_2025.pdf', ticker: 'NVDA', formType: '10-K', status: 'processing', date: '2025-02-15' },
    { id: 4, filename: 'tesla_10k_2024.pdf', ticker: 'TSLA', formType: '10-K', status: 'pending', date: '2025-01-26' },
  ]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setMockAnswer(null);

    // Simulate RAG Pipeline process timer
    setTimeout(() => {
      setIsLoading(false);
      setMockAnswer(
        `Based on Apple's (AAPL) 2025 10-K filing, research and development expenses increased by 14% year-over-year to $32.5 billion, primarily driven by investments in silicon engineering and machine learning model optimization. Capital expenditures for data centers and compute infrastructures accounted for $8.4 billion.`
      );
    }, 1500);
  };

  return (
    <div style={styles.container}>
      {/* Sidebar Navigation */}
      <aside style={styles.sidebar}>
        <div style={styles.logoArea}>
          <Cpu size={28} style={styles.brandIcon} />
          <span style={styles.brandName}>SEC <span style={styles.brandAccent}>RAG</span></span>
        </div>
        
        <nav style={styles.navMenu}>
          <a href="#" style={{ ...styles.navLink, ...styles.navLinkActive }}>
            <Database size={18} />
            <span>Workspace</span>
          </a>
          <a href="#" style={styles.navLink}>
            <BookOpen size={18} />
            <span>Document Library</span>
          </a>
          <a href="#" style={styles.navLink}>
            <BarChart2 size={18} />
            <span>Pipeline Telemetry</span>
          </a>
        </nav>

        <div style={styles.systemStatus}>
          <div style={styles.statusHeader}>
            <ShieldAlert size={14} />
            <span>System Infrastructure</span>
          </div>
          <div style={styles.statusRow}>
            <span>Database:</span>
            <span style={styles.badgeOnline}>Online</span>
          </div>
          <div style={styles.statusRow}>
            <span>Vector Index:</span>
            <span style={styles.badgeOnline}>Online</span>
          </div>
        </div>
      </aside>

      {/* Main Workspace Area */}
      <main style={styles.mainContent}>
        {/* Header */}
        <header style={styles.header}>
          <div>
            <h1 style={styles.pageTitle}>Financial Intelligence Console</h1>
            <p style={styles.pageSubtitle}>Retrieve & Synthesize SEC Filings context using Clean RAG Architecture</p>
          </div>
          <button style={styles.uploadButton}>
            <Upload size={16} />
            <span>Upload SEC Filing</span>
          </button>
        </header>

        {/* Dashboard Grid */}
        <div style={styles.workspaceGrid}>
          {/* Query Console */}
          <section style={styles.querySection}>
            <h2 style={styles.sectionTitle}>Pipeline Query Interface</h2>
            <form onSubmit={handleSearchSubmit} style={styles.searchForm}>
              <div style={styles.searchInputWrapper}>
                <Search style={styles.searchIcon} size={20} />
                <input 
                  type="text" 
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask a question about filing details (e.g. 'Compare R&D expenditures...')"
                  style={styles.searchInput}
                />
              </div>

              {/* Advanced Query Filters */}
              <div style={styles.filtersWrapper}>
                <div style={styles.filterGroup}>
                  <ListFilter size={14} style={styles.filterIcon} />
                  <input
                    type="text"
                    value={tickerFilter}
                    onChange={(e) => setTickerFilter(e.target.value.toUpperCase())}
                    placeholder="Ticker (e.g. AAPL)"
                    style={styles.filterInput}
                  />
                </div>
                <div style={styles.filterGroup}>
                  <select 
                    value={formTypeFilter} 
                    onChange={(e) => setFormTypeFilter(e.target.value)}
                    style={styles.filterSelect}
                  >
                    <option value="10-K">Form 10-K</option>
                    <option value="10-Q">Form 10-Q</option>
                    <option value="8-K">Form 8-K</option>
                  </select>
                </div>
                <button type="submit" style={styles.submitButton} disabled={isLoading}>
                  {isLoading ? 'Synthesizing...' : 'Run Query'}
                  <ArrowRight size={16} />
                </button>
              </div>
            </form>

            {/* Answer Display */}
            {isLoading && (
              <div style={styles.loadingContainer}>
                <div style={styles.spinner}></div>
                <p style={styles.loadingText}>Retrieving vectors & generating response...</p>
              </div>
            )}

            {!isLoading && mockAnswer && (
              <div style={styles.responseContainer}>
                <h3 style={styles.responseHeader}>Generated Synthesis</h3>
                <p style={styles.responseText}>{mockAnswer}</p>
                <div style={styles.sourcesWrapper}>
                  <span style={styles.sourcesLabel}>Sources Utilized:</span>
                  <div style={styles.sourceTag}>apple_10k_2025.pdf (Chunk #12, Score: 0.95)</div>
                </div>
              </div>
            )}
          </section>

          {/* Filings List Panel */}
          <section style={styles.filingsSection}>
            <div style={styles.sectionHeader}>
              <h2 style={styles.sectionTitle}>Indexed SEC Filings</h2>
              <span style={styles.filingCount}>{filings.length} Total</span>
            </div>
            
            <div style={styles.filingsList}>
              {filings.map((filing) => (
                <div key={filing.id} style={styles.filingCard}>
                  <div style={styles.filingMeta}>
                    <span style={styles.tickerTag}>{filing.ticker}</span>
                    <span style={styles.formTag}>{filing.formType}</span>
                  </div>
                  <div style={styles.filingName}>{filing.filename}</div>
                  <div style={styles.filingFooter}>
                    <span style={styles.filingDate}>{filing.date}</span>
                    <span style={{
                      ...styles.statusTag,
                      ...(filing.status === 'completed' ? styles.statusCompleted : 
                           filing.status === 'processing' ? styles.statusProcessing : styles.statusPending)
                    }}>
                      {filing.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

// Styling Object - Dark Mode Glassmorphism Theme
const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    minHeight: '100vh',
    backgroundColor: '#0b0f19',
    color: '#f3f4f6',
    fontFamily: '"Outfit", "Inter", sans-serif',
  },
  sidebar: {
    width: '260px',
    backgroundColor: '#0f172a',
    borderRight: '1px solid #1e293b',
    padding: '24px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
  },
  logoArea: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: '40px',
  },
  brandIcon: {
    color: '#3b82f6',
  },
  brandName: {
    fontSize: '20px',
    fontWeight: 700,
    letterSpacing: '0.5px',
  },
  brandAccent: {
    color: '#3b82f6',
  },
  navMenu: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    flexGrow: 1,
  },
  navLink: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '12px 16px',
    borderRadius: '8px',
    color: '#94a3b8',
    textDecoration: 'none',
    transition: 'all 0.2s ease',
    fontWeight: 500,
  },
  navLinkActive: {
    backgroundColor: '#1e293b',
    color: '#3b82f6',
  },
  systemStatus: {
    backgroundColor: '#1e293b',
    borderRadius: '10px',
    padding: '16px',
    border: '1px solid #334155',
  },
  statusHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    color: '#94a3b8',
    fontSize: '12px',
    fontWeight: 600,
    marginBottom: '12px',
    textTransform: 'uppercase',
  },
  statusRow: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '13px',
    marginBottom: '8px',
  },
  badgeOnline: {
    color: '#10b981',
    fontWeight: 600,
  },
  mainContent: {
    flexGrow: 1,
    padding: '40px',
    display: 'flex',
    flexDirection: 'column',
    gap: '32px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  pageTitle: {
    fontSize: '28px',
    fontWeight: 700,
    margin: 0,
    background: 'linear-gradient(to right, #ffffff, #94a3b8)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  pageSubtitle: {
    fontSize: '14px',
    color: '#94a3b8',
    margin: '4px 0 0 0',
  },
  uploadButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: 600,
    transition: 'all 0.2s ease',
  },
  workspaceGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 320px',
    gap: '32px',
    flexGrow: 1,
  },
  querySection: {
    backgroundColor: '#0f172a',
    borderRadius: '16px',
    padding: '32px',
    border: '1px solid #1e293b',
    display: 'flex',
    flexDirection: 'column',
    gap: '24px',
  },
  sectionTitle: {
    fontSize: '18px',
    fontWeight: 600,
    margin: 0,
  },
  searchForm: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  searchInputWrapper: {
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
  },
  searchIcon: {
    position: 'absolute',
    left: '16px',
    color: '#64748b',
  },
  searchInput: {
    width: '100%',
    backgroundColor: '#0b0f19',
    border: '1px solid #334155',
    borderRadius: '10px',
    padding: '16px 16px 16px 52px',
    color: '#ffffff',
    fontSize: '15px',
    outline: 'none',
  },
  filtersWrapper: {
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
  },
  filterGroup: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    backgroundColor: '#0b0f19',
    border: '1px solid #334155',
    borderRadius: '8px',
    padding: '8px 12px',
  },
  filterIcon: {
    color: '#64748b',
  },
  filterInput: {
    background: 'none',
    border: 'none',
    color: '#ffffff',
    fontSize: '14px',
    outline: 'none',
    width: '120px',
  },
  filterSelect: {
    background: 'none',
    border: 'none',
    color: '#ffffff',
    fontSize: '14px',
    outline: 'none',
    cursor: 'pointer',
  },
  submitButton: {
    marginLeft: 'auto',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    backgroundColor: '#1e293b',
    border: '1px solid #3b82f6',
    color: '#3b82f6',
    padding: '10px 20px',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: 600,
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '40px 0',
    gap: '16px',
  },
  spinner: {
    width: '32px',
    height: '32px',
    border: '3px solid #334155',
    borderTop: '3px solid #3b82f6',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  loadingText: {
    color: '#94a3b8',
    fontSize: '14px',
  },
  responseContainer: {
    backgroundColor: '#0b0f19',
    borderRadius: '12px',
    padding: '24px',
    border: '1px solid #334155',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  responseHeader: {
    fontSize: '14px',
    fontWeight: 600,
    textTransform: 'uppercase',
    color: '#3b82f6',
    margin: 0,
  },
  responseText: {
    fontSize: '15px',
    lineHeight: 1.6,
    color: '#e2e8f0',
    margin: 0,
  },
  sourcesWrapper: {
    borderTop: '1px solid #1e293b',
    paddingTop: '16px',
    marginTop: '8px',
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  sourcesLabel: {
    fontSize: '12px',
    color: '#64748b',
    fontWeight: 600,
  },
  sourceTag: {
    fontSize: '13px',
    color: '#94a3b8',
  },
  filingsSection: {
    backgroundColor: '#0f172a',
    borderRadius: '16px',
    padding: '24px',
    border: '1px solid #1e293b',
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  sectionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  filingCount: {
    fontSize: '12px',
    color: '#64748b',
    fontWeight: 600,
  },
  filingsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    overflowY: 'auto',
  },
  filingCard: {
    backgroundColor: '#0b0f19',
    border: '1px solid #1e293b',
    borderRadius: '10px',
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  filingMeta: {
    display: 'flex',
    gap: '8px',
  },
  tickerTag: {
    backgroundColor: '#1e293b',
    color: '#3b82f6',
    fontSize: '11px',
    fontWeight: 700,
    padding: '2px 6px',
    borderRadius: '4px',
  },
  formTag: {
    backgroundColor: '#1e293b',
    color: '#94a3b8',
    fontSize: '11px',
    fontWeight: 700,
    padding: '2px 6px',
    borderRadius: '4px',
  },
  filingName: {
    fontSize: '13px',
    fontWeight: 500,
    color: '#f3f4f6',
  },
  filingFooter: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontSize: '11px',
    color: '#64748b',
  },
  statusTag: {
    padding: '2px 6px',
    borderRadius: '4px',
    fontSize: '10px',
    fontWeight: 600,
    textTransform: 'uppercase',
  },
  statusCompleted: {
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    color: '#10b981',
  },
  statusProcessing: {
    backgroundColor: 'rgba(245, 158, 11, 0.1)',
    color: '#f59e0b',
  },
  statusPending: {
    backgroundColor: 'rgba(100, 116, 139, 0.1)',
    color: '#64748b',
  },
};
