import { useState } from 'react'
import Navbar from '../components/Navbar'
import Upload from '../components/Upload'
import Preview from '../components/Preview'
import Options from '../components/Options'
import Results from '../components/Results'
import { uploadImage, restoreImage, getStatus } from '../services/api'

export default function Dashboard() {
  const [file, setFile] = useState(null)
  const [jobId, setJobId] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [loading, setLoading] = useState(false)
  const [restoredUrl, setRestoredUrl] = useState(null)
  const [stats, setStats] = useState(null)
  const [options, setOptions] = useState({
    face: true,
    scratch: true,
    upscale: true,
    colorize: false,
  })

  const handleUpload = async (f) => {
    setFile(f)
    setRestoredUrl(null)
    setStats(null)
    setPreviewUrl(URL.createObjectURL(f))

    try {
      const data = await uploadImage(f)
      setJobId(data.job_id)
    } catch (err) {
      console.error('Upload failed:', err)
    }
  }

  const handleRestore = async () => {
    if (!jobId) return
    setLoading(true)

    try {
      const data = await restoreImage(jobId)
      setStats(data)
      const status = await getStatus(jobId)
      setRestoredUrl(status.restored)
    } catch (err) {
      console.error('Restore failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-5xl px-4 py-8 mx-auto">
        <h2 className="mb-6 text-2xl font-bold text-gray-900">Dashboard</h2>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2 space-y-6">
            {!previewUrl ? (
              <Upload onUpload={handleUpload} />
            ) : (
              <Preview imageUrl={previewUrl} />
            )}
            <Results
              original={previewUrl}
              restored={restoredUrl}
              stats={stats}
            />
          </div>

          <div className="space-y-6">
            <Options
              options={options}
              onChange={setOptions}
              onRestore={handleRestore}
              loading={loading}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
