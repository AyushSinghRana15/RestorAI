import { useCallback } from 'react'

export default function Upload({ onUpload }) {
  const handleDrop = useCallback((e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file) onUpload(file)
  }, [onUpload])

  const handleChange = (e) => {
    const file = e.target.files[0]
    if (file) onUpload(file)
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      className="flex flex-col items-center justify-center p-12 border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-gray-100 cursor-pointer transition"
    >
      <p className="mb-2 text-lg font-medium text-gray-700">
        Drag & drop your image here
      </p>
      <p className="mb-4 text-sm text-gray-500">JPG, JPEG, PNG, WEBP (max 20 MB)</p>
      <label className="px-6 py-2 text-white bg-blue-600 rounded-lg cursor-pointer hover:bg-blue-700">
        Browse Files
        <input type="file" accept=".jpg,.jpeg,.png,.webp" onChange={handleChange} className="hidden" />
      </label>
    </div>
  )
}
