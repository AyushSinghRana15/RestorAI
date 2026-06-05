export default function Options({ options, onChange, onRestore, loading }) {
  const toggles = [
    { key: 'face', label: 'Face Restoration (GFPGAN)' },
    { key: 'scratch', label: 'Scratch Removal (LaMa)' },
    { key: 'upscale', label: 'Upscaling (Real-ESRGAN)' },
    { key: 'colorize', label: 'Colorization (DeOldify)' },
  ]

  return (
    <div className="p-6 bg-white rounded-xl shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-gray-900">Restoration Options</h3>
      <div className="space-y-3">
        {toggles.map(({ key, label }) => (
          <label key={key} className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={options[key]}
              onChange={() => onChange({ ...options, [key]: !options[key] })}
              className="w-4 h-4 text-blue-600 rounded"
            />
            <span className="text-sm text-gray-700">{label}</span>
          </label>
        ))}
      </div>
      <button
        onClick={onRestore}
        disabled={loading}
        className="w-full mt-6 px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
      >
        {loading ? 'Processing...' : 'Restore Image'}
      </button>
    </div>
  )
}
