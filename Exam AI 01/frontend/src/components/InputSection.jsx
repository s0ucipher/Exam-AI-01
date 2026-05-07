import { useState } from 'react'
import {
  CheckCircle2,
  FilePlus2,
  FolderOpen,
  FolderPlus,
  Play,
  ScanLine,
  SortAsc,
  Target,
  X,
} from 'lucide-react'

export default function InputSection({
  onChooseDestination,
  onChooseFiles,
  onChooseFolders,
  onSubmit,
  choosingAction,
  loading,
}) {
  const [sources, setSources] = useState([])
  const [destinationPath, setDestinationPath] = useState('')
  const [sortBy, setSortBy] = useState('name')
  const [applyChanges, setApplyChanges] = useState(false)

  const addSources = (paths) => {
    setSources((currentSources) => {
      const merged = [...currentSources, ...paths]
      return [...new Set(merged)]
    })
  }

  const handleChooseFiles = async () => {
    const selectedPaths = await onChooseFiles()
    addSources(selectedPaths)
  }

  const handleChooseFolders = async () => {
    const selectedPaths = await onChooseFolders()
    addSources(selectedPaths)
  }

  const handleChooseDestination = async () => {
    const selectedPath = await onChooseDestination()
    if (selectedPath) {
      setDestinationPath(selectedPath)
    }
  }

  const handleRemoveSource = (source) => {
    setSources((currentSources) => currentSources.filter((item) => item !== source))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    onSubmit({ sources, destinationPath, sortBy, applyChanges })
  }

  const isChoosing = Boolean(choosingAction)

  return (
    <form className="input-panel" onSubmit={handleSubmit}>
      <div className="input-glow" aria-hidden="true" />
      <div className="input-heading">
        <span className="heading-icon"><ScanLine size={24} /></span>
        <div>
          <h2>Universal Source Scanner</h2>
          <p>Add individual files, multiple folders, or both. s0ucipher will organize the full batch.</p>
        </div>
      </div>

      <div className="source-builder">
        <div className="source-actions">
          <button
            className="choose-folder-action"
            disabled={isChoosing || loading}
            type="button"
            onClick={handleChooseFiles}
          >
            {choosingAction === 'files' ? <span className="spinner dark-spinner" /> : <FilePlus2 size={18} />}
            {choosingAction === 'files' ? 'Opening...' : 'Add Files'}
          </button>

          <button
            className="choose-folder-action folder-action"
            disabled={isChoosing || loading}
            type="button"
            onClick={handleChooseFolders}
          >
            {choosingAction === 'folders' ? <span className="spinner dark-spinner" /> : <FolderPlus size={18} />}
            {choosingAction === 'folders' ? 'Opening...' : 'Add Folders'}
          </button>
        </div>

        <div className="selected-sources">
          {sources.length ? (
            sources.map((source) => (
              <div className="source-token" key={source}>
                <FolderOpen size={18} />
                <span>{source}</span>
                <button type="button" onClick={() => handleRemoveSource(source)} aria-label={`Remove ${source}`}>
                  <X size={16} />
                </button>
              </div>
            ))
          ) : (
            <div className="empty-source-token">
              <FolderOpen size={18} />
              <span>No files or folders added yet</span>
            </div>
          )}
        </div>
      </div>

      <div className="destination-row">
        <div className="destination-copy">
          <Target size={19} />
          <div>
            <strong>Output location</strong>
            <span>{destinationPath || 'Auto: NeuroSort will choose a safe organized folder'}</span>
          </div>
        </div>
        <button
          className="secondary-action"
          disabled={isChoosing || loading}
          type="button"
          onClick={handleChooseDestination}
        >
          {choosingAction === 'destination' ? <span className="spinner dark-spinner" /> : <Target size={17} />}
          {choosingAction === 'destination' ? 'Opening...' : 'Choose Output'}
        </button>
      </div>

      <div className="organizer-controls">
        <label className="select-wrap">
          <SortAsc size={18} />
          <span>Sort</span>
          <select value={sortBy} onChange={(event) => setSortBy(event.target.value)} disabled={loading}>
            <option value="name">Alphabetical</option>
            <option value="type">File type</option>
          </select>
        </label>

        <label className="toggle-row">
          <input
            type="checkbox"
            checked={applyChanges}
            onChange={(event) => setApplyChanges(event.target.checked)}
            disabled={loading}
          />
          <span>{applyChanges ? 'Move mode active' : 'Preview first'}</span>
          {applyChanges && <CheckCircle2 size={18} />}
        </label>

        <button className="primary-action" type="submit" disabled={loading || !sources.length}>
          {loading ? <span className="spinner" /> : <Play size={18} />}
          {loading ? 'Scanning...' : 'Organize Batch'}
        </button>
      </div>
    </form>
  )
}
