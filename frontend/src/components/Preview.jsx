export default function Preview({ imageUrl, metadata }) {
  if (!imageUrl) return null

  return (
    <div className="p-4 bg-white rounded-xl shadow-sm">
      <img src={imageUrl} alt="Uploaded" className="w-full rounded-lg" />
      {metadata && (
        <div className="mt-3 text-sm text-gray-600">
          {metadata.size && <p>Size: {metadata.size}</p>}
          {metadata.resolution && <p>Resolution: {metadata.resolution}</p>}
        </div>
      )}
    </div>
  )
}
