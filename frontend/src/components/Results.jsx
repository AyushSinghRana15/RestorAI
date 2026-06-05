export default function Results({ original, restored, stats }) {
  if (!restored) return null

  return (
    <div className="p-6 bg-white rounded-xl shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-gray-900">Results</h3>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="mb-1 text-sm font-medium text-gray-600">Original</p>
          <img src={original} alt="Original" className="w-full rounded-lg" />
        </div>
        <div>
          <p className="mb-1 text-sm font-medium text-gray-600">Restored</p>
          <img src={restored} alt="Restored" className="w-full rounded-lg" />
        </div>
      </div>
      {stats && (
        <div className="grid grid-cols-2 gap-4 mt-4 text-sm text-gray-600">
          <p>Processing Time: {stats.processing_time}s</p>
          <p>Models Used: {stats.models_used?.join(', ')}</p>
        </div>
      )}
      <div className="flex gap-3 mt-4">
        <a
          href={restored}
          download
          className="px-4 py-2 text-white bg-green-600 rounded-lg hover:bg-green-700 transition"
        >
          Download Restored
        </a>
      </div>
    </div>
  )
}
